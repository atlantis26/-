# coding:utf-8
from conf.settings import DB_Users, DB_STORAGE
from core.orm import User, SomeError, ResponseData
import json
import os
import logging


logger = logging.getLogger("ftp.users")


class UserHandler(object):
    def __init__(self):
        self.username = None
        self.is_authenticated = False

    def register(self, username, password1, password2, quota):
        """创建新用户"""
        try:
            if self.user_is_exists(username):
                raise SomeError(u"用户名{0}已被使用".format(username))
            if password1 != password2:
                raise SomeError(u"两次设置密码不一致".format(username))
            user = User(username, password1, quota)
            self.save_user(user)
            self.create_or_get_user_home(username)
            code = 200
            msg = u"创建用户成功"
            data = user.__dict__
        except SomeError as e:
            code = 400
            msg = u"创建用户失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def login(self, username, password):
        """登录"""
        try:
            if not UserHandler.user_is_exists(username):
                raise SomeError(u"用户不存在")
            user = UserHandler.load_user(username)
            if user["password"] != password:
                raise SomeError(u"密码错误")
            code = 200
            msg = u"用户{0}登录成功, 欢迎您使用本系统, 使用'help'命令了解更多系统操作命令""".format(username)
            self.username = username
            self.is_authenticated = True
        except SomeError as e:
            code = 400
            msg = u"用户{0}登录失败，详情：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def logout(self):
        """登出"""
        try:
            if self.is_authenticated is False:
                raise SomeError(u"当前是未登录状态，请核对后再尝试")
            code = 200
            msg = u"用户{0}登出系统成功，欢迎再次光临".format(self.username)
            self.is_authenticated = False
            self.username = None
        except SomeError as e:
            code = 400
            msg = u"用户{0}登出系统失败，详情：{1}".format(self.username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def user_is_exists(username):
        """检测用户是否存在"""
        user_file = os.path.join(DB_Users, "{0}.json".format(username))
        if os.path.exists(user_file):
            return True

    @staticmethod
    def load_user(username):
        """加载用户数据"""
        user_file = os.path.join(DB_Users, "{0}.json".format(username))
        if not os.path.exists(user_file):
            raise SomeError(u"用户{0}不存在，加载数据失败".format(username))
        with open(user_file, "r") as f:
            user = json.loads(f.read().strip())

        return user

    @staticmethod
    def save_user(user):
        """保存用户数据，写入到存储文件"""
        user_json = json.dumps(user.__dict__)
        user_file = os.path.join(DB_Users, "{0}.json".format(user.username))
        with open(user_file, "w") as f:
            f.write(user_json)
            f.flush()

    @staticmethod
    def create_or_get_user_home(username):
        """创建或者获取个人仓库目录路径"""
        user_home = os.path.join(DB_STORAGE, username)
        if not os.path.exists(user_home):
            os.mkdir(user_home)
        return user_home
