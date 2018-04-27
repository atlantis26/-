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

    @staticmethod
    def receive(conn):
        """接收数据并进行解析，约定与客户端交互的json数据格式：
        {"action_id": "action_id", "kwargs":{"key1": "value1", "key2": "value2"} }
        """
        data = conn.recv(1024)
        receive_strings = str(data, encoding='utf-8')
        payload = json.loads(receive_strings)
        action_id = payload["action_id"]
        kwargs = payload["kwargs"]

        return action_id, kwargs

    @staticmethod
    def sendall(conn, data):
        """发送数据"""
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
