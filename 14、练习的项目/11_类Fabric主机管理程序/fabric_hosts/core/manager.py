# coding:utf-8
from core.db_handler import create_host, query_host, create_host_group, query_host_group
from core.orm import Host, HostGroup, SomeError, ResponseData
import threading
import paramiko
import logging


class HostsManager(object):
    @property
    def host(self):
        """"""
        return _Host

    @property
    def host_group(self):
        return _HostGroup


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
        """添加新主机信息"""
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
        """查询主机信息详情"""
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
        """创建主机组信息"""
        try:
            host_group = HostGroup(group_id, host_ids)
            create_host_group(host_group)
            code = 200
            msg = "添加主机组信息成功"
            data = host_group.__dict__
        except SomeError as e:
            code = 400
            msg = "添加主机组信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)

    @staticmethod
    def detail(group_id):
        """查询主机组信息详情"""
        try:
            host_group = query_host_group(group_id)
            code = 200
            msg = "查询主机组信息成功"
            data = host_group.__dict__
        except SomeError as e:
            code = 400
            msg = "查询主机组信息失败，详情：{0}".format(str(e))
            data = None
        return ResponseData(code, msg, data)

    @staticmethod
    def _execute_job(group_id, action, **kwargs):
        """批量在主机组内的全部主机上都执行任务"""
        host_group = query_host_group(group_id)
        hosts = [query_host(host_id) for host_id in host_group.host_ids]
        result = {}
        threads = []
        for host in hosts:
            thread = HostThread(host, action, **kwargs)
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for thread in threads:
            result[thread.host_id] = thread.get_result()

        return result

    @staticmethod
    def execute_cmd(group_id, cmd):
        """批量在主机组内的全部主机上都执行命令"""
        return _HostGroup._execute_job(group_id, "cmd", cmd=cmd)

    @staticmethod
    def get(group_id, remote_path, local_path):
        """批量在主机组内的全部主机上都执行下载"""
        return _HostGroup._execute_job(group_id, "get", remote_path=remote_path,  local_path=local_path)

    @staticmethod
    def put(group_id, local_path, remote_path):
        """批量在主机组内的全部主机上都执行上传"""
        return _HostGroup._execute_job(group_id, "put", local_path=local_path, remote_path=remote_path)


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


class HostThread(threading.Thread):
    def __init__(self, host, action, **kwargs):
        self.host = host
        self.action = action
        self.kwargs = kwargs
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        if self.action == "cmd":
            client = _Shell(**self.host)
            self.result = client.execute(**self.kwargs)
            client.close()
        elif self.action == "get":
            client = _TransPort(**self.host)
            self.result = client.get(**self.kwargs)
            client.close()
        elif self.action == "put":
            client = _TransPort(**self.host)
            self.result = client.put(**self.kwargs)
            client.close()
        else:
            msg = u"不支持'{0}'类型任务job,请联系管理员核实".format(self.action)
            self.result = ResponseData(400, msg)

    def get_result(self):
        return self.result
