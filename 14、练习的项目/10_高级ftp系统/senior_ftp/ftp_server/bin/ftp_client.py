# coding=utf-8
from core.client_handler import FtpClient
from core.orm import SomeError


class FtpPortal(object):
    def __init__(self, host, ip):
        self.client = FtpClient(host, ip)

    def register(self):
        """注册用户"""
        username = input(u"请输入注册用户名：").strip()
        password1 = input(u"请输入设置密码：").strip()
        password2 = input(u"请重复输入设置的密码：").strip()
        return self.client.register(username, password1, password2, quota=50)

    def login(self):
        """用户登录"""
        username = input(u"请输入用户名：").strip()
        password = input(u"请输入密码：").strip()
        return self.client.login(username, password)

    def console(self):
        home_page = """
        --------------------欢迎访问无忧FTP云盘系统---------------------
        请先根据操作编号进行注册\登录操作：
        <\033[36;1m1\033[0m>.用户注册                      <\033[36;1m2\033[0m>.用户登录
        """
        while True:
            print(home_page)
            action = input(u"请输入您选择的操作编号：").strip()
            if action == "1":
                rsp = self.register()
                print(rsp.msg)
            elif action == "2":
                rsp = self.login()
                print(rsp.msg)
                if rsp.code == 200:
                    username = rsp.data
                    while True:
                        cmd_args = input(u"${0}>: ".format(username)).strip()
                        cmd_args = [s.strip() for s in cmd_args.split(" ")]
                        rsp = self.client.run_cmd(cmd_args[0], *cmd_args[1:])
                        print(rsp.msg)
            else:
                raise SomeError(u"输入的操作项编号{0}不存在，请核对后再试".format(action))


if __name__ == "__main__":
    client = FtpPortal("localhost", 4396)
    client.console()
