# coding:utf-8
from core.orm import SocketServer, SomeError, ResponseData
from core.users import UserManager
from core.auth import auth
from conf.settings import AUTH_FLAG, DB_Storage
import json
import os
import logging

logger = logging.getLogger("ftp.ftp_server")


class FtpServer(SocketServer):
    """FTP服务器"""
    def __init__(self, host, port):
        SocketServer.__init__(self, host, port)

    def console(self):
        while True:
            conn, address = self.server.accept()
            while True:
                action_id, kwargs = self.receive(conn)
                actions = {"1": self.register,
                           "2": self.login,
                           "3": self.logout,
                           "4": self.show,
                           "5": self.upload,
                           "6": self.download}
                rsp = actions[action_id](**kwargs)
                rsp = bytes(json.dumps(rsp.__dict__), encoding="utf-8")
                conn.sendall(rsp)

    @staticmethod
    def register(username, password1, password2):
        """注册用户"""
        try:
            data = UserManager.create_user(username, password1, password2)
            FtpServer._create_user_home(username)
            code = 200
            msg = u"用户{0}注册成功".format(username)
            data = data.__dict__
        except SomeError as e:
            code = 400
            msg = u"用户{0}注册失败，原因：{1}".format(username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def _create_user_home(username):
        """创建个人仓库"""
        user_home = os.path.join(DB_Storage, username)
        os.mkdir(user_home)

    @property
    def _get_user_home(self):
        user_home = os.path.join(DB_Storage, AUTH_FLAG["username"])
        if not os.path.exists(user_home):
            os.mkdir(user_home)
        return user_home

    @staticmethod
    def login(username, password):
        """用户登录"""
        try:
            UserManager.login(username, password)
            code = 200
            msg = u"用户{0}成功登录，欢迎您使用本系统".format(username)
        except SomeError as e:
            code = 400
            msg = u"用户{0}登录失败，原因：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def logout(self):
        """用户登出"""
        try:
            msg = u"用户{0}成功登出，欢迎您再次使用本系统".format(AUTH_FLAG["username"])
            UserManager.logout()
            code = 200
        except SomeError as e:
            code = 400
            msg = u"用户{0}登出失败，原因：{1}".format(AUTH_FLAG["username"], str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def show(self):
        """显示个人FTP仓库信息"""
        try:
            data = list()
            user_home = os.path.join(DB_Storage, AUTH_FLAG["username"])
            if not user_home:
                raise SomeError(u"用户个人仓库不存在")
            for root, dirs, files in os.walk(user_home):
                data = files
            code = 200
            msg = u"用户{0}查询个人仓库文件成功".format(AUTH_FLAG["username"])
        except SomeError as e:
            code = 400
            msg = u"用户{0}查询个人仓库文件失败, 原因：{1}".format(AUTH_FLAG["username"], str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def upload(self, file_name, data):
        """上传文件到个人仓库"""
        try:
            file_path = os.path.join(self._get_user_home, file_name)
            with open(file_path, "wb") as f:
                f.write(data)
                f.flush()
            code = 200
            msg = u"用户{0}上传文件成功".format(AUTH_FLAG["username"])
        except SomeError as e:
            code = 400
            msg = u"用户{0}上传文件失败, 原因：{1}".format(AUTH_FLAG["username"], str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def download(self, file_name):
        """下载文件"""
        try:
            file_path = os.path.join(self._get_user_home, file_name)
            with open(file_path, "rb") as f:
                data = f.read()
            code = 200
            msg = u"用户{0}下载文件成功".format(AUTH_FLAG["username"])
        except SomeError as e:
            code = 400
            msg = u"用户{0}下载文件失败, 原因：{1}".format(AUTH_FLAG["username"], str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)
