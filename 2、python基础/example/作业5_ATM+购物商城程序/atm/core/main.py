# coding:utf-8
from atm.core.orm import ResponseData
from atm.core.accounts import account_is_exists, load_account, settle_account, save_account, account_flow
from atm.db.account_sample import account_sample
from atm.conf.settings import PROJECT_DIR
from atm.core.auth import auth
import os
import json
import logging


logger = logging.getLogger("atm.main")

AUTH_FLAG = {"is_authenticated": False, "account_name": None}


def login():
    """登陆"""
    account_name = input(u"请输入账号: ")
    password = input(u"请输入密码: ")
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account_name))
    if not os.path.exists(account_file):
        code = 400
        msg = u"账户{0}不存在,认证失败".format(account_name)
    else:
        with open(account_file, "r") as f:
            account = json.loads(f.read().strip())
        if account["password"] == password:
            code = 200
            msg = u"账户{0}的密码正确，认证成功".format(account_name)
            AUTH_FLAG["is_authenticated"] = True
            AUTH_FLAG["account_name"] = account_name
        else:
            code = 400
            msg = u"账户{0}的密码错误，认证失败".format(account_name)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def logout():
    """登出"""
    msg = u"用户{0}成功登出系统，欢迎再次光临".format(AUTH_FLAG["account_name"])
    AUTH_FLAG["is_authenticated"] = False
    AUTH_FLAG["account_name"] = None
    code = 200
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def create_account():
    """创建新账户"""
    account_name = input(u"请输入新建账户的账号：")
    if account_is_exists:
        code = 400
        msg = u"创建失败，账户{0}已存在".format(account_name)
    else:
        password1 =  input(u"请输入设置密码：")
        password2 = input(u"请再次输入设置密码：")
        if password1 != password2:
            code = 400
            msg = u"创建失败，账户{0}的两次设置密码不一致".format(account_name)
        else:
            resp = account_sample(account_name, password1)
            if resp.code == 200:
                resp = save_account(resp.data.__dict__)
            code = resp.code
            msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def pay(money):
    """付款"""
    resp = load_account(AUTH_FLAG["account_name"])
    if resp.code == 200:
        resp = settle_account(resp.data, money, flag=0)
    code = resp.code
    msg = resp.msg
    account_flow(AUTH_FLAG["account_name"], u"付款", msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def withdraw(money):
    """提现"""
    resp = load_account(AUTH_FLAG["account_name"])
    if resp.code == 200:
        resp = settle_account(resp.data, money, flag=1)
    code = resp.code
    msg = resp.msg
    account_flow(AUTH_FLAG["account_name"], u"提现", msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def repayment(money):
    """还款"""
    resp = load_account(AUTH_FLAG["account_name"])
    if resp.code == 200:
        resp = settle_account(resp.data, money, flag=2)
    code = resp.code
    msg = resp.msg
    account_flow(AUTH_FLAG["account_name"], u"还款", msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def transfer(account_name, money):
    """转账"""
    if not account_is_exists(account_name):
        code = 400
        msg = u"转账失败，账户{0}不存在".format(account_name)
    else:
        rsp = pay(money)
        if rsp.code == 200:
            resp = load_account(account_name)
            account = resp.data
            account["balance"] += money
            save_account(account)
            code = 200
            msg = u"转账成功，转账给账户{0}{1}元".format(account_name, money)
        else:
            code = rsp.code
            msg = u"转账失败，原因：{0}".format(rsp.msg)
    account_flow(AUTH_FLAG["account_name"], u"转账", msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def history(year, month):
    """查询账户单月流水记录"""
    flows_dir = os.path.join(PROJECT_DIR, "db", "flows_history")
    tmp = "flows_history_{0}{1}.json".format(year, month)
    flows_history_file = os.path.join(flows_dir, tmp)
    flow_list = list()
    if os.path.exists(flows_history_file):
        with open(flows_history_file, "r") as f:
            for flow in f:
                if AUTH_FLAG["account_name"] == json.loads(flow)["account_name"]:
                    flow_list.append(flow)
        code = 200
        msg = u"查询成功"
    else:
        code = 400
        msg = u"查询失败，无相关流水信息"
    logger.debug(ResponseData(code, msg, flow_list).__dict__)

    return ResponseData(code, msg)
