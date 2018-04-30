# coding:utf-8
from core.orm import SocketMethods
from core.orm import SomeError, ResponseData
from conf.settings import Label_Byte_String
import socket
import json
import os
import logging

logger = logging.getLogger("ftp.ftp_client")


class FtpClient(object):
    def __init__(self, host, port):
        self.client = socket.socket()
        self.client.connect((host, port))
        self.username = None
        self.password = None

    def _get_response(self, req_data):
        """不带文件内容的请求，发送请求，并获取响应"""
        data_json = bytes(json.dumps(req_data), encoding='utf-8')
        self.client.send(data_json)
        rsp = self.client.recv(1024)
        rsp = json.loads(str(rsp, encoding='utf-8'))
        return rsp

    def _get_upload_file_response(self, req_data, file_path):
        """对于上传文件的请求，发送两次请求数据，第一次告诉服务端文件名称，第二次连续发送文件数据直到全部发送完成
        """
        data_json = bytes(json.dumps(req_data), encoding='utf-8')
        self.client.send(data_json)
        # 发送文件内容，并接收服务端响应
        with open(file_path, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    self.client.send(Label_Byte_String)
                    break
                self.client.send(file_data)
        rsp = self.client.recv(1024)
        rsp = json.loads(str(rsp, encoding='utf-8'))
        return rsp

    def _get_download_file_response(self, req_data, directory):
        """对于下载文件的请求，接收两次请求数据，第一次获得服务端文件名称，第二次连续接收文件数据直到完成
        """
        file_name = req_data["kwargs"]["file_name"]
        file_path = os.path.join(directory, file_name)
        data_json = bytes(json.dumps(req_data), encoding='utf-8')
        self.client.send(data_json)
        # 发送文件内容，并接收服务端响应
        rsp = self.client.recv(1024)
        rsp = json.loads(str(rsp, encoding="utf-8"))
        if rsp["code"] == 200:
            SocketMethods.receive_file_by_label_string(self.client, file_path)
        return rsp

    def register(self, username, password1, password2):
        """注册用户"""
        try:
            data = dict()
            data["action_id"] = "1"
            data["kwargs"] = {"username": username,
                              "password1": password1,
                              "password2": password2}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            data = rsp["data"] if code == 200 else None
        except SomeError as e:
            code = 400
            msg = u"注册用户失败，原因：{1}".format(username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def login(self, username, password):
        """用户登录"""
        try:
            data = dict()
            data["action_id"] = "2"
            data["kwargs"] = {"username": username,
                              "password": password}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            self.username = username
            self.password = password
        except SomeError as e:
            code = 400
            msg = u"登录失败，原因：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def logout(self):
        """用户登出"""
        try:
            data = dict()
            data["action_id"] = "3"
            data["kwargs"] = {}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            if rsp["code"] == 200:
                self.username = None
                self.password = None
        except SomeError as e:
            code = 400
            msg = u"登出失败，原因：{1}".format(self.username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def show(self):
        """显示个人FTP仓库信息"""
        try:
            req_body = dict()
            req_body["action_id"] = "4"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            code = rsp["code"]
            msg = rsp["msg"]
            data = rsp["data"] if code == 200 else None
        except SomeError as e:
            code = 400
            msg = u"查询个人文件列表失败, 原因：{0}".format(self.username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def upload(self, file_path):
        """上传文件到个人仓库"""
        try:
            if not os.path.exists(file_path):
                raise SomeError(u"文件{0}不存在".format(file_path))
            file_name = os.path.split(file_path)[-1]
            req_body = dict()
            req_body["action_id"] = "5"
            req_body["kwargs"] = {"file_name": file_name}
            rsp = self._get_upload_file_response(req_body, file_path)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"上传文件失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def download(self, file_name, directory):
        """下载文件"""
        try:
            if not os.path.exists(directory):
                raise SomeError(u"存放文件的目录{0}不存在".format(directory))
            req_body = dict()
            req_body["action_id"] = "6"
            req_body["kwargs"] = {"file_name": file_name}
            rsp = self._get_download_file_response(req_body, directory)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"下载文件失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
