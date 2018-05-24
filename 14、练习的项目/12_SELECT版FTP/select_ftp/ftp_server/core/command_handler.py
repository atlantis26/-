# coding:utf-8
from core.orm import SomeError, ResponseData
from core.user_handler import UserHandler
from conf.settings import DB_STORAGE
import hashlib
import shutil
import os
import logging

logger = logging.getLogger("ftp.commands")


class FtpCommands(object):
    def __init__(self, username=None):
        self.username = username
        self.path_depth = []

    def run(self, command, **kwargs):
        """执行命令，并返回执行结果"""
        try:
            self.validate_cmd(command)
            method_name = "cmd_{0}".format(command)
            return getattr(self, method_name)(**kwargs)
        except TypeError as e:
            print(str(e))
            msg = u"{0}命令执行失败，语法有误".format(command)
            logger.debug(ResponseData(400, msg).__dict__)
            return ResponseData(400, msg)

    @staticmethod
    def get_file_md5(file_path):
        """计算获取文件md5 code"""
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for line in f:
                md5.update(line)
        return md5.hexdigest()

    @property
    def current_path(self):
        """返回当前登录用户所在的绝对路径"""
        return os.path.join(self.user_home, *self.path_depth)

    @property
    def user_home(self):
        """返回当前登录用户的家目录"""
        self.is_authenticated()
        return os.path.join(DB_STORAGE, self.username)

    def get_cmd_list(self):
        """查询系统可用命令列表"""
        return [attr.split("_")[1] for attr in dir(self) if attr.startswith("cmd_")]

    def update_user_status(self, username):
        """设置用户登录状态"""
        if username:
            self.username = username
        else:
            self.username = None
            self.path_depth = []

    def validate_cmd(self, cmd):
        """检查命令cmd是否被支持"""
        if not hasattr(self, "cmd_{0}".format(cmd)):
            raise SomeError(u"{0}命令不存在".format(cmd))
        return True

    def validate_quota(self, file_size):
        """检查用户剩余quota配额是否满足文件上传的条件"""
        total_quota, used_quota, residual_quota = self.get_user_quota_detail()
        if residual_quota < file_size:
            raise SomeError("用户存储配额不足")

    def is_authenticated(self):
        """判断是否是已登录状态"""
        if not self.username:
            raise SomeError(u"认证失败,当前是未登录状态,请先登录用户")

    def cmd_mkdir(self, name):
        """
        功能描述：创建一个新目录；
        使用语法：mkdir ${name};
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            path = os.path.join(self.current_path, name)
            if os.path.exists(path):
                raise SomeError(u"文件目录{0}已存在".format(name))
            os.mkdir(path)
            code = 200
            msg = "mkdir命令执行成功"
        except SomeError as e:
            code = 400
            msg = "mkdir命令执行失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_remove(self, name):
        """
        功能描述：删除目录或文件，如果目标是非空目录，那么会递归删除其子文件、子目录
        使用语法：remove ${name}; 参数${name}为当前路径下的目录或文件的名称
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            if not name:
                raise SomeError(u"文件目录名不能为空")
            path = os.path.join(self.current_path, name)
            if not os.path.exists(path):
                raise SomeError(u"文件目录{0}不存在".format(name))
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            code = 200
            msg = "remove命令执行成功"
        except SomeError as e:
            code = 400
            msg = "remove命令执行失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_cd(self, name):
        """
        功能描述：切换用户所在目录
        使用语法：
                cd ${name}: 进入下一级目录,参数${name}为当前路径下的目录名称
                cd ..:返回上一级目录，参数".."代表为上一级目录
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            if name == "..":
                if not self.path_depth:
                    raise SomeError(u"用户已经在最上级目录")
                self.path_depth.pop()
            else:
                current_path, dir_lst, file_lst = next(os.walk(self.current_path))
                print(dir_lst)
                if name not in dir_lst:
                    raise SomeError("当前路径下不存在'{0}'文件目录".format(name))
                self.path_depth.append(name)
            code = 200
            msg = "cd切换目录命令执行成功"
        except SomeError as e:
            code = 400
            msg = "cd切换目录命令执行失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_ls(self):
        """
        功能描述：查看当前路径下的文件与目录名称
        使用语法：ls
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            current_path, dir_lst, file_lst = next(os.walk(self.current_path))
            data = dir_lst, file_lst
            code = 200
            msg = "ls命令执行成功"
        except SomeError as e:
            code = 400
            msg = "ls命令执行失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def cmd_pwd(self):
        """
        功能描述：查看用户当前所在ftp系统的路径
        使用语法：pwd
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            path = "/" + "/".join(self.path_depth)
            msg = "pwd命令执行成功"
            code = 200
        except SomeError as e:
            code = 400
            msg = "pwd命令执行失败，详情：{0}".format(str(e))
            path = None
        logger.debug(ResponseData(code, path).__dict__)

        return ResponseData(code, msg, path)

    def cmd_put(self, file_name, file_md5, temp_file_path):
        """
        功能描述：上传文件，上传到用户当前所在路径
        使用语法：put ${file_name}
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            file_path = os.path.join(self.current_path, file_name)
            if os.path.exists(file_path):
                raise SomeError(u"文件名{0}不能重复".format(file_name))
            # socket程序已经先将文件数据存储在临时文件内，这里只需拷贝临时文件内容
            shutil.move(temp_file_path, file_path)
            file_md51 = self.get_file_md5(file_path)
            if file_md51 != file_md5:
                raise SomeError(u"md5校验失败,传输接收数据有错误")
            code = 200
            msg = "上传文件成功"
        except SomeError as e:
            code = 400
            msg = "上传文件失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    def cmd_get(self, **kwargs):
        """
        功能描述：下载文件,文件必须在用户当前路径下存在
        使用语法：get ${file_name} ${download_directory}: 下载文件（全新下载）；
                 get ${temp_file_path}: 下载文件（断点续传下载）, ${temp_file_path}是被中止下载的文件的缓存文件路径
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            file_name = kwargs.get("file_name")
            seek_size = kwargs.get("tmp_size", 0)
            file_path = os.path.join(self.current_path, file_name)
            if not os.path.exists(file_path):
                raise SomeError(u"文件名{0}不存在".format(file_name))
            file_md5 = self.get_file_md5(file_path)
            file_size = os.path.getsize(file_path)
            # 这里只检查文件是否存在和返回文件的绝对路径，发送文件数据的操作，交给socket程序
            code = 200
            msg = "下载文件成功"
            data = {"file_path": file_path,
                    "file_md5": file_md5,
                    "file_size": file_size,
                    "seek_size": seek_size}
        except SomeError as e:
            code = 400
            msg = "下载文件失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def get_user_quota_detail(self):
        """功能描述：查询登录用户已使用的存储配额(GB)"""
        size = 0
        for root, dirs, files in os.walk(self.user_home):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        used_quota = round((size/(1024*1024*1024)), 2)

        user = UserHandler.load_user(self.username)
        total_quota = user["quota"]
        residual_quota = total_quota - used_quota

        return total_quota, used_quota, residual_quota

    def cmd_quota(self):
        """
        功能描述：查询用户存储总配额、可用配额、已用配额信息
        使用语法：quota
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            total_quota, used_quota, residual_quota = self.get_user_quota_detail()
            code = 200
            msg = "查询用户存储配额信息成功"
            data = {"total_quota": total_quota,
                    "used_quota": used_quota,
                    "residual_quota": residual_quota}
        except SomeError as e:
            code = 400
            msg = "查询用户存储配额信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    def cmd_help(self, cmd):
        """
        功能描述：查询命令列表或者查询某个命令的使用帮助信息
        使用语法：help  ：查询命令列表
                help ${command_name} ： 查询命令${command_name}的使用帮助信息
        返回值：命令执行结果
        """
        try:
            self.is_authenticated()
            if cmd:
                self.validate_cmd(cmd)
                method_name = "cmd_{0}".format(cmd)
                data = getattr(self, method_name).__doc__
            else:
                data = self.get_cmd_list()
            code = 200
            msg = "help命令执行成功"
        except SomeError as e:
            code = 400
            msg = "help命令执行失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)
