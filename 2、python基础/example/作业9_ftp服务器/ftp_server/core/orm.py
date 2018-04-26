# coding:utf-8
import socket
import json


class SocketServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.session, self.address = self.server.accept()

    def receive(self):
        """接收数据并解析，约定与客户端交互的json数据格式：
        {"action_id": "id", "kwargs":{"key1": "value1", "key2": "value2"} }
        """
        action_json = ""
        while True:
            data = self.session.recv(1024).encode("utf-8")
            if data == "":
                break
            action_json += data
        action_info = json.loads(action_json)
        action_id = action_info["action_id"]
        action_kwargs = action_info["kwargs"]

        return action_id, action_kwargs

    def sendall(self, data):
        """发送数据"""
        self.session.sendall(data)

    def close(self):
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
