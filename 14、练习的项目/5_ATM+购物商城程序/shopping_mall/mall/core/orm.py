# coding:utf-8


class ResponseData(object):
    """统一函数方法返回值的格式"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class Flow(object):
    """账户单笔流水信息"""
    def __init__(self, datetime, name, action, details):
        self.datetime = datetime
        self.name = name
        self.action = action
        self.details = details
