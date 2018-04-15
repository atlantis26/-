# coding:utf-8
from core.orm import ResponseData
import logging

logger = logging.getLogger("atm.auth")


def auth(auth_flag):
    """判断是否是已登录状态"""
    def new_func(func):
        def deco(*args, **kwargs):
            if auth_flag["is_authenticated"]:
                code = 200
                msg = u"认证成功，用户{0}已成功登陆".format(auth_flag["account_name"])
                logger.debug(ResponseData(code, msg).__dict__)
                return func(*args, **kwargs)
            else:
                code = 400
                msg = u"认证失败，当前是未登录状态,请先登录用户"
                logger.debug(ResponseData(code, msg).__dict__)
                print(msg)
                return ResponseData(code, msg)
        return deco
    return new_func


def is_administrator(auth_flag):
    """判断是否是管理员身份"""
    def new_func(func):
        def deco(*args, **kwargs):
            if auth_flag["is_administrator"]:
                code = 200
                msg = u"认证成功，用户{0}是管理员身份".format(auth_flag["account_name"])
                logger.debug(ResponseData(code, msg).__dict__)
                return func(*args, **kwargs)
            else:
                code = 400
                msg = "认证失败，用户{0}不是管理员身份".format(auth_flag["account_name"])
                logger.debug(ResponseData(code, msg).__dict__)
                print(msg)
                return ResponseData(code, msg)
        return deco
    return new_func

