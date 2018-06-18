# coding:utf-8
from core.orm import SomeError, ResponseData
import threading
import paramiko
import logging
import os

logger = logging.getLogger("fabric.rpc")


class Shell(object):
    def __init__(self, hostname, port, username, password):
        """初始化，创建ssh连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, port, username, password)

    def execute(self, commands):
        """执行命令"""
        try:
            cmd_list = commands.split(",")
            data = {}
            for cmd in cmd_list:
                stdin, stdout, stderr = self.client.exec_command(cmd)
                data[cmd] = {"stdout": stdout.read(),
                             "stderr": stderr.read()}
            code = 200
            msg = "执行命令成功"
        except SomeError as e:
            code = 400
            msg = "执行命令失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

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
        transport = paramiko.Transport((hostname, int(port)))
        transport.connect(username=username, password=password)
        self.client = paramiko.SFTPClient.from_transport(transport)

    def put(self, local_path, remote_path):
        """文件上传"""
        try:
            if not os.path.exists(local_path):
                raise SomeError(u"本地文件'{0}'不存在".format(local_path))
            self.client.put(local_path, remote_path)
            code = 200
            msg = "文件上传成功".format(self.hostname)
        except FileNotFoundError:
            code = 400
            msg = "文件上传失败，详情：远程主机上存放文件的目录路径不存在"
        except SomeError as e:
            code = 400
            msg = "文件上传失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def get(self, remote_path, local_path):
        """文件下载"""
        try:
            self.client.get(remote_path, local_path)
            code = 200
            msg = "文件下载成功".format(self.hostname)
        except FileNotFoundError:
            code = 400
            msg = "文件下载失败，详情：目标主机上不存在该文件"
        except SomeError as e:
            code = 400
            msg = "文件下载失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

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
        try:
            if self.action == "commands":
                client = Shell(hostname=self.host["ip"],
                               port=self.host["port"],
                               username=self.host["username"],
                               password=self.host["password"])
                self.result = client.execute(**self.kwargs).__dict__
                client.close()
            elif self.action == "get":
                local_dir = self.kwargs["local_dir"]
                local_host_id_dir = os.path.join(local_dir, str(self.host["host_id"]))
                if not os.path.exists(local_host_id_dir):
                    os.mkdir(local_host_id_dir)
                remote_path = self.kwargs["remote_path"]
                file_name = os.path.split(remote_path)[-1]
                local_path = os.path.join(local_host_id_dir, file_name)
                client = TransPort(hostname=self.host["ip"],
                                   port=self.host["port"],
                                   username=self.host["username"],
                                   password=self.host["password"])
                self.result = client.get(remote_path, local_path).__dict__
                client.close()
            elif self.action == "put":
                client = TransPort(hostname=self.host["ip"],
                                   port=self.host["port"],
                                   username=self.host["username"],
                                   password=self.host["password"])
                self.result = client.put(**self.kwargs).__dict__
                client.close()
            else:
                msg = u"不支持'{0}'类型任务job,请联系管理员核实".format(self.action)
                self.result = ResponseData(400, msg).__dict__
        except paramiko.ssh_exception.AuthenticationException:
            msg = u"执行失败，原因：登录失败，请检查目标主机的连接配置信息中账号密码是否正确"
            self.result = ResponseData(400, msg).__dict__
        except TimeoutError:
            msg = u"执行失败，原因：连接超时，请检查目标主机的网络是否连通"
            self.result = ResponseData(400, msg).__dict__

    def get_result(self):
        return self.result
