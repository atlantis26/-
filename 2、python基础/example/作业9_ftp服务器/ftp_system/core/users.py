# coding:utf-8
from core.orm import User, SomeError
from conf.settings import AUTH_FLAG
from conf.settings import DB_Users
import json
import os
import logging


logger = logging.getLogger("ftp.users")


class UserManager(object):
    @staticmethod
    def login(username, password):
        """登录"""
        if not UserManager.user_is_exists(username):
            raise SomeError(u"用户{0}不存在".format(username))
        user = UserManager.load_user(username)
        if user["password"] != password:
            raise SomeError(u"用户{0}的密码错误".format(username))
        AUTH_FLAG["is_authenticated"] = True
        AUTH_FLAG["username"] = username

        return u"用户{0}成功登录，欢迎您使用本系统".format(username)

    @staticmethod
    def logout():
        """登出"""
        AUTH_FLAG["is_authenticated"] = False
        AUTH_FLAG["username"] = None

        return u"用户{0}成功登出系统，欢迎再次光临".format(AUTH_FLAG["username"])

    @staticmethod
    def create_user(username, password1, password2):
        """创建新用户"""
        if UserManager.user_is_exists(username):
            raise SomeError(u"用户名{0}已被使用".format(username))
        if password1 != password2:
            raise SomeError(u"两次设置密码不一致".format(username))
        user = User(username, password1)
        UserManager.save_user(user)
        return user

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
