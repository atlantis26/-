# coding:utf-8
from socketserver import BaseRequestHandler
from core.command_handler import FtpCommands
from core.user_handler import UserHandler
from core.orm import SomeError
from conf.settings import DB_TEMP
from datetime import datetime
import json
import os


class FtpHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.username = None
        self.user_handler = UserHandler()
        self.ftp_commands = FtpCommands()
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
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
                self.sendall_data(cmd, response)
        except (ConnectionResetError, SomeError) as e:
            msg = u"客户端{0}已经断开连接，详细：{1}".format(self.client_address, str(e))
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
        return temp_file

    def sendall_data(self, cmd, response):
        """发送请求响应数据,对下载文件请求（cmd=get）做单独处理"""
        response_body = json.dumps(response.__dict__).encode("utf-8")
        self.request.sendall(response_body)
        if cmd == "get" and response.code == 200:
            file_path = response.data.pop("file_path")
            seek_size = response.data.get("seek_size")
            with open(file_path, "rb") as f:
                f.seek(seek_size)
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.request.sendall(data)
