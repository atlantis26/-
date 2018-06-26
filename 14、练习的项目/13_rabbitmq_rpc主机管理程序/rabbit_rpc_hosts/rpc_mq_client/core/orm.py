# coding:utf-8


class Task(object):
    def __init__(self, task_id, queue, data):
        self.task_id = task_id
        self.queue = queue
        self.data = data


class ResponseData(object):
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    pass
