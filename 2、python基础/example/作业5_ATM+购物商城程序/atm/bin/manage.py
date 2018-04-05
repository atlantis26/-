# coding:utf-8
from atm.core.accounts import create_account, frozen_account, thawing_account, reset_account
from atm.core.main import login, logout
from atm.core.auth import is_administrator, auth
from atm.conf.settings import AUTH_FLAG


def admin_login():
    """登录"""
    if AUTH_FLAG["is_authenticated"]:
        msg = u"您当前已经登录系统，无需再次登录"
        print(msg)
        return msg
    account_name = input(u"请输入账户的账号: ")
    password = input(u"请输入密码: ")
    rsp = login(account_name, password)
    msg = rsp.msg
    if rsp.code == 200:
        if not AUTH_FLAG["is_administrator"]:
            msg = "{0}不是管理员，不能登录本后台管理系统".format(AUTH_FLAG["account_name"])
            logout()
    print(msg)


@auth(AUTH_FLAG)
@is_administrator(AUTH_FLAG)
def admin_logout():
    """登出"""
    rsp = logout()
    print(rsp.msg)


@auth(AUTH_FLAG)
@is_administrator(AUTH_FLAG)
def admin_create_account():
    """创建新账户"""
    account_name = input(u"请输入新建账户的账号：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = create_account(account_name, password1, password2)
    print(rsp.msg)


@auth(AUTH_FLAG)
@is_administrator(AUTH_FLAG)
def admin_frozen_account():
    """冻结账户"""
    account_name = input(u"请输入账户的账号：")
    rsp = frozen_account(account_name)
    print(rsp.msg)


@auth(AUTH_FLAG)
@is_administrator(AUTH_FLAG)
def admin_thawing_account():
    """解冻账户"""
    account_name = input(u"请输入账户的账号：")
    rsp = thawing_account(account_name)
    print(rsp.msg)


@auth(AUTH_FLAG)
@is_administrator(AUTH_FLAG)
def admin_reset_account():
    """修改账户密码"""
    account_name = input(u"请输入账户的账号：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = reset_account(account_name, password1, password2)
    print(rsp.msg)


def admin_help():
    """打印操作选项信息"""
    msg = u"""-------------------------------------------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.管理员账号登录                 <\033[36;1m2\033[0m>.登出账户
            <\033[36;1m3\033[0m>.创建新账户                     <\033[36;1m4\033[0m>.冻结账户
            <\033[36;1m5\033[0m>.解冻账户                       <\033[36;1m6\033[0m>.重置账户密码
    """
    print(msg)


def console():
    msg = u"***欢迎使用ATM个人信用金融系统后台管理平台***"
    print(msg)
    action = {"1": admin_login,
              "2": admin_logout,
              "3": admin_create_account,
              "4": admin_frozen_account,
              "5": admin_thawing_account,
              "6": admin_reset_account}
    while True:
        admin_help()
        key = input("请输入操作选项编号>: ")
        if key not in action:
            print(u"输入的操作选项不存在，请核对后再尝试")
            continue
        action[key]()


if __name__ == "__main__":
    console()
