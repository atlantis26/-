
# coding:utf-8
from core.db_handler import load_account_pkl, save_account_pkl, save_flow_pkl, load_flow_pkl
from core.orm import ResponseData
from db.account_sample import account_sample, account_flow_sample
from conf.settings import DB_Accounts, DB_Flows_History
from datetime import datetime
import os
import json
import logging


logger = logging.getLogger("atm.accounts")


def create_account(account_name, password1, password2, balance=15000):
    """创建新账户"""
    if account_is_exists(account_name):
        code = 400
        msg = u"创建失败，账户{0}已存在".format(account_name)
    else:
        if password1 != password2:
            code = 400
            msg = u"创建失败，账户{0}的两次设置密码不一致".format(account_name)
        else:
            resp = account_sample(account_name, password1, balance)
            if resp.code == 200:
                resp = save_account_pkl(resp.data)
            code = resp.code
            msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def account_is_exists(name):
    """检测账户是否存在"""
    account_file = os.path.join(DB_Accounts, "{0}.pkl".format(name))
    if os.path.exists(account_file):
        return True


def settle_account(account, money, flag):
    """结算功能：
                flag=0：表示支出业务；
                flag=1：表示存入业务；
    """
    if flag == 0:
        if account.balance >= money:
            account.balance -= money
            save_account_pkl(account)
            code = 200
            msg = u"结算成功，账户{0}扣款支出{1}元，当前余额为：{2}元".format(account["name"], money, account["balance"])
        else:
            code = 400
            msg = u"结算失败，账户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["balance"])
    elif flag == 1:
        account.balance += money
        save_account_pkl(account)
        code = 200
        msg = u"结算成功，账户{0}存入{1}元,当前余额为：{2}元".format(account["name"], money, account["balance"])
    else:
        code = 400
        msg = u"暂不支持此结算方式"

    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def create_account_flow(account_name, action, details):
    """记录账户流水"""
    now = datetime.now()
    time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    rsp = account_flow_sample(time_stamp, account_name, action, details)
    if rsp.code == 200:
        flow = rsp.data
        save_flow_pkl(flow)
        code = 200
        msg = u"账户流水入库成功，流水详情：{0}".format(flow.__dict__)
    else:
        code = 400
        msg = u"账户流水入库失败，失败原因：{0}".format(rsp.msg)

    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def show_account_flow(account_name):
    """查询账户消费流水记录"""
    flow_list = list()
    account_flows_dir = os.path.join(DB_Flows_History, account_name)
    if os.path.exists(account_flows_dir):

    else:
        code = 400
        msg = u"查询失败，未找到账户{0}的消费流水记录".format(account_name)
    logger.debug(ResponseData(code, msg, flow_list).__dict__)

    return ResponseData(code, msg, flow_list)


def reset_account(account_name, password1, password2):
    """重置账户密码"""
    if not account_is_exists(account_name):
        code = 400
        msg = u"重置密码失败，账户{0}不存在".format(account_name)
    else:
        if password1 != password2:
            code = 400
            msg = u"重置密码失败，账户{0}的两次设置密码不一致".format(account_name)
        else:
            resp = load_account(account_name)
            if resp.code == 200:
                account = resp.data
                account["password"] = password1
                save_account(account)
                code = 200
                msg = u"账户{0}重置密码成功".format(account_name)
            else:
                code = resp.code
                msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)
