# coding:utf-8


class User(object):
    """用户orm模型"""
    def __init__(self, username, password, quota):
        self.username = username
        self.password = password
        self.quota = quota


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    """自定义异常错误"""
    pass
