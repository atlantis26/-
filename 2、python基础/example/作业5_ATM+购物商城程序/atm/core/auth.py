# coding:utf-8
from atm.core.common import ResponseData
import logging

logger = logging.getLogger("atm.auth")


def auth(account):
    def new_auth(func):
        def deco(*args, **kwargs):
            if account["is_authenticated"]:
                # code = 200
                # msg = u"账户{0}认证成功,当前为登陆状态".format(account["detail"]["name"])
                return func(*args, **kwargs)
            else:
                code = 400
                msg = u"账户{0}认证失败，当前为未登陆状态".format(account["detail"]["name"])
                logger.debug(ResponseData(code, msg).__dict__)
                return ResponseData(code, msg)
        return deco
