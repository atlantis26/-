# coding:utf-8
from atm.core.orm import ResponseData, Account
import logging

logger = logging.getLogger("atm.db")


def account_sample(name, password, balance=15000):
    """生成初始账户信息,默认信用额度为15000元"""
    account = Account(name, password, balance)
    code = 200
    msg = u"新建账户{0}的模型成功,初始账户信用额度为{1}元".format(account.name, account.balance)
    logger.debug(ResponseData(code, msg, account.__dict__).__dict__)

    return ResponseData(code, msg, account)


def account_flow_sample():
    """生成月消费流水记录"""
    pass
