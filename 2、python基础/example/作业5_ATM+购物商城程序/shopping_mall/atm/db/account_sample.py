# coding:utf-8
from atm.core.orm import ResponseData, Account, Flow
import logging

logger = logging.getLogger("atm.db")


def account_sample(name, password, balance, is_administrator=False):
    """生成初始账户信息"""
    account = Account(name, password, balance, is_administrator)
    code = 200
    msg = u"新建账户模型成功,账户{0}信用额度为{1}元".format(account.name, account.balance)
    logger.debug(ResponseData(code, msg, account.__dict__).__dict__)

    return ResponseData(code, msg, account)


def account_flow_sample(time_stamp, account_name, action, details):
    """生成账户消费流水信息记录"""
    flow = Flow(time_stamp, account_name, action, details)
    code = 200
    msg = u"新建消费流水模型成功,详情：{0}".format(flow.__dict__)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg, flow)
