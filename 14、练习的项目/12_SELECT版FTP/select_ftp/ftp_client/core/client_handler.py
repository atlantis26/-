# coding:utf-8
from core.utils import SomeError, ResponseData
from core.utils import show_process, get_file_md5
from conf.settings import Separator
import socket
import json
import os
import shutil
import hashlib
import logging

logger = logging.getLogger("ftp.ftp_client")


class FtpClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket()
        self.client.connect((host, port))
        self.username = None
        self.password = None

    def restart(self):
        """重新建立socket连接"""
        self.client.close()
        self.__init__(self.host, self.port)

    def run_cmd(self, cmd, *args):
        """命令执行统一入口"""
        try:
            attr = "cmd_{0}".format(cmd)
            rsp = getattr(self, attr)(*args).__dict__
            code = rsp.get("code")
            msg = rsp.get("msg")
        except AttributeError:
            code = 400
            msg = "命令执行失败，{0}不是系统支持的命令".format(cmd)
        except TypeError:
            code = 400
            msg = "{0}命令使用有误，请使用'help {1}'命令查询语法详细".format(cmd, cmd)

        return ResponseData(code, msg)

    @staticmethod
    def md5_password(password):
        """密码通过MD5加密"""
        return hashlib.md5(password.encode("utf-8")).hexdigest()

    @staticmethod
    def validate_md5(file_path, md5_code):
        # md5校验失败
        file_md5 = get_file_md5(file_path)
        if file_md5 != md5_code:
            raise SomeError("md5校验失败,传输接收数据有错误")

    def _get_response(self, req_data):
        """不带文件内容的请求，发送请求，并获取响应"""
        data_json = json.dumps(req_data).encode("utf-8")
        self.client.send(data_json)
        rsp = self.client.recv(1024)
        rsp = json.loads(rsp.decode("utf-8"))
        return rsp

    def _put_file_response(self, req_data, file_path):
        """对于上传文件的请求，分数据块发送，以时间戳作为服务端缓存文件的标示
        """
        file_size = os.path.getsize(file_path)
        send_size = 0
        with open(file_path, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                request_json = json.dumps(req_data).encode('utf-8')
                b_str = request_json + Separator + file_data
                self.client.send(b_str)
                send_size += len(file_data)
                show_process(file_size, send_size)
                # 每发送一段文件数据块后，服务端都会有一次响应
                rsp = self.client.recv(1024)
                rsp = json.loads(rsp.decode("utf-8"))
                if rsp["code"] == 201:
                    req_data["kwargs"]["time_stamp"] = rsp["data"]["time_stamp"]
                else:
                    return rsp

    @staticmethod
    def split_get_file_response_data(data):
        """拆分请求数据"""
        data_list = data.split(Separator)
        if len(data_list) == 1:
            json_string = data_list[0]
            file_data = b""
        elif len(data_list) == 2:
            json_string = data_list[0]
            file_data = data_list[1]
        else:
            raise SomeError("传输的请求数据包格式有误，请联系管理员")

        return json_string, file_data

    def _get_file_response(self, req_data, directory):
        """对于下载文件的请求，分多次发送请求下载数据，每次请求下载一部分内容
        """
        file_name = req_data["kwargs"]["file_name"]
        tmp_file_path = os.path.join(directory, "{0}.ftp.tmp".format(file_name))
        while True:
            data_json = json.dumps(req_data).encode("utf-8")
            self.client.send(data_json)
            # 发送文件内容，并接收服务端响应
            data = self.client.recv(2048)
            rsp, file_data = self.split_get_file_response_data(data)
            rsp = json.loads(rsp.decode("utf-8"))

            if rsp["code"] == 201:
                # code=201表示未完成文件下载，更新本地临时文件内容后继续发送请求
                with open(tmp_file_path, "ab") as f:
                    f.write(file_data)
                    f.flush()
                # 更新缓存文件大小，告诉服务端从何处开始发送文件数据，标示seek的位置
                receive_size = int(req_data["kwargs"]["tmp_size"]) + len(file_data)
                req_data["kwargs"]["tmp_size"] = receive_size
                # 打印下载进度条
                file_size = rsp["data"]["file_size"]
                show_process(file_size, receive_size)
            elif rsp["code"] == 200:
                # code=200表示文件数据下载完成，后续将临时文件名变更为原文件名和md5内容一致性校验
                file_path = os.path.join(directory, file_name)
                shutil.move(tmp_file_path, file_path)
                # 校验MD5文件内容一致性
                print(rsp)
                file_md5 = rsp["data"]["file_md5"]
                self.validate_md5(file_path, file_md5)
                return rsp
            else:
                return rsp

    def register(self, username, password1, password2, quota):
        """注册用户"""
        try:
            data = dict()
            data["cmd"] = "register"
            password1 = self.md5_password(password1)
            password2 = self.md5_password(password2)
            data["kwargs"] = {"username": username,
                              "password1": password1,
                              "password2": password2,
                              "quota": quota}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"注册用户失败，原因：{1}".format(username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def login(self, username, password):
        """用户登录"""
        try:
            data = dict()
            data["cmd"] = "login"
            password = self.md5_password(password)
            data["kwargs"] = {"username": username,
                              "password": password}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            self.username = username
            self.password = password
            data = {"username": username}
        except SomeError as e:
            code = 400
            msg = u"登录失败，原因：{1}".format(username, str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def logout(self):
        """用户登出"""
        try:
            data = dict()
            data["cmd"] = "logout"
            data["kwargs"] = {}
            rsp = self._get_response(data)
            code = rsp["code"]
            msg = rsp["msg"]
            if rsp["code"] == 200:
                self.username = None
                self.password = None
        except SomeError as e:
            code = 400
            msg = u"登出失败，原因：{1}".format(self.username, str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_put(self, file_path):
        """上传文件到个人仓库"""
        try:
            if not os.path.exists(file_path):
                raise SomeError(u"文件{0}不存在".format(file_path))
            file_name = os.path.split(file_path)[-1]
            file_size = os.path.getsize(file_path)
            file_md5 = get_file_md5(file_path)
            req_body = dict()
            req_body["cmd"] = "put"
            req_body["kwargs"] = {"file_name": file_name,
                                  "file_size": file_size,
                                  "file_md5": file_md5}
            rsp = self._put_file_response(req_body, file_path)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"上传文件失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_get(self, file_name_or_tmp_path, directory=None):
        """下载文件"""
        try:
            req_body = dict()
            req_body["cmd"] = "get"
            if directory:
                if not os.path.exists(directory):
                    raise SomeError(u"存放文件的目录{0}不存在".format(directory))
                req_body["kwargs"] = {"file_name": file_name_or_tmp_path,
                                      "tmp_size": 0}
            else:
                if not file_name_or_tmp_path.endswith(".ftp.tmp"):
                    raise SomeError(u"缓存文件名称格式有误，请核对后再试")
                if not os.path.exists(file_name_or_tmp_path):
                    raise SomeError(u"缓存文件不存在，请核对后再试")
                tmp_size = os.path.getsize(file_name_or_tmp_path)
                file_path = file_name_or_tmp_path.split(".ftp.tmp")[0]
                file_lst = os.path.split(file_path)
                file_name = file_lst[-1]
                req_body["kwargs"] = {"file_name": file_name,
                                      "tmp_size": tmp_size}
                directory = os.path.join(*file_lst[:-1])
            rsp = self._get_file_response(req_body, directory)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except KeyboardInterrupt:
            msg = u"执行下载文件命令过程中被中止，部分文件数据已下载写入到下载目录下的缓存文件内；" \
                  u"系统支持文件断点续传，您可使用‘help get’命令了解详情"
            raise KeyboardInterrupt(msg)
        except SomeError as e:
            code = 400
            msg = u"下载文件失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_mkdir(self, name):
        """创建目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "mkdir"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"创建目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_remove(self, name):
        """删除文件目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "remove"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"删除目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_cd(self, name):
        """切换目录"""
        try:
            req_body = dict()
            req_body["cmd"] = "cd"
            req_body["kwargs"] = {"name": name}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
        except SomeError as e:
            code = 400
            msg = u"切换目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_ls(self):
        """查询用户当前路径下文件目录信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "ls"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
            if code == 200:
                dirs, files = rsp.get("data")
                print(u"目录列表：{0} \n文件列表:{1}".format(dirs, files))
        except SomeError as e:
            code = 400
            msg = u"查询当前路径下文件目录失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_pwd(self):
        """查询用户当前ftp目录路径"""
        try:
            req_body = dict()
            req_body["cmd"] = "pwd"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
            if code == 200:
                data = rsp.get("data")
                print(u"您当前ftp目录路径：{0}".format(data))
        except SomeError as e:
            code = 400
            msg = u"查询当前ftp目录路径, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_quota(self):
        """查询用户存储配额信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "quota"
            req_body["kwargs"] = {}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
            if code == 200:
                data = rsp.get("data")
                msg = u"""
                您的存储配额详情为：
                    总配额：{0}GB 
                    已使用配额：{1}GB
                    剩余配额：{2}GB""".format(data["total_quota"], data["used_quota"], data["residual_quota"])
                print(msg)
        except SomeError as e:
            code = 400
            msg = u"查询用户存储配额信息, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_help(self, cmd=""):
        """查询命令列表，及命令使用信息"""
        try:
            req_body = dict()
            req_body["cmd"] = "help"
            req_body["kwargs"] = {"cmd": cmd}
            rsp = self._get_response(req_body)
            logger.debug(rsp)
            code = rsp["code"]
            msg = rsp["msg"]
            if code == 200:
                data = rsp.get("data")
                if cmd == "":
                    print("系统支持的命令列表：{0}".format(data))
                    print("您可以使用 help ${command_name}的语法方式，查询某个命令的具体用法")
                else:
                    print(u"{0}命令的使用详情：".format(cmd))
                    print(data)
        except SomeError as e:
            code = 400
            msg = u"查询命令相关信息失败, 原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
