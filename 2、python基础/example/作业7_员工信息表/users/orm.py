# coding:utf-8


class ResponseData(object):
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data
