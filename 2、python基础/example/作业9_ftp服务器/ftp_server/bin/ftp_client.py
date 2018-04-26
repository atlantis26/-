# coding=utf-8
from core.client_handler import FtpClient


class FtpSystem(object):
    def __init__(self):
        self.client = FtpClient("localhost", 4396)
        self.username = None
        self.password = None
        self.console()

    def register(self):
        username = input(u"请输入注册用户名：").strip()
        password1 = input(u"请输入设置密码：").strip()
        password2 = input(u"请重复输入设置的密码：").strip()
        rsp = self.client.register(username, password1, password2)
        print(rsp.msg)

    def login(self):
        username = input(u"请输入用户名：").strip()
        password = input(u"请输入密码:").strip()
        rsp = self.client.login(username, password)
        self.username = username
        self.password = password
        print(rsp.msg)

    def logout(self):
        rsp = self.client.logout(self.username)
        print(rsp.msg)

    def show(self):
        rsp = self.client.show()
        print(rsp.msg)

    def upload(self):
        file_path = input(u"请输入上传文件的文件路径：").strip()
        rsp = self.client.upload(file_path)
        print(rsp.msg)

    def download(self):
        file_name = input(u"请输入下载文件的名称：").strip()
        directory = input(u"请输入保存文件的目录地址：").strip()
        rsp = self.client.download(file_name, directory)
        print(rsp.msg)

    def console(self):
        while True:
            msg = """--------------------欢迎访问无忧FTP云盘系统---------------------
                    你可以选择如下操作：
                    <\033[36;1m1\033[0m>.用户注册                     <\033[36;1m2\033[0m>.用户登录
                    <\033[36;1m3\033[0m>.用户登出                     <\033[36;1m4\033[0m>.个人文件查看
                    <\033[36;1m5\033[0m>.上传文件                     <\033[36;1m6\033[0m>.下载文件
                    """
            print(msg)
            actions = {"1": self.register,
                       "2": self.login,
                       "3": self.logout,
                       "4": self.show,
                       "5": self.upload,
                       "6": self.download}
            num = input(u"请输入您选择的操作编号：").strip()
            if num not in actions:
                print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

if __name__ == "__main__":
    FtpSystem()
