# coding:utf-8
from core.orm import ResponseData, User, Flow
import logging

logger = logging.getLogger("atm.db")


def user_sample(name, password, balance, is_administrator=False):
    """生成初始用户信息"""
    user = User(name, password, balance, is_administrator)
    code = 200
    msg = u"新建用户模型成功,初始用户的账户余额为{0}元".format(user.name, user.balance)
    logger.debug(ResponseData(code, msg, user.__dict__).__dict__)

    return ResponseData(code, msg, user)


def user_flow_sample(time_stamp, username, action, details):
    """生成用户消费流水信息记录"""
    flow = Flow(time_stamp, username, action, details)
    code = 200
    msg = u"新建消费流水模型成功,详情：{0}".format(flow.__dict__)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg, flow)
