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
                msg = u"操作失败，当前是未登录状态,请先登录账户"
                logger.debug(ResponseData(code, msg).__dict__)
                print(msg)
                return ResponseData(code, msg)
        return deco
    return new_func


def is_administrator(auth_flag):
    def new_func(func):
        def deco(*args, **kwargs):
            if auth_flag["is_administrator"]:
                return func(*args, **kwargs)
            else:
                code = 400
                msg = "{0}不是管理员账户，不能登录本后台管理系统".format(auth_flag["account_name"])
                print(msg)
                return ResponseData(code, msg)
        return deco
    return new_func

