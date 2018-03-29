# coding:utf-8
from atm.core.common import ResponseData
from atm.conf.settings import PROJECT_DIR
from atm.core.auth import auth
import os
import json


@auth
def load_account(account_name):
    """加载账户数据"""
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account_name))
    if not os.path.exists(account_file):
        code = 400
        msg = u"账户{0}不存在，加载数据失败".format(account_name)
        data = None
    else:
        with open(account_file, "r") as f:
            data = json.loads(f.read().strip())
        code = 200
        msg = "账户{0}的数据加载成功".format(account_name)

    return ResponseData(code, msg, data)


@auth
def save_account(account):
    """保存账户数据，写入到存储文件"""
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account["name"]))
    account_json = json.dumps(account)
    with open(account_file, "r+") as f:
        f.write(account_json)
        f.flush()
    code = 200
    msg = u"账户{0}信息保存成功".format(account["name"])

    return ResponseData(code, msg)


def account_is_exists(account_name):
    """检测账户是否存在"""
    account_file = os.path.join(PROJECT_DIR, "db", "{0}.json".format(account_name))
    if os.path.exists(account_file):
        return True


def settle_account(account, money):
    if account["money"] >= money:
        account["money"] = account["money"] - money
        save_account(account)
        code = 200
        msg = u"结算成功，用户{0}当前信用余额为：{1}".format(account["account_name"], account["money"])
    else:
        code = 400
        msg = u"结算失败，用户{0}的余额不足，当前余额为：{1}".format(account["account_name"], account["money"])

    return ResponseData(code, msg)