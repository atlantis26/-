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


class SelectSocketServer(object):
    def __init__(self, host, port):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.server.setblocking(False)
        self.inputs = [self.server]
        self.outputs = []
        self.queue_dict = {}
        self.client_cache = {}

    def run(self):
        while True:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for r in readable:
                if r is self.server:
                    conn, address = r.accept()
                    self.inputs.append(conn)
                    self.queue_dict[conn] = queue.Queue()
                else:
                    if r not in self.client_cache:
                        ftp = FtpHandler(r)
                        self.client_cache[r] = ftp
                    data = r.recv(2048)
                    self.queue_dict[r].put(data)
                    self.outputs.append(r)

            for w in writeable:
                data = self.queue_dict[w].get()
                ftp = self.client_cache[w]
                cmd, rsp = ftp.get_response(data)
                ftp.sendall_data(cmd, rsp)
                self.outputs.remove(w)

            for e in exceptional:
                if e in self.outputs:
                    self.outputs.remove(e)
                    self.inputs.remove(e)
                del self.queue_dict[e]
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

    def parse_data(self, data):
        separator = b"---woshifenggefu---"
        data_list = data.split(separator)
        if len(data_list) == 1:
            json_string = data_list[0]
            file_data = None
        else:
            json_string = data_list[0]
            file_data = data_list[1]
        payload = json.loads(json_string.decode("utf-8"))
        cmd = payload["cmd"]
        kwargs = payload["kwargs"]
        if cmd == "put":
            file_size = kwargs.pop("file_size", None)
            time_stamp = kwargs.pop("time_stamp", None)
            temp_file = self.temp_file_cache.get(time_stamp, None)
            if not temp_file:
                now = datetime.now()
                time_stamp = now.strftime("%Y-%m-%d_%H%M%S")
                temp_file = os.path.join(DB_TEMP, "temp_file_{0}_{1}".format(file_size, time_stamp))
                self.temp_file_cache[time_stamp] = temp_file
            is_ok = self.save_data_and_check_is_ok(temp_file, file_size, file_data)
            if is_ok:
                kwargs["temp_file_path"] = temp_file
                del self.temp_file_cache[time_stamp]
            else:
                kwargs["temp_file_path"] = None
        return cmd, kwargs

    @staticmethod
    def save_data_and_check_is_ok(file_path, file_size, file_data):
        """接收文件数据，暂时存放在临时文件内"""
        with open(file_path, "wb") as f:
            f.write(file_data)
            f.flush()
        size = os.path.getsize(file_path)
        if size == file_size:
            return True

    def sendall_data(self, cmd, response):
        response_body = json.dumps(response.__dict__).encode("utf-8")
        self.request.sendall(response_body)
