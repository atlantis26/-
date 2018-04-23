# coding:utf-8
from core.users import user_is_exists
from core.db_handler import load_user_pkl
from conf.settings import AUTH_FLAG
from core.auth import auth
from core.orm import SomeError, ResponseData
import logging

logger = logging.getLogger("system.base_view")


class BaseView(object):
    def __init__(self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id
        self.login()

    def validate_role(self, user):
        """验证登录用户账号是否符合角色身份"""
        roles = {"1": u"学员", "2": u"讲师", "3": u"管理员"}
        if user.role != roles[self.role_id]:
            raise SomeError(u"登录用户的身份不相符，请核对后再试")
        return roles[self.role_id]

    def login(self):
        """登录"""
        if not user_is_exists(self.username):
            raise SomeError(u"用户{0}不存在,登录失败".format(self.username))
        else:
            user = load_user_pkl(self.username)
            role = self.validate_role(user)
            if user.password == self.password:
                code = 200
                msg = u"{0}{1}成功登录，欢迎您使用本系统".format(role, self.username)
                AUTH_FLAG["is_authenticated"] = True
                AUTH_FLAG["username"] = self.username
            else:
                code = 400
                msg = u"用户{0}的密码错误，登录失败".format(self.username)
        logger.debug(ResponseData(code, msg).__dict__)
        print(msg)
        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def logout(self):
        """登出"""
        msg = u"成功登出系统，欢迎再次光临"
        AUTH_FLAG["is_authenticated"] = False
        AUTH_FLAG["username"] = None
        code = 200
        logger.debug(ResponseData(code, msg).__dict__)
        raise SomeError(msg)
