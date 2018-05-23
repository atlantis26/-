# coding:utf-8
from core.orm import SomeError, ResponseData
import threading
import paramiko
import logging


class Shell(object):
    def __init__(self, hostname, port, username, password):
        """初始化，创建ssh连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, port, username, password)

    def execute(self, cmd):
        """执行命令"""
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            data = {"stdout": stdout.read(),
                    "stderr": stderr.read()}
            code = 200
            msg = "执行命令成功"
        except SomeError as e:
            code = 400
            msg = "执行命令失败，详情：{0}".format(str(e))
            data = None
        logging.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def close(self):
        self.client.close()


class TransPort(object):
    def __init__(self, hostname, port, username, password):
        """初始化，创建sftp连接"""
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        transport = paramiko.Transport(hostname, port)
        transport.connect(username, password)
        self.client = paramiko.SFTPClient.from_transport(transport)

    def put(self, local_path, remote_path):
        """文件上传"""
        try:
            data = self.client.put(local_path, remote_path)
            code = 200
            msg = "文件上传成功".format(self.hostname)
        except SomeError as e:
            code = 400
            msg = "文件上传失败，详情：{0}".format(str(e))
            data = None
        logging.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def get(self, remote_path, local_path):
        """文件下载"""
        try:
            data = self.client.get(remote_path, local_path)
            code = 200
            msg = "文件下载成功".format(self.hostname)
        except SomeError as e:
            code = 400
            msg = "文件下载失败，详情：{0}".format(str(e))
            data = None
        logging.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def close(self):
        """sftp关闭连接"""
        self.client.close()


class HostThread(threading.Thread):
    def __init__(self, host, action, **kwargs):
        self.host = host
        self.action = action
        self.kwargs = kwargs
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        if self.action == "cmd":
            client = Shell(hostname=self.host.ip,
                           port=self.host.port,
                           username=self.host.username,
                           password=self.host.password)
            self.result = client.execute(**self.kwargs)
            client.close()
        elif self.action == "get":
            client = TransPort(hostname=self.host.ip,
                               port=self.host.port,
                               username=self.host.username,
                               password=self.host.password)
            self.result = client.get(**self.kwargs)
            client.close()
        elif self.action == "put":
            client = TransPort(hostname=self.host.ip,
                               port=self.host.port,
                               username=self.host.username,
                               password=self.host.password)
            self.result = client.put(**self.kwargs)
            client.close()
        else:
            msg = u"不支持'{0}'类型任务job,请联系管理员核实".format(self.action)
            self.result = ResponseData(400, msg)

    def get_result(self):
        return self.result
