# coding:utf-8
from atm.core.main import login, logout, withdraw, repayment, transfer, history, balance, reset
from atm.core.auth import auth
from atm.conf.settings import AUTH_FLAG


def console_login():
    """登录"""
    account_name = input(u"请输入账号: ")
    password = input(u"请输入密码: ")
    rsp = login(account_name, password)
    print(rsp.msg)


@auth(AUTH_FLAG)
def console_logout():
    """登出"""
    rsp = logout()
    print(rsp.msg)


@auth(AUTH_FLAG)
def console_withdraw():
    """取现"""
    money = eval(input(u"请输入取现金额（收取5%的手续费）： "))
    rsp = withdraw(money)
    print(rsp.msg)


@auth(AUTH_FLAG)
def console_repayment():
    """还款/存钱"""
    money = eval(input(u"请输入还款\存款的金额： "))
    rsp = repayment(money)
    print(rsp.msg)


@auth(AUTH_FLAG)
def console_transfer():
    """转账"""
    account = input(u"请输入对方的账户名： ")
    money = eval(input(u"请输入转账的金额： "))
    rsp = transfer(account, money)
    print(rsp.msg)


@auth(AUTH_FLAG)
def console_flow_history():
    """根据月份查询账户消费流水历史记录"""
    year = input(u"请输入年份（例如：2018）： ")
    month = input(u"请输入月份（例如：4）： ")
    rsp = history(year, month)
    if rsp.code == 200:
        for flow in rsp.data:
            print(flow)
    else:
        print(rsp.msg)


@auth(AUTH_FLAG)
def console_balance():
    """查询个人当前账户余额"""
    rsp = balance()
    print(rsp.msg)


def console_help():
    """打印操作选项信息"""
    msg = u"""-------------------------------------------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.登录账户                      <\033[36;1m2\033[0m>.登出账户
            <\033[36;1m3\033[0m>.存钱/还款                     <\033[36;1m4\033[0m>.取现
            <\033[36;1m5\033[0m>.转账                          <\033[36;1m6\033[0m>.按月查询账户流水信息
            <\033[36;1m7\033[0m>.查询账户余额
    """
    print(msg)


def console():
    msg = u"***欢迎使用ATM个人信用金融系统***"
    print(msg)
    action = {"1": console_login,
              "2": console_logout,
              "3": console_repayment,
              "4": console_withdraw,
              "5": console_transfer,
              "6": console_flow_history,
              "7": console_balance}
    while True:
        console_help()
        key = input("请输入操作选项编号>: ")
        if key not in action:
            print(u"输入的操作选项不存在，请核对后再尝试")
            continue
        action[key]()


if __name__ == "__main__":
    console()
