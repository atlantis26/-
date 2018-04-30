# coding:utf-8
from atm.core.orm import ResponseData
from atm.db.account_sample import account_sample, account_flow_sample
from atm.conf.settings import DB_TYPE, DB_Accounts, DB_Flows_History
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
                resp = save_account(resp.data.__dict__)
            code = resp.code
            msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def load_account(name):
    """加载账户数据"""
    if DB_TYPE == "FileStorage":
        account_file = os.path.join(DB_Accounts, "{0}.json".format(name))
        if not os.path.exists(account_file):
            code = 400
            msg = u"账户{0}不存在，加载数据失败".format(name)
            data = None
        else:
            with open(account_file, "r") as f:
                data = json.loads(f.read().strip())
            code = 200
            msg = "账户{0}的数据加载成功".format(name)
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
        data = None
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)


def save_account(account):
    """保存账户数据，写入到存储文件或数据库"""
    if DB_TYPE == "FileStorage":
        account_file = os.path.join(DB_Accounts, "{0}.json".format(account["name"]))
        account_json = json.dumps(account)
        with open(account_file, "w") as f:
            f.write(account_json)
            f.flush()
        code = 200
        msg = u"账户{0}信息保存成功".format(account["name"])
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def account_is_exists(name):
    """检测账户是否存在"""
    if DB_TYPE == "FileStorage":
        account_file = os.path.join(DB_Accounts, "{0}.json".format(name))
        if os.path.exists(account_file):
            return True
    else:
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
        raise Exception(msg)


def settle_account(account, money, flag=0):
    """结算功能：
                flag=0：表示支出业务；
                flag=1：表示取现业务，取现收取5%手续费；
                flag=2：表示存入业务；
    """
    if flag == 0:
        if account["balance"] >= money:
            account["balance"] -= money
            save_account(account)
            code = 200
            msg = u"结算成功，账户{0}扣款支出{1}元，当前余额为：{2}元".format(account["name"], money, account["balance"])
        else:
            code = 400
            msg = u"结算失败，账户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["balance"])
    elif flag == 1:
        total_money = float(money) * (1 + 0.05)
        if account["balance"] >= total_money:
            account["balance"] -= total_money
            save_account(account)
            code = 200
            msg = u"结算成功，账户{0}扣款支出{1}元（包含手续费{2}元),当前余额为：{3}元"\
                .format(account["name"], total_money, money*0.05, account["balance"])
        else:
            code = 400
            msg = u"结算失败，账户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["balance"])
    elif flag == 2:
        account["balance"] += float(money)
        save_account(account)
        code = 200
        msg = u"结算成功，账户{0}存入{1}元,当前余额为：{2}元".format(account["name"], money, account["balance"])
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
        if account["locked"] is False:
            account["locked"] = True
            rsp = save_account(account)
            if rsp.code == 200:
                code = 200
                msg = u"账户{0}冻结成功".format(name)
            else:
                code = 400
                msg = u"账户{0}冻结失败，原因：{1}".format(name, rsp.msg)
        else:
            code = 400
            msg = u"账户{0}已经是冻结状态，无需再次冻结".format(name)
    else:
        code = 400
        msg = u"账户{0}冻结失败，原因：{1}".format(name, rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def thawing_account(name):
    """解冻账户"""
    rsp = load_account(name)
    if rsp.code == 200:
        account = rsp.data
        if account["locked"] is True:
            account["locked"] = False
            rsp = save_account(account)
            if rsp.code == 200:
                code = 200
                msg = u"账户{0}解冻成功".format(name)
            else:
                code = 400
                msg = u"账户{0}解冻失败，原因：{1}".format(name, rsp.msg)
        else:
            code = 400
            msg = u"账户{0}是正常未冻结状态，无需解冻".format(name)
    else:
        code = 400
        msg = u"账户{0}解冻失败，原因：{1}".format(name, rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def account_flow(account_name, action, details):
    """记录账户流水"""
    if DB_TYPE == "FileStorage":
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
        rsp = account_flow_sample(time_stamp, account_name, action, details)
        if rsp.code == 200:
            flow = rsp.data
            tmp = "flows_history_{0}_{1}.json".format(now.year, now.month)
            flows_history_file = os.path.join(DB_Flows_History, tmp)
            with open(flows_history_file, "a") as f:
                f.write("{0}\n".format(json.dumps(flow.__dict__)))
                f.flush()
            code = 200
            msg = u"账户流水入库成功，流水详情：{0}".format(flow.__dict__)
        else:
            code = 400
            msg = u"账户流水入库失败，失败原因：{0}".format(rsp.msg)
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def query_account_flow(account_name, year, month):
    """查询账户单月流水记录"""
    flow_list = list()
    if DB_TYPE == "FileStorage":
        tmp = "flows_history_{0}_{1}.json".format(year, month)
        flows_history_file = os.path.join(DB_Flows_History, tmp)
        if os.path.exists(flows_history_file):
            with open(flows_history_file, "r") as f:
                for flow in f:
                    if account_name == json.loads(flow)["account_name"]:
                        flow_list.append(flow)
            code = 200
            msg = u"查询成功"
        else:
            code = 400
            msg = u"查询失败，无相关流水信息"
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
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
