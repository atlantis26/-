# coding:utf-8


class ResponseData(object):
    """统一函数方法返回值的格式"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class Account(object):
    """账户orm模型"""
    def __init__(self, name, password, balance, locked=False, is_administrator=False):
        self.name = name
        self.password = password
        self.balance = balance
        self.locked = locked
        self.is_administrator = is_administrator


class Flow(object):
    """账户单笔流水信息"""
    def __init__(self, datetime, account_name, action, details):
        self.datetime = datetime
        self.account_name = account_name
        self.action = action
        self.details = details
