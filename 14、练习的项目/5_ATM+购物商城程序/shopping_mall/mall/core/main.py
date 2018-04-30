# coding:utf-8
from atm.core.accounts import create_account
from atm.core.auth import auth
from atm.conf.settings import AUTH_FLAG
from atm.core.main import login, logout, balance, reset
from mall.core.products import purchase_product, purchase_flow, get_products, query_purchase_flow
from mall.conf.settings import ATM_ADMIN
from mall.core.orm import ResponseData
import logging


logger = logging.getLogger("mall.main")


def user_register():
    """注册新账户"""
    name = input(u"请输入新账户名：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = login(ATM_ADMIN["account_name"], ATM_ADMIN["password"])
    logger.debug(rsp.__dict__)
    balances = 15000
    if rsp.code == 200:
        rsp = create_account(name, password1, password2, balances)
        if rsp.code == 200:
            code = 200
            msg = "注册账户成功，账户为：{0},账户初始信用额度为{1}元".format(name, balances)
        else:
            code = rsp.code
            msg = rsp.msg
        logout()
    else:
        code = 400
        msg = "注册账户失败，连接后台管理平台失败，请联系管理员"
    logger.debug(ResponseData(code, msg).__dict__)

    print(msg)


def user_login():
    """登录"""
    if AUTH_FLAG["is_authenticated"]:
        msg = u"您当前已经登录系统，无需多次登录；如果需要登录其他账号，请先登出再尝试"
        print(msg)
        return
    name = input(u"请输入账户名: ")
    password = input(u"请输入密码: ")
    rsp = login(name, password)
    if rsp.code == 200:
        code = 200
        msg = u"账户{0}成功登录，欢迎您访问懒猫网上购物商城".format(name)
    else:
        code = rsp.code
        msg = rsp.msg
    logger.debug(ResponseData(code, msg).__dict__)

    print(msg)


@auth(AUTH_FLAG)
def user_logout():
    """登出"""
    rsp = logout()
    logger.debug(rsp.__dict__)

    print(rsp.msg)


@auth(AUTH_FLAG)
def user_modify():
    """修改账户密码"""
    password0 = input(u"请输入账户原密码：")
    password1 = input(u"请输入设置新密码：")
    password2 = input(u"请再次输入设置新密码：")
    rsp = reset(password0, password1, password2)
    logger.debug(rsp.__dict__)

    print(rsp.msg)


@auth(AUTH_FLAG)
def purchase():
    """购物"""
    product_id = eval(input(u"请输入商品的编号:").strip())
    rsp = purchase_product(product_id)
    if rsp.code == 200:
        rsp1 = purchase_flow(AUTH_FLAG["account_name"], u"购买商品", rsp.msg)
        if rsp1.code == 200:
            code1 = 200
            msg1 = u"购买商品成功，生成购物流水成功，原因：{0}".format(rsp1.msg)
        else:
            code1 = 400
            msg1 = u"购买商品成功，但是生成购物流水失败，原因：{0}".format(rsp1.msg)
        logger.debug(ResponseData(code1, msg1).__dict__)
    logger.debug(rsp.__dict__)

    print(rsp.msg)


def show_products():
    """打印显示商品列表"""
    rsp = get_products()
    if rsp.code == 200:
        for index, product in enumerate(rsp.data):
            msg1 = u"\033[31;1m{0}\033[0m    {1}    {2}元".format(index, product[0], product[1])
            print(msg1)
        code = 200
        msg = u"查询商品列表信息成功，详情：{0}".format(rsp.msg)
    else:
        code = 400
        msg = u"查询商品列表信息失败，原因：{0}".format(rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)


@auth(AUTH_FLAG)
def show_history():
    """根据月份查询购物消费流水历史记录"""
    year = input(u"请输入年份（例如：2018）： ")
    month = input(u"请输入月份（例如：4）： ")
    rsp = query_purchase_flow(AUTH_FLAG["account_name"], year, month)
    if rsp.code == 200:
        for flow in rsp.data:
            print(flow)
    else:
        print(rsp.msg)
    logger.debug(rsp.__dict__)


@auth(AUTH_FLAG)
def show_balance():
    """查询账户当前余额"""
    rsp = balance()
    logger.debug(rsp.__dict__)
    print(rsp.msg)


def console_help():
    """打印操作选项信息"""
    msg = u"""-------------------------------------------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.注册账户                      <\033[36;1m2\033[0m>.账户登录
            <\033[36;1m3\033[0m>.浏览商品列表                  <\033[36;1m4\033[0m>.购买商品
            <\033[36;1m5\033[0m>.按月查询购物流水信息           <\033[36;1m6\033[0m>.查询账户余额
            <\033[36;1m7\033[0m>.账户登出                      <\033[36;1m8\033[0m>.修改密码
    """
    print(msg)


def console():
    msg = u"********欢迎访问懒猫网上购物商城*******"
    print(msg)
    action = {"1": user_register,
              "2": user_login,
              "3": show_products,
              "4": purchase,
              "5": show_history,
              "6": show_balance,
              "7": user_logout,
              "8": user_modify}
    while True:
        console_help()
        key = input("请输入操作选项编号>: ")
        if key not in action:
            print(u"输入的操作选项不存在，请核对后再尝试")
            continue
        action[key]()


if __name__ == "__main__":
    console()
