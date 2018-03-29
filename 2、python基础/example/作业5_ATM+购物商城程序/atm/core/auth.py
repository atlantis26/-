# coding:utf-8
from atm.core.common import ResponseData
from atm.conf.settings import PROJECT_DIR
import os
import json
import logging

logger = logging.getLogger("atm.auth")


def auth(func):
    def deco(*args, **kwargs):
        account_name = input(u"请输入账号: ")
        password = input(u"请输入密码: ")
        account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account_name))
        if not os.path.exists(account_file):
            code = 400
            msg = u"账户{0}不存在,认证失败".format(account_name)
        else:
            with open(account_file) as f:
                account = json.loads(f.read().strip())
            if account["password"] == password:
                code = 200
                msg = u"账户{0}的密码正确，认证成功".format(account_name)
                logger.debug(ResponseData(code, msg).__dict__)
                return func(*args, **kwargs)
            else:
                code = 400
                msg = u"账户{0}的密码错误，认证失败".format(account_name)
        logger.debug(ResponseData(code, msg).__dict__)
        return ResponseData(code, msg)
    return deco
