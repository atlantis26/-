# coding:utf-8
from atm.core.common import ResponseData
import logging

logger = logging.getLogger("atm.auth")


def account_sample(name, password, money=15000):
    """生成初始账户信息"""
    account = dict()
    account["name"] = name
    account["password"] = password
    account["money"] = money
    account["is_frozen"] = False
    account["history"] = {}
    code = 200
    msg = u"新建账户{0}成功,初始账户信用额度为{1}元".format(account["name"], account["money"])
    logger.debug(ResponseData(code, msg, account).__dict__)

    return ResponseData(code, msg, account)
