# coding:utf-8
from core.command_handler import FtpCommands
from core.user_handler import UserHandler
from core.orm import SomeError
from conf.settings import DB_TEMP
from datetime import datetime
import json
import os
import socket
import select
import queue
import threading


class SelectSocketServer(object):
    def __init__(self, host, port):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.server.setblocking(False)
        self.queue_dict = {}
        self.conn_cache = {}

    def run(self):
        # 将socket服务端加入到检测列表inputs中
        inputs = [self.server]
        outputs = []

        while True:
            # 初始执行检测，只有server处于检测列表中
            try:
                readable, writeable, exceptional = select.select(inputs, outputs, inputs, 1)
            except Exception:
                break
            for r in readable:
                if r is self.server:
                    # 检测到server变活跃则表示有新连接过来，则将新连接conn加入到检测列表inputs中
                    conn, addr = r.accept()
                    inputs.append(conn)
                    self.queue_dict[conn] = queue.Queue()  # 初始化一个队列
                else:
                    if r in self.conn_cache:
                        ftp = self.conn_cache[r]
                    else:
                        ftp = FtpHandler(r)
                        self.conn_cache[r] = ftp
                    # 创建子线程异步处理单个socket的数据请求的操作，由于传输大文件内容的柱塞问题，选择子线程异步处理请求
                    que = self.queue_dict[r]
                    req_thread = RequestThread(r, ftp, que, outputs)
                    req_thread.start()

            for w in outputs:
                # 创建子线程异步处理单个socket的请求响应数据的发送操作，由于传输大文件内容会柱塞问题，子线程异步处理请求
                ftp = self.conn_cache[w]
                que = self.queue_dict[w]
                rsp_thread = ResponseThread(w, ftp, que)
                rsp_thread.start()
                # 开启异步处理后，直接将socket连接句柄从outputs列表中移出
                outputs.remove(w)

            for e in exceptional:
                if e in outputs:
                    outputs.remove(e)
                inputs.remove(e)
                del self.queue_dict[e]
                del self.conn_cache[e]


class RequestThread(threading.Thread):
    def __init__(self, request, ftp_obj, que, outputs):
        self.request = request
        self.ftp_obj = ftp_obj
        self.que = que
        self.outputs = outputs
        threading.Thread.__init__(self)

    def run(self):
        cmd, data = self.ftp_obj.get_response()
        # 处理完请求后，返回数据放入到队列中
        response_data = (cmd, data)
        self.que.put(response_data)
        # 处理完请求后，将需要返回响应数据的请求放入到outputs列表中
        self.outputs.append(self.request)


class ResponseThread(threading.Thread):
    def __init__(self, request, ftp_obj, que):
        self.request = request
        self.ftp_obj = ftp_obj
        self.que = que
        threading.Thread.__init__(self)

    def run(self):
        # 取到请求返回数据
        cmd, data = self.que.get()
        # 执行请求放回数据的send发送
        self.ftp_obj.sendall_data(cmd, data)


class FtpHandler(object):
    def __init__(self, request):
        self.username = None
        self.user_handler = UserHandler()
        self.ftp_commands = FtpCommands()
        self.request = request

    def get_response(self):
        """处理单个客户端连接与请求"""
        try:
            while True:
                cmd, kwargs = self.receive_data()
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
        except ConnectionResetError as e:
            msg = u"客户端连接{0}已经断开连接，详细：{1}".format(self.request, str(e))
            print(msg)

    def receive_data(self):
        """接收数据并进行解析，与客户端协议约定请求交互为json数据，格式：
        {"cmd": "cmd_name", "kwargs":{"key1": "value1", "key2": "value2"} },
        对上传文件请求（cmd=put）做单独处理
        """
        data = self.request.recv(1024)
        if not data:
            raise SomeError("客户端主动关闭连接")
        payload = json.loads(data.decode("utf-8"))
        print(payload)
        cmd = payload["cmd"]
        kwargs = payload["kwargs"]
        if cmd == "put":
            file_size = kwargs.pop("file_size")
            self.ftp_commands.validate_quota(file_size)
            temp_file_path = self._receive_file_data(file_size)
            kwargs["temp_file_path"] = temp_file_path
        return cmd, kwargs

    def _receive_file_data(self, file_size):
        """接收文件数据，暂时存放在临时文件内"""
        try:
            self.request.setblocking(True)
            now = datetime.now()
            time_stamp = now.strftime("%Y-%m-%d_%H%M%S")
            temp_file = os.path.join(DB_TEMP, "temp_file_{0}_{1}".format(file_size, time_stamp))
            receive_size = 0
            f = open(temp_file, "wb")
            while True:
                diff = file_size - receive_size
                if diff > 1024:
                    data = self.request.recv(1024)
                elif diff == 0:
                    f.close()
                    break
                else:
                    data = self.request.recv(diff)
                f.write(data)
                f.flush()
                receive_size += len(data)
        finally:
            self.request.setblocking(False)
        return temp_file

    def sendall_data(self, cmd, response):
        """发送请求响应数据,对下载文件请求（cmd=get）做单独处理"""
        try:
            response_body = json.dumps(response.__dict__).encode("utf-8")
            self.request.sendall(response_body)
            if cmd == "get" and response.code == 200:
                self.request.setblocking(True)
                file_path = response.data.pop("file_path")
                seek_size = response.data.get("seek_size")
                with open(file_path, "rb") as f:
                    f.seek(seek_size)
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        self.request.sendall(data)
        finally:
            self.request.setblocking(False)
