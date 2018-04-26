# coding:utf-8
from core.orm import SocketServer, SomeError, ResponseData
import json
import os
import logging

logger = logging.getLogger("ftp.client")


class FtpClient(SocketServer):
    def __init__(self, host, port, username=None, password=None):
        SocketServer.__init__(self, host, port)
        self.username = username
        self.password = password

    def console(self):
        while True:
            action_id, kwargs = self.receive()
            actions = {"1": self.register,
                       "2": self.login,
                       "3": self.logout,
                       "4": self.show,
                       "5": self.upload,
                       "6": self.download}
            actions[action_id](**kwargs)

    def _get_response(self, req_data):
        data_json = json.dumps(req_data)
        self.sendall(data_json)
        return self.receive()

    def register(self, username, password1, password2):
        """注册用户"""
        try:
            data = dict()
            data["action_id"] = "1"
            data["kwargs"] = {"username": username,
                              "password1": password1,
                              "password2": password2}
            rsp = self._get_response(data)
            logger.debug(rsp)
            code = 200
            msg = u"用户{0}注册成功".format(username)
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
            logger.debug(rsp)

            self.username = username
            self.password = password
            code = 200
            msg = u"用户{0}成功登录，欢迎您使用本系统".format(username)
        except SomeError as e:
            code = 400
            msg = u"用户{0}登录失败，原因：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def logout(self, username):
        """用户登出"""
        try:
            data = dict()
            data["action_id"] = "3"
            data["kwargs"] = {"username": username}
            rsp = self._get_response(data)
            logger.debug(rsp)

            self.username = None
            self.password = None
            code = 200
            msg = u"用户{0}成功登出，欢迎您再次使用本系统".format(self.username)
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
            data["kwargs"] = {"username": self.username}
            rsp = self._get_response(data)
            logger.debug(rsp)
            code = 200
            msg = u"用户{0}查询个人仓库文件成功".format(self.username)
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
            with open(file_path, "rb") as f:
                data = f.read()
            req_body["kwargs"]["data"] = data

            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = 200
            msg = u"上传文件成功".format(self.username)
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
            data = rsp.data
            with open(file_path, "wb") as f:
                f.write(data)
                f.flush()
            code = 200
            msg = u"下载文件成功".format(self.username)
        except SomeError as e:
            code = 400
            msg = u"下载文件失败, 原因：{1}".format(self.username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)
