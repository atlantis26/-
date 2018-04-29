# coding:utf-8
from conf.settings import DB_Temp, Label_Byte_String
from datetime import datetime
import os
import json


class SocketMethods(object):
    @staticmethod
    def receive_data_by_action(conn):
        """接收数据并进行解析，与客户端协议约定请求交互为json数据，格式：
        {"action_id": "action_id", "kwargs":{"key1": "value1", "key2": "value2"} },
        对上传文件请求（action_id=5）做单独处理
        """
        data = conn.recv(1024)
        payload = str(data, encoding='utf-8')
        payload = json.loads(payload)
        action_id = payload["action_id"]
        kwargs = payload["kwargs"]
        if action_id == "5":
            temp_file_path = SocketMethods.receive_file_data(conn)
            kwargs["temp_file_path"] = temp_file_path

        return action_id, kwargs

    @staticmethod
    def receive_file_data(conn):
        """接受文件数据"""
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d_%H%M%S")
        temp_file = os.path.join(DB_Temp, "temp_file_{0}".format(time_stamp))
        SocketMethods.receive_file_by_label_string(conn, temp_file)
        return temp_file

    @staticmethod
    def receive_file_by_label_string(conn, file_path):
        """以标示字符串Label_Byte_String来判断文件内容是否接收完成"""
        with open(file_path, "wb") as f:
            while True:
                data = conn.recv(1024)
                if Label_Byte_String in data:
                    data = data.replace(Label_Byte_String, b"")
                    f.write(data)
                    f.flush()
                    break
                else:
                    f.write(data)
                    f.flush()

    @staticmethod
    def send_data_by_action(conn, action_id, response_obj):
        """发送请求响应数据,对下载文件请求（action_id=6）做单独处理，以标示字符串Label_Byte_String来标示文件内容发送完成"""
        response_body = bytes(json.dumps(response_obj.__dict__), encoding='utf-8')
        conn.sendall(response_body)
        if action_id == "6" and response_obj.code == 200:
            file_path = response_obj.data["file_path"]
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        conn.sendall(Label_Byte_String)
                        break
                    conn.sendall(data)


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
