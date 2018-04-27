# coding:utf-8
from core.orm import SomeError, ResponseData
import socket
import json
import os
import logging

logger = logging.getLogger("ftp.ftp_client")


class FtpClient(object):
    def __init__(self, host, port, username=None, password=None):
        self.client = socket.socket()
        self.client.connect((host, port))
        self.username = username
        self.password = password

    def _get_response(self, req_data):
        """发送请求，并获取响应"""
        data_json = bytes(json.dumps(req_data), encoding='utf-8')
        self.client.send(data_json)
        rsp = self.client.recv(1024)
        rsp = json.loads(str(rsp, encoding='utf-8'))
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
        except SomeError as e:
            code = 400
            msg = u"用户{0}注册失败，原因：{1}".format(username, str(e))
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
            msg = u"用户{0}登录失败，原因：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def logout(self):
        """用户登出"""
        try:
            data = dict()
            data["action_id"] = "3"
            # data["kwargs"] = {"username": self.username}
            data["kwargs"] = {}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            if rsp["code"] == 200:
                self.username = None
                self.password = None
        except SomeError as e:
            code = 400
            msg = u"用户{0}登出失败，原因：{1}".format(self.username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def show(self):
        """显示个人FTP仓库信息"""
        try:
            data = dict()
            data["action_id"] = "4"
            # data["kwargs"] = {"username": self.username}
            data["kwargs"] = {}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"用户{0}查询个人仓库文件失败, 原因：{1}".format(self.username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def upload(self, file_path):
        """上传文件到个人仓库"""
        try:
            file_name = os.path.split(file_path)[-1]
            req_body = dict()
            req_body["action_id"] = "5"
            req_body["kwargs"] = {"file_name": file_name}
            with open(file_path, "r") as f:
                data = f.read()
            req_body["kwargs"]["data"] = data.encode("utf-8")

            rsp = self._get_response(req_body)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"上传文件失败, 原因：{1}".format(self.username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def download(self, file_name, directory):
        """下载文件"""
        try:
            file_path = os.path.join(directory, file_name)
            req_body = dict()
            req_body["action_id"] = "6"
            req_body["kwargs"] = {"file_name": file_name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
            if code == 200:
                with open(file_path, "wb") as f:
                    f.write(rsp["data"])
                    f.flush()
        except SomeError as e:
            code = 400
            msg = u"下载文件失败, 原因：{1}".format(self.username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
