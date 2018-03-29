# coding:utf-8


class ResponseData(object):
    """统一函数方法返回值的格式"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is None:
            self.data = data
