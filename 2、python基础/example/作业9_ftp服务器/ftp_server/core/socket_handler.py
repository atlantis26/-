# coding:utf-8
from core.users import UserManager
from core.orm import SomeError, ResponseData
from core.auth import auth
from conf.settings import AUTH_FLAG, DB_Storage
import socket
import os
import logging

logger = logging.getLogger("system.users")


class SocketServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.session, self.address = self.server.accept()

    def receive(self):
        """接收数据"""
        data = self.session.recv(1024)
        return data

    def send(self, data):
        """发送数据"""
        self.session.sendall(data)

    def close(self):
        """关闭连接"""
        self.server.close()


class FtpServer(object):
    """FTP服务器"""
    def __init__(self):
        self.username = None
        self.password = None

    @classmethod
    def __create_user_home(cls, username):
        """创建个人仓库"""
        user_home = os.path.join(DB_Storage, username)
        os.mkdir(user_home)

    @classmethod
    def register(cls, username, password1, password2):
        """注册用户"""
        try:
            user = UserManager.create_user(username, password1, password2)
            cls.__create_user_home(username)
            code = 200
            msg = u"用户{0}注册成功".format(username)
            data = user.__dict__
        except SomeError as e:
            code = 400
            msg = u"用户{0}注册失败，原因：{1}".format(username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @classmethod
    def login(cls, username, password):
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
            UserManager.logout()
            code = 200
            msg = u"用户{0}成功登出，欢迎您再次使用本系统".format(AUTH_FLAG["username"])
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
            user_home = os.path.join(DB_Storage, self.username)
            for root, dirs, files in os.walk(user_home):
                data = files
            code = 200
            msg = u"用户{0}查询个人仓库文件成功".format(self.username)
        except SomeError as e:
            code = 400
            msg = u"用户{0}查询个人仓库文件失败, 原因：{1}".format(self.username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def upload(self):
        """上传文件到个人仓库"""
        pass

    @auth(AUTH_FLAG)
    def download(self):
        """下载文件"""
        pass
