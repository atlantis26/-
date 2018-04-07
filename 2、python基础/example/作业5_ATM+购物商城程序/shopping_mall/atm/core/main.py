# coding:utf-8
from atm.core.orm import ResponseData
from atm.core.accounts import account_is_exists, load_account, settle_account
from atm.core.accounts import account_flow, reset_account, query_account_flow
from atm.conf.settings import AUTH_FLAG
from atm.core.auth import auth
import logging


logger = logging.getLogger("atm.main")


def login(account_name, password):
    """登录"""
    if not account_is_exists(account_name):
        code = 400
        msg = u"账户{0}不存在,认证失败".format(account_name)
    else:
        resp = load_account(account_name)
        account = resp.data
        if account["password"] == password:
            code = 200
            msg = u"账户{0}成功登录，欢迎您使用本系统".format(account_name)
            AUTH_FLAG["is_authenticated"] = True
            AUTH_FLAG["is_administrator"] = account["is_administrator"]
            AUTH_FLAG["account_name"] = account_name
        else:
            code = 400
            msg = u"账户{0}的密码错误，认证失败".format(account_name)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def logout():
    """登出"""
    msg = u"账户{0}成功登出系统，欢迎再次光临".format(AUTH_FLAG["account_name"])
    AUTH_FLAG["is_authenticated"] = False
    AUTH_FLAG["account_name"] = None
    AUTH_FLAG["is_administrator"] = False
    code = 200
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
    account_flow(AUTH_FLAG["account_name"], u"还款/存款", msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def transfer(account_name, money):
    """转账"""
    if account_name == AUTH_FLAG["account_name"]:
        code = 400
        msg = u"转账失败，不能对自己进行转账操作"
    elif not account_is_exists(account_name):
        code = 400
        msg = u"转账失败，账户{0}不存在".format(account_name)
    else:
        rsp = load_account(AUTH_FLAG["account_name"])
        if rsp.code == 200:
            rsp = settle_account(rsp.data, money, flag=0)
        if rsp.code == 200:
            rsp = load_account(account_name)
        if rsp.code == 200:
            rsp = settle_account(rsp.data, money, flag=2)
        if rsp.code == 200:
            code = 200
            msg = u"转账成功，转账给账户{0}共计{1}元".format(account_name, money)
            account_flow(AUTH_FLAG["account_name"], u"转账/支出", msg)
            msg1 = u"转账成功，收到账户{0}转账共计{1}元".format(AUTH_FLAG["account_name"], money)
            account_flow(account_name, u"转账/存入", msg1)
        else:
            code = rsp.code
            msg = u"转账失败，原因：{0}".format(rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def history(year, month):
    """查询账户单月流水记录"""
    rsp = query_account_flow(AUTH_FLAG["account_name"], year, month)
    if rsp.code == 200:
        code = 200
        msg = u"查询成功"
    else:
        code = 400
        msg = u"查询失败，无相关流水信息"
    logger.debug(ResponseData(code, msg, rsp.data).__dict__)

    return ResponseData(code, msg, rsp.data)


@auth(AUTH_FLAG)
def balance():
    """查询余额"""
    resp = load_account(AUTH_FLAG["account_name"])
    if resp.code == 200:
        ba = resp.data["balance"]
        code = 200
        msg = u"查询成功，您的当前余额为：{0}元".format(ba)
    else:
        code = 400
        msg = "查询失败，原因：{0}".format(resp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


@auth(AUTH_FLAG)
def reset(password0, password1, password2):
    """修改密码"""
    resp = load_account(AUTH_FLAG["account_name"])
    if resp.code == 200:
        if resp.data["password"] == password0:
            resp = reset_account(AUTH_FLAG["account_name"], password1, password2)
            if resp.code == 200:
                code = 200
                msg = u"修改密码成功"
            else:
                code = 400
                msg = u"修改密码失败，原因：{0}".format(resp.msg)
        else:
            code = 400
            msg = u"修改密码失败，原密码输入错误"
    else:
        code = 400
        msg = u"修改密码失败，原因：{0}".format(resp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)
