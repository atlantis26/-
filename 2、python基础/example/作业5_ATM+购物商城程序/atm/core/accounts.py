# coding:utf-8
from atm.core.common import ResponseData
from atm.conf.settings import PROJECT_DIR
from atm.core.auth import auth
import os
import json
import logging

logger = logging.getLogger("atm.accounts")


def load_account(name):
    """加载账户数据"""
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(name))
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
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account["name"]))
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
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(name))
    if os.path.exists(account_file):
        return True


def settle_account(account, money, flag=False):
    """结算功能，flag默认为False,表示正常结算；flag为True表示为提现操作，需加收5%手续费"""
    if flag:
        money = float(money) * (1 + 0.05)
    if account["money"] >= money:
        account["money"] = account["money"] - money
        save_account(account)
        code = 200
        msg = u"结算成功，用户{0}当前信用余额为：{1}元".format(account["name"], account["money"])
    else:
        code = 400
        msg = u"结算失败，用户{0}的余额不足，当前余额为：{1}元".format(account["name"], account["money"])
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def frozen_account(name):
    """冻结账户"""
    rsp = load_account(name)
    if rsp.code == 200:
        account = rsp.data
        account["is_frozen"] = True
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


def frozen_account(name):
    """冻结账户"""
    rsp = load_account(name)
    if rsp.code == 200:
        account = rsp.data
        account["is_frozen"] = True
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


def thaw_account(name):
    """解冻账户"""

