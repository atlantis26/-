# coding:utf-8
from core.orm import SocketMethods, SomeError, ResponseData
from core.users import UserManager
from conf.settings import AUTH_FLAG
from core.auth import auth
import socket
import shutil
import os
import logging

logger = logging.getLogger("ftp.ftp_server")


class FtpServer(object):
    """FTP服务器"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)

    def console(self):
        while True:
            conn, address = self.server.accept()
            try:
                while True:
                    action_id, kwargs = SocketMethods.receive_data_by_action(conn)
                    actions = {"1": self.register,
                               "2": self.login,
                               "3": self.logout,
                               "4": self.show,
                               "5": self.upload,
                               "6": self.download}
                    rsp = actions[action_id](**kwargs)
                    SocketMethods.send_data_by_action(conn, action_id, rsp)
            except Exception as e:
                msg = u"远程客户端连接实例({0},{1})意外断开，详细：{2}".format(conn, address, str(e))
                print(msg)
                logger.debug(msg)

    @staticmethod
    def register(username, password1, password2):
        """注册用户"""
        try:
            data = UserManager.create_user(username, password1, password2)
            UserManager.create_or_get_user_home(username)
            code = 200
            msg = u"注册用户{0}成功".format(username)
            data = data.__dict__
        except SomeError as e:
            code = 400
            msg = u"注册用户{0}失败，原因：{1}".format(username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def login(username, password):
        """用户登录"""
        try:
            UserManager.login(username, password)
            code = 200
            msg = u"登录成功，欢迎用户{0}使用本系统".format(username)
        except SomeError as e:
            code = 400
            msg = u"登录失败，原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def logout(self):
        """用户登出"""
        try:
            msg = u"登出成功，欢迎用户{0}再次使用本系统".format(AUTH_FLAG["username"])
            UserManager.logout()
            code = 200
        except SomeError as e:
            code = 400
            msg = u"登出失败，原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def show(self):
        """查询个人文件列表"""
        try:
            data = list()
            user_home = UserManager.create_or_get_user_home(AUTH_FLAG["username"])
            if not user_home:
                raise SomeError(u"用户的ftp文件仓库不存在，请联系管理员")
            for root, dirs, files in os.walk(user_home):
                data = files
            code = 200
            msg = u"查询个人文件列表成功"
        except SomeError as e:
            code = 400
            msg = u"查询个人文件列表失败, 原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def upload(self, file_name, temp_file_path):
        """上传文件到个人仓库"""
        try:
            user_home = UserManager.create_or_get_user_home(AUTH_FLAG["username"])
            file_path = os.path.join(user_home, file_name)
            shutil.move(temp_file_path, file_path)
            code = 200
            msg = u"上传文件成功"
        except SomeError as e:
            code = 400
            msg = u"上传文件失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def download(self, file_name):
        """下载文件"""
        try:
            user_home = UserManager.create_or_get_user_home(AUTH_FLAG["username"])
            file_path = os.path.join(user_home, file_name)
            if not os.path.exists(file_path):
                raise SomeError(u"文件{0}不存在".format(file_name))
            data = {"file_name": file_name,
                    "file_path": file_path}
            code = 200
            msg = u"下载文件成功"
        except SomeError as e:
            code = 400
            msg = u"下载文件失败, 原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg, data)
