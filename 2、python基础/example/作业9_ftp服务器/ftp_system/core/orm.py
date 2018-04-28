# coding:utf-8
from conf.settings import DB_Temp
from datetime import datetime
import socket
import os
import json


class SocketServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)

    @staticmethod
    def receive(conn):
        """接收数据并进行解析，约定与客户端交互的json数据格式：
        {"action_id": "action_id", "kwargs":{"key1": "value1", "key2": "value2"} }
        """
        data = conn.recv(1024)
        payload = str(data, encoding='utf-8')
        payload = json.loads(payload)
        action_id = payload["action_id"]
        kwargs = payload["kwargs"]
        if action_id == "5":
            file_size = kwargs["file_size"]
            temp_file_path = SocketServer.receive_file_data(conn, file_size)
            kwargs["temp_file_path"] = temp_file_path
        if action_id == "6":
            kwargs["socket_conn"] = conn

        return action_id, kwargs

    @staticmethod
    def receive_file_data(conn, file_size):
        """接受文件数据，并存储在临时文件内，返回临时文件的路径地址"""
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d_%H%M%S")
        temp_file = os.path.join(DB_Temp, "temp_file_{0}".format(time_stamp))
        with open(temp_file, "wb") as f:
            while file_size > 0:
                if file_size <= 1024:
                    data = conn.recv(1024)
                    f.write(data)
                    break
                elif file_size > 1024:
                    data = conn.recv(1024)
                    f.write(data)
                    file_size -= 1024
        return temp_file

    @staticmethod
    def send_file_data(conn, file_path):
        """发送文件数据"""
        with open(file_path, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                conn.sendall(data)

    def __del__(self):
        """关闭连接"""
        self.server.close()


class User(object):
    """用户orm模型"""
    def __init__(self, username, password):
        self.username = username
        self.password = password


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    """自定义异常错误"""
    pass
