# coding:utf-8
from core.command_handler import FtpCommands
from core.user_handler import UserHandler
from core.orm import SomeError
from conf.settings import DB_TEMP
from datetime import datetime
from conf.settings import Separator
import json
import os
import socket
import select
import queue


class SelectSocketServer(object):
    def __init__(self, host, port):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.server.setblocking(False)
        self.inputs = [self.server]
        self.outputs = []
        self.message_queues = {}
        self.client_cache = {}

    def run(self):
        while True:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for r in readable:
                if r is self.server:
                    conn, address = r.accept()
                    self.inputs.append(conn)
                    self.message_queues[conn] = queue.Queue()
                else:
                    if r not in self.client_cache:
                        ftp = FtpHandler(r)
                        self.client_cache[r] = ftp
                    # 每次请求的数据包data都会小于2048，接收到后放到队列中暂不处理，服务端只有等客户端发出recv请求时才处理
                    data = r.recv(2048)
                    if data:
                        self.message_queues[r].put(data)
                        self.outputs.append(r)
                    else:
                        # 无数据表示，客户端已断开连接
                        if r in self.outputs:
                            self.outputs.remove(r)
                        self.inputs.remove(r)
                        r.close()
                        del self.message_queues[r]

            for w in writeable:
                # 当客户端发出recv请求时，才取出队列中数据，进行处理，并发送响应数据
                try:
                    data = self.message_queues[w].get_nowait()
                except queue.Empty:
                    print(u"队列为空，无请求数据")
                    self.outputs.remove(w)
                else:
                    ftp = self.client_cache[w]
                    cmd, rsp = ftp.get_response(data)
                    ftp.sendall_data(cmd, rsp)
                    self.outputs.remove(w)

            for e in exceptional:
                if e in self.outputs:
                    self.outputs.remove(e)
                del self.message_queues[e]
                del self.client_cache[e]


class FtpHandler(object):
    def __init__(self, request):
        self.username = None
        self.user_handler = UserHandler()
        self.ftp_commands = FtpCommands()
        self.request = request
        self.temp_file_cache = {}

    def get_response(self, data):
        """处理单个客户端连接与请求"""
        cmd, kwargs = self.parse_data(data)
        if cmd == "register":
            response = self.user_handler.register(**kwargs)
        elif cmd == "login":
            response = self.user_handler.login(**kwargs)
            if response.code == 200:
                self.username = self.user_handler.username
        elif cmd == "logout":
            response = self.user_handler.logout()
            if response.code == 200:
                self.username = None
        else:
            self.ftp_commands.update_user_status(self.username)
            response = self.ftp_commands.run(cmd, **kwargs)
        return cmd, response

    @staticmethod
    def split_request_data(data):
        """根据分隔符拆分请求数据"""
        data_list = data.split(Separator)
        if len(data_list) == 1:
            json_string = data_list[0]
            file_data = b""
        elif len(data_list) == 2:
            json_string = data_list[0]
            file_data = data_list[1]
        else:
            raise SomeError("传输的请求数据包格式有误，请联系管理员")

        return json_string, file_data

    def update_temp_file_cache(self, time_stamp, file_size, file_data):
        """
        1.以时间戳未key来记录上传文件的缓存内容文件;
        2.更新上传文件的已缓存的文件内容;
        3.如果缓存文件大小与上传文件大小一致，则表示完成文件传输
        """
        ret = {}
        if time_stamp:
            temp_file_path = self.temp_file_cache.get(time_stamp)
        else:
            now = datetime.now()
            time_stamp = now.strftime("%Y-%m-%d_%H%M%S")
            temp_file_path = os.path.join(DB_TEMP, "temp_file_{0}_{1}".format(file_size, time_stamp))
            self.temp_file_cache[time_stamp] = temp_file_path
        with open(temp_file_path, "ab") as f:
            f.write(file_data)
            f.flush()
        temp_file_size = os.path.getsize(temp_file_path)
        if temp_file_size == file_size:
            del self.temp_file_cache[time_stamp]
            ret["temp_file_path"] = temp_file_path
            ret["time_stamp"] = time_stamp
        else:
            ret["temp_file_path"] = None
            ret["time_stamp"] = time_stamp

        return ret

    def parse_data(self, data):
        """
        解析data数据包内容，,data存在两种结构构成：
        1.普通命令请求，data为纯json格式字符串；
        2.上传文件的请求，data为拼接字符串，如：上传文件请求json字符串 + 分隔符 + 部分文件内容数据块内容；
        针对上传文件请求，需要先根据分隔符拆分data数据，再进行后续处理
        """
        json_string, file_data = self.split_request_data(data)
        payload = json.loads(json_string.decode("utf-8"))
        cmd = payload["cmd"]
        kwargs = payload["kwargs"]
        if cmd == "put":
            file_size = kwargs.pop("file_size", None)
            time_stamp = kwargs.get("time_stamp", None)
            ret_dict = self.update_temp_file_cache(time_stamp, file_size, file_data)
            kwargs.update(ret_dict)
        return cmd, kwargs

    def sendall_data(self, cmd, response):
        """发送请求响应数据，对get下载文件的请求单独请求"""
        if cmd == "get" and response.code == 201:
            file_path = response.data.pop("file_path")
            tmp_size = response.data.pop("tmp_size")
            with open(file_path, "rb") as f:
                f.seek(tmp_size)
                file_data = f.read(1024)
            response_body = json.dumps(response.__dict__).encode("utf-8")
            b_str = response_body + Separator + file_data
        else:
            b_str = json.dumps(response.__dict__).encode("utf-8")
        self.request.sendall(b_str)
