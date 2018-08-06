#  coding:utf-8
from core.views import HybridViews
from core.handler import login


def console():
    while True:
        msg = u"""------------欢迎访问堡垒机系统---------------
            您可以选择如下操作：
                <\033[36;1m1\033[0m>.用户登录                     <\033[36;1m2\033[0m>.退出系统
        """
        print(msg)
        num = input(u"请输入您选择的操作编号：").strip()
        if num == "1":
            username = input(u"请输入用户账号：").strip()
            password = input(u"请输入账号密码：").strip()
            rsp = login(username, password)
            if rsp.code == 200:
                user_id = rsp.data["id"]
                role_id = rsp.data["role_id"]
                HybridViews(user_id, role_id)
            else:
                print(rsp.msg)
        elif num == "2":
            exit()
        else:
            print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))


if __name__ == "__main__":
    console()

