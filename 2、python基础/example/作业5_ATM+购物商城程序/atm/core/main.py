# coding:utf-8
from atm.core.common import ResponseData
from atm.core.accounts import account_is_exists, load_account, settle_account, save_account
from atm.db.account_sample import account_sample
from atm.conf.settings import PROJECT_DIR
from atm.core.auth import auth
import os
import json
import logging


logger = logging.getLogger("atm.main")

ACCOUNT = {"is_authenticated": False, "details": None}


def login():
    """登陆"""
    account_name = input(u"请输入账号: ")
    password = input(u"请输入密码: ")
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account_name))
    if not os.path.exists(account_file):
        code = 400
        msg = u"账户{0}不存在,认证失败".format(account_name)
        data = None
    else:
        with open(account_file, "r") as f:
            account = json.loads(f.read().strip())
        if account["password"] == password:
            code = 200
            msg = u"账户{0}的密码正确，认证成功".format(account_name)
            data = account
        else:
            code = 400
            msg = u"账户{0}的密码错误，认证失败".format(account_name)
            data = None
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)


@auth(ACCOUNT)
def logout():
    """登出"""
    ACCOUNT["is_authenticated"] = False
    code = 200
    msg = u"用户{0}成功登出系统，欢迎再次光临".format(ACCOUNT["details"]["account_name"])
    data = ACCOUNT
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg, data)


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
                resp = save_account(resp.data)
            code = resp.code
            msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(ACCOUNT)
def pay_the_bill(account_name, money):
    """付款"""
    resp = load_account(account_name)
    if resp.code == 200:
        resp = settle_account(resp.data, money)
    code = resp.code
    msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(ACCOUNT)
def withdraw(account_name, money):
    """提现"""
    resp = load_account(account_name)
    if resp.code == 200:
        resp = settle_account(resp.data, money, flag=True)
    code = resp.code
    msg = resp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(ACCOUNT)
def transfer(m_account, h_account, money):
    """转账"""

