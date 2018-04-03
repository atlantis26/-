# coding:utf-8
from atm.core.main import *


def console_login():
    """登录"""
    account_name = input(u"请输入账号: ")
    password = input(u"请输入密码: ")
    rsp = login(account_name, password)
    print(rsp.msg)


def console_logout():
    """登出"""
    rsp = logout()
    print(rsp.msg)


def console_create_account():
    """创建新用户"""
    account_name = input(u"请输入新建账户的账号：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = create_account(account_name, password1, password2)
    print(rsp.msg)


def console_withdraw():
    """取现"""
    money = input(u"请输入取现金额（收取5%的手续费）： ")
    rsp = withdraw(money)
    print(rsp.msg)


def console_repayment():
    """还款/存钱"""
    money = input(u"请输入还款\存款的金额： ")
    rsp = repayment(money)
    print(rsp.msg)


def console_transfer():
    """转账"""
    account = input(u"请输入对方的账户名： ")
    money = input(u"请输入转账的金额： ")
    rsp = transfer(account, money)
    print(rsp.msg)


def console_flow_history():
    """根据日期查询个人消费流水历史记录"""
    year = input(u"请输入年份（比如：2018）： ")
    month = input(u"请输入月份（比如：1）： ")
    rsp = history(year, month)
    print(rsp.msg)


def console_balance():
    """查询个人当前账户余额"""
    rsp = balance()
    print(rsp.msg)


def console_help():
    """打印操作选项信息"""
    msg = u"""您可以选择如下操作：
            1.登录账户                         2.登出账户
            3.新建账户                         4.还款/存钱
            5.取现                             6.转账
            7.按月查询个人账户流水信息          8.查询账户余额
    """
    print(msg)


def console():
    msg = u"***欢迎使用ATM个人信用金融系统***"
    print(msg)
    action = {"1": console_login,
              "2": console_logout,
              "3": console_create_account,
              "4": console_repayment,
              "5": console_withdraw,
              "6": console_transfer,
              "7": console_flow_history,
              "8": console_balance}
    while True:
        console_help()
        key = input("请输入操作选项编号>: ")
        if key not in action:
            print(u"输入的操作选项不存在，请核对后再尝试")
            continue
        action[key]()


if __name__ == "__main__":
    console()
