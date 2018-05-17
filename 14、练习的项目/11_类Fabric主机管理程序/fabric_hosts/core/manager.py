# coding:utf-8
from core.db_handler import create_host, query_host, create_host_group, query_host_host
from core.orm import Host, HostGroup, SomeError, ResponseData
import paramiko
import logging


class HostsManager(object):
    @property
    def host(self):
        """"""
        return _Host()

    @property
    def host_group(self):
        return _HostGroup()


class _Host(object):
    @staticmethod
    def create_session(hostname, port, username, password):
        """创建ssh客户端连接实例"""
        return _Shell(hostname, port, username, password)

    @staticmethod
    def create_sftp_session(hostname, port, username, password):
        """创建sftp客户端连接实例"""
        return _TransPort(hostname, port, username, password)

    @staticmethod
    def create(host_id, ip, port, username, password):
        try:
            host = Host(host_id, ip, port, username, password)
            create_host(host)
            code = 200
            msg = "添加服务器主机信息成功"
            data = host.__dict__
        except SomeError as e:
            code = 400
            msg = "添加服务器主机信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)

    @staticmethod
    def detail(hostname):
        try:
            host = query_host(hostname)
            code = 200
            msg = "查询服务器主机信息成功"
            data = host.__dict__
        except SomeError as e:
            code = 400
            msg = "查询服务器主机信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)


class _HostGroup(object):
    @staticmethod
    def create(group_id, host_ids):
        """创建服务器主机组信息"""
        try:
            host_group = HostGroup(group_id, host_ids)
            create_host_group(host_group)
            code = 200
            msg = "添加服务器主机组信息成功"
            data = host_group.__dict__
        except SomeError as e:
            code = 400
            msg = "添加服务器主机组信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)

    @staticmethod
    def detail(host_group_name):
        try:
            host = query_host_host(host_group_name)
            code = 200
            msg = "查询服务器主机组信息成功"
            data = host.__dict__
        except SomeError as e:
            code = 400
            msg = "查询服务器主机组信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)

    @staticmethod
    def execute_cmd(cmd):
        pass

    @staticmethod
    def get(remote_path, local_path):
        pass

    @staticmethod
    def put(local_path, remote_path):
        pass


class _Shell(object):
    def __init__(self, hostname, port, username, password):
        """初始化，创建ssh连接"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client = ssh.connect(hostname, port, username, password)

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


class _TransPort(object):
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
