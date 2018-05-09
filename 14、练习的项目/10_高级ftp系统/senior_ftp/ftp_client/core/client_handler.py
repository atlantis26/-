# coding:utf-8
from core.orm import SomeError, ResponseData
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
        data_json = json.dumps(req_data).encode("utf-8")
        self.client.send(data_json)
        rsp = self.client.recv(1024)
        rsp = json.loads(rsp.decode("utf-8"))
        return rsp

    def _get_upload_file_response(self, req_data, file_path):
        """对于上传文件的请求，发送两次请求数据，第一次告诉服务端文件名称，第二次连续发送文件数据直到全部发送完成
        """
        data_json = json.dumps(req_data).encode('utf-8')
        self.client.send(data_json)
        # 发送文件内容，并接收服务端响应
        with open(file_path, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                self.client.send(file_data)
        rsp = self.client.recv(1024)
        rsp = json.loads(rsp.decode("utf-8"))
        return rsp

    def _get_download_file_response(self, req_data, directory):
        """对于下载文件的请求，接收两次请求数据，第一次获得服务端文件名称，第二次连续接收文件数据直到完成
        """
        file_name = req_data["kwargs"]["file_name"]
        file_path = os.path.join(directory, file_name)
        data_json = json.dumps(req_data).encode("utf-8")
        self.client.send(data_json)
        # 发送文件内容，并接收服务端响应
        rsp = self.client.recv(1024)
        rsp = json.loads(rsp.decode("utf-8"))
        if rsp["code"] == 200:
            file_size = rsp["data"]["file_size"]
            self._receive_file_data(file_size, file_path)
        return rsp

    def _receive_file_data(self, file_size, file_path):
        """根据文件size大小接收文件数据"""
        receive_size = 0
        f = open(file_path, "wb")
        while True:
            diff = file_size - receive_size
            if diff > 1024:
                data = self.client.recv(1024)
            elif diff == 0:
                f.close()
                break
            else:
                data = self.client.recv(diff)
            f.write(data)
            f.flush()
            receive_size += len(data)

    def run_cmd(self):
        pass

    def register(self, username, password1, password2, quota):
        """注册用户"""
        try:
            data = dict()
            data["cmd"] = "register"
            data["kwargs"] = {"username": username,
                              "password1": password1,
                              "password2": password2,
                              "quota": quota}
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
            data["cmd"] = "login"
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
            data["cmd"] = "logout"
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

    def put(self, file_path):
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

    def get(self, file_name, directory):
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

    def mkdir(self, name):
        """创建目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "mkdir"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"创建目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def rmdir(self, name):
        """删除目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "rmdir"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"删除目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cd(self, name):
        """切换目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "cd"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"切换目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def ls(self):
        """查询用户当前路径下文件目录信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "ls"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"查询当前路径下文件目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def pwd(self):
        """查询用户当前路径"""
        try:
            req_body = dict()
            req_body["cmd"] = "pwd"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"查询当前路径, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def quota(self):
        """查询用户存储配额信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "quota"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"查询用户存储配额信息, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def help(self):
        """查询命令列表，及命令使用信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "quota"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"查询命令相关信息失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
