# coding:utf-8
from atm.core.orm import ResponseData, Flow
from atm.conf.settings import PROJECT_DIR
from datetime import datetime
import os
import json
import logging


logger = logging.getLogger("atm.accounts")


def load_account(name):
    """加载账户数据"""
    account_file = os.path.join(PROJECT_DIR, "db", "accounts", "{0}.json".format(name))
    if not os.path.exists(account_file):
        code = 400
        msg = u"账户{0}不存在，加载数据失败".format(name)
        data = None
    else:
        with open(account_file, "r") as f:
            data = json.loads(f.read().strip())
        code = 200
        msg = "账户{0}的数据加载成功".format(name)
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)


def save_account(account):
    """保存账户数据，写入到存储文件"""
    account_file = os.path.join(PROJECT_DIR, "db", "accounts", "{0}.json".format(account["name"]))
    account_json = json.dumps(account)
    with open(account_file, "r+") as f:
        f.write(account_json)
        f.flush()
    code = 200
    msg = u"账户{0}信息保存成功".format(account["name"])
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def account_is_exists(name):
    """检测账户是否存在"""
    account_file = os.path.join(PROJECT_DIR, "db", "accounts", "{0}.json".format(name))
    if os.path.exists(account_file):
        return True


def settle_account(account, money, flag=0):
    """结算功能：
                flag=0：表示付款业务；
                flag=1：表示取现业务，取现收取5%手续费；
                flag=2：表示还款业务；
    """
    if flag == 0:
        if account["balance"] >= money:
            account["balance"] -= money
            save_account(account)
            code = 200
            msg = u"结算成功，用户{0}当前信用余额为：{1}元".format(account["name"], account["balance"])
        else:
            code = 400
            msg = u"结算失败，用户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["balance"])
    elif flag == 1:
        money = float(money) * (1 + 0.05)
        if account["balance"] >= money:
            account["balance"] -= money
            save_account(account)
            code = 200
            msg = u"结算成功，用户{0}当前信用余额为：{1}元".format(account["name"], account["balance"])
        else:
            code = 400
            msg = u"结算失败，用户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["balance"])
    elif flag == 2:
        account["balance"] += money
        save_account(account)
        code = 200
        msg = u"结算成功，用户{0}当前信用余额为：{1}元".format(account["name"], account["balance"])
    else:
        code = 400
        msg = u"暂不支持此结算方式"

    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def frozen_account(name):
    """冻结账户"""
    rsp = load_account(name)
    if rsp.code == 200:
        account = rsp.data
        account["locked"] = True
        rsp = save_account(account)
        if rsp.code == 200:
            code = 200
            msg = u"冻结账户{0}成功".format(name)
        else:
            code = 400
            msg = u"冻结账户{0}失败，原因：{1}".format(name, rsp.msg)
    else:
        code = 400
        msg = u"冻结账户{0}失败，原因：{1}".format(name, rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def thawing_account(name):
    """解冻账户"""
    rsp = load_account(name)
    if rsp.code == 200:
        account = rsp.data
        account["locked"] = False
        rsp = save_account(account)
        if rsp.code == 200:
            code = 200
            msg = u"解冻账户{0}成功".format(name)
        else:
            code = 400
            msg = u"解冻账户{0}失败，原因：{1}".format(name, rsp.msg)
    else:
        code = 400
        msg = u"解冻账户{0}失败，原因：{1}".format(name, rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def account_flow(account_name, action, details):
    """记录账户流水"""
    now = datetime.now()
    flow = Flow(now, account_name, action, details)
    flows_dir = os.path.join(PROJECT_DIR, "db", "flows_history")
    tmp = "flows_history_{0}{1}.json".format(now.year, now.month)
    flows_history_file = os.path.join(flows_dir, tmp)
    with open(flows_history_file, "a") as f:
        f.write("{0}\n".format(flow))
        f.flush()
    code = 200
    msg = u"账户流水成功入库，流水详情：{0}".format(flow.__dict__)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)
