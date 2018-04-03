# coding:utf-8
from atm.core.orm import ResponseData
import logging

logger = logging.getLogger("atm.auth")


def auth(auth_flag):
    def new_func(func):
        def deco(*args, **kwargs):
            if auth_flag["is_authenticated"]:
                return func(*args, **kwargs)
            else:
                code = 400
                msg = u"账户{0}认证失败，当前为未登陆状态".format(auth_flag["account_name"])
                logger.debug(ResponseData(code, msg).__dict__)
                return ResponseData(code, msg)
        return deco
    return new_func
