# coding:utf-8


class Host(object):
    def __init__(self, host_id, ip, port, username, password):
        self.host_id = host_id
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password


class HostGroup(object):
    def __init__(self, group_id, group_name, host_id_list):
        self.group_id = group_id
        self.group_name = group_name
        self.host_id_list = host_id_list


class ResponseData(object):
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    pass
