# coding:utf-8

from core.orm import ResponseData
import logging

logger = logging.getLogger("system.auth")


def auth(auth_flag):
    """判断是否是已登录状态"""
    def new_func(func):
        def deco(*args, **kwargs):
            if auth_flag["is_authenticated"]:
                code = 200
                msg = u"认证成功，用户{0}已成功登陆".format(auth_flag["username"])
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
