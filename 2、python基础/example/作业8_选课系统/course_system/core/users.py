
# coding:utf-8
from core.db_handler import load_user_pkl, save_user_pkl, save_flow_pkl, load_flow_pkl
from core.orm import ResponseData
from db.user_sample import user_sample, user_flow_sample
from conf.settings import DB_Users, DB_Flows_History
from datetime import datetime
import os
import logging


logger = logging.getLogger("atm.users")


def create_user(username, password1, password2, balance=0):
    """创建新用户"""
    if user_is_exists(username):
        code = 400
        msg = u"创建失败，用户{0}已存在".format(username)
    else:
        if password1 != password2:
            code = 400
            msg = u"创建失败，用户{0}的两次设置密码不一致".format(username)
        else:
            resp = user_sample(username, password1, balance)
            if resp.code == 200:
                resp = save_user_pkl(resp.data)
            code = resp.code
            msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def user_is_exists(name):
    """检测用户是否存在"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(name))
    if os.path.exists(user_file):
        return True


def settle_user(user, money, flag):
    """结算功能：
                flag=0：表示支出业务；
                flag=1：表示存入业务；
    """
    if flag == 0:
        if user.balance >= money:
            user.balance -= money
            save_user_pkl(user)
            code = 200
            msg = u"结算成功，用户{0}扣款支出{1}元，当前余额为：{2}元".format(user["name"], money, user["balance"])
        else:
            code = 400
            msg = u"结算失败，用户{0}的余额不足，当前余额为：{1}元".format(user["name"], user["balance"])
    elif flag == 1:
        user.balance += money
        save_user_pkl(user)
        code = 200
        msg = u"结算成功，用户{0}存入{1}元,当前余额为：{2}元".format(user["name"], money, user["balance"])
    else:
        code = 400
        msg = u"暂不支持此结算方式"

    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def create_user_flow(username, action, details):
    """记录用户流水"""
    now = datetime.now()
    time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    rsp = user_flow_sample(time_stamp, username, action, details)
    if rsp.code == 200:
        flow = rsp.data
        save_flow_pkl(flow)
        code = 200
        msg = u"用户流水入库成功，流水详情：{0}".format(flow.__dict__)
    else:
        code = 400
        msg = u"用户流水入库失败，失败原因：{0}".format(rsp.msg)

    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def show_user_flow(username):
    """查询用户消费流水记录"""

    # flow_list = load_flow_pkl(username)
    #
    #
    # logger.debug(ResponseData(code, msg, flow_list).__dict__)
    #
    # return ResponseData(code, msg, flow_list)
    pass
