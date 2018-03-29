# coding:utf-8
from atm.core.common import ResponseData
import logging

logger = logging.getLogger("atm.auth")


def account_sample(account_name, password, money=15000):
    """生成初始账户信息"""
    account = dict()
    account["account_name"] = account_name
    account["password"] = password
    account["money"] = money
    account["history"] = {}
    code = 200
    msg = u"新建账户{0}成功".format(account["name"])
    logger.debug(ResponseData(code, msg, account).__dict__)

    return ResponseData(code, msg, account)
