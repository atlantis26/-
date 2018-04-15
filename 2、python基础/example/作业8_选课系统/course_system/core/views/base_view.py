# coding:utf-8
from conf.settings import AUTH_FLAG
from core.auth import auth, is_administrator
from core.orm import SomeError


class BaseView(object):
    def __init__(self, username, password, schools=list()):
        self.username = username
        self.password = password
        self.schools = schools

    def login(self, username, password):
        """登录"""
        if not username_is_exists(username):
            code = 400
            msg = u"账户{0}不存在,认证失败".format(account_name)
        else:
            resp = load_account(account_name)
            account = resp.data
            if account["password"] == password:
                code = 200
                msg = u"账户{0}成功登录，欢迎您使用本系统".format(account_name)
                AUTH_FLAG["is_authenticated"] = True
                AUTH_FLAG["is_administrator"] = account["is_administrator"]
                AUTH_FLAG["account_name"] = account_name
            else:
                code = 400
                msg = u"账户{0}的密码错误，认证失败".format(account_name)
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def logout():
        """登出"""
        msg = u"账户{0}成功登出系统，欢迎再次光临".format(AUTH_FLAG["account_name"])
        AUTH_FLAG["is_authenticated"] = False
        AUTH_FLAG["account_name"] = None
        AUTH_FLAG["is_administrator"] = False
        code = 200
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)




    def show_personal_info(self):
        pass

    def show_history(self):
        pass

    def reset_password(self):
        pass
