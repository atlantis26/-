# coding:utf-8


class RedisHandler(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pool = []

    def get(self):
        pass

    def put(self, log):
        pass

    def append(self, msg):
        pass
