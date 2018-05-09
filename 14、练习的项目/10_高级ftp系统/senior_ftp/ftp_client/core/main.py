# coding=utf-8
from core.client_handler import FtpClient


class FtpPortal(object):
    def __init__(self, host, ip):
        self.client = FtpClient(host, ip)
        self.username = None
        self.password = None

    def register(self):
        """注册用户"""
        username = input(u"请输入注册用户名：").strip()
        password1 = input(u"请输入设置密码：").strip()
        password2 = input(u"请重复输入设置的密码：").strip()
        rsp = self.client.register(username, password1, password2, quota=50)
        print(rsp.msg)

    def login(self):
        """用户登录"""
        username = input(u"请输入用户名：").strip()
        password = input(u"请输入密码:").strip()
        rsp = self.client.login(username, password)
        if rsp["code"] == 200:
            self.username = username
            self.password = password
        print(rsp.msg)

    def logout(self):
        """用户登出"""
        rsp = self.client.logout()
        if rsp["code"] == 200:
            self.username = None
            self.password = None
        print(rsp.msg)

    def ftp_shell(self):
        cmd_args = input(u" 请输入执行的命令:>").strip()
        cmd_args = [s.strip() for s in cmd_args.split(" ")]
        rsp = self.client.run(cmd_args[0], *cmd_args[1:])
        print(rsp.msg)

    def help(self):
        rsp = self.client.help()
        if rsp["code"] == 200:
            print(rsp["data"])
        print(rsp["msg"])

    def console(self):
        while True:
            msg = """--------------------欢迎访问无忧FTP云盘系统---------------------
            你可以通过命令进行如下操作：
            <\033[36;1m1\033[0m>.用户注册                      <\033[36;1m2\033[0m>.用户登录
            <\033[36;1m3\033[0m>.用户登出                      <\033[36;1m4\033[0m>.查询ftp系统支持的命令及使用信息
            """
            print(msg)
            actions = {"1": self.register,
                       "2": self.login,
                       "3": self.logout,
                       "4": self.help}
            num = input(u"请输入您选择的操作编号：").strip()
            if num not in actions:
                print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()


if __name__ == "__main__":
    client = FtpPortal("localhost", 4396)
    client.console()
