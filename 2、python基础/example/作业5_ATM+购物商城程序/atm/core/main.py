# coding:utf-8
from atm.core.common import ResponseData
from atm.core.accounts import account_is_exists, load_account, settle_account
from atm.db.account_sample import account_sample
import logging

logger = logging.getLogger("atm.main")


def create_account():
    account_name = input(u"请输入新建账户的账号：")
    if account_is_exists:
        code = 400
        msg = u"创建失败，账户{0}已存在".format(account_name)
        data = None
    else:
        password1 =  input(u"请输入设置密码：")
        password2 = input(u"请再次输入设置密码：")
        if password1 != password2:
            code = 400
            msg = u"创建失败，账户{0}的两次设置密码不一致".format(account_name)
            data = None
        else:
            resp = account_sample(account_name, password1)
            code = resp["code"]
            msg = resp["msg"]
            data = resp["data"]
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)


def pay_the_bill(account_name, money):
    rsp = load_account(account_name)
    if rsp.code == 200:
        rsp = settle_account(rsp.data, money)
    code = rsp.code
    msg = rsp.msg

    return ResponseData(code, msg)