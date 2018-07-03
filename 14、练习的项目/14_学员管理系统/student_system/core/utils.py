# coding:utf-8


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomethingError(Exception):
    """自定义异常错误"""
    pass
