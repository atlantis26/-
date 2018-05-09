# coding:utf-8


class UserView(object):
    """用户登录成功后，进入的视图"""
    def __init__(self):
        pass

    def ftp_shell(self):
        while True:
            cmd_args = input(u" 请输入命令:>").strip()
            cmd_args = [s.strip() for s in cmd_args.split(" ")]
            rsp = self.client(self, cmd_args[0])(*cmd_args[1:])
            print(rsp.msg)


class HomeView(object):
    """用户未登录时，首页视图"""
    def __init__(self):
        pass
