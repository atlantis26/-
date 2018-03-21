# coding:utf-8
import  os

ProductLst = os.path.join(os.path.curdir, "products.txt")
UserInfo = os.path.join(os.path.curdir, "user.txt")
PurchaseHistory = os.path.join(os.path.curdir, "purchase_history.txt")


def login():
    username = input(u"请输入账号: ")
    user_info = auth_username(username)
    if not user_info:
        msg = u"用户'{0}'不存在".format(username)
        print(msg)
        return False
    count = 0
    while count < 3:
        password = input(u"请输入密码: ")
        if username == user_info[0] and password == user_info[1]:
            msg = u"欢迎用户'{0}'登陆系统".format(username)
            print(msg)
            update_user_salary(user_info)
            return user_info
        count += 1
        print(u"密码错误...")
    else:
        msg = u"抱歉，您的账号密码已经连续错误3次，账号将被锁定10分钟无法登陆"
        print(msg)
        lock_user(username)


def lock_user(username):
    pass


def auth_username(username):
    """
    假定用户信息文件user.txt中存放单个用户信息格式为一行，类似数据库的结构，字段间逗号分开，不同列为不同字段信息
    例如：用户名，密码，工资余额
          zhangsan,123456,10000
          lisi,123456,
    """
    with open(UserInfo, 'r') as f:
        for line in f:
            user_info = line.strip().split(",")
            if len(user_info) != 3:
                print(u"用户表信息有错误，请联系管理员")
                return False
            if username == user_info[0]:
                return user_info


def update_user_info(user_info):
    temp_file = os.path.join(os.path.curdir, "user_temp.txt")
    tmp = open(temp_file, 'w')
    with open(UserInfo, 'r+') as f:
        for line in f:
            user_info_lst = line.strip().split(",")
            if user_info_lst[0] == user_info[0]:
                line = ",".join([str(i) for i in user_info]) + "\n"
            tmp.write(line)
        tmp.close()
    os.remove(UserInfo)
    os.rename(temp_file, UserInfo)


def update_user_salary(user_info):
    if user_info[2] == "":
        while True:
            salary = input(u"您是第一次使用本系统，请输入您的薪资金额（元）: ")
            try:
                salary = eval(salary)
            except Exception as e:
                pass
            if isinstance(salary, (int, float)):
                if float(salary) > 0:
                    user_info[2] = salary
                    break
                else:
                    print(u"薪资必须大于\033[31;1m0\033[0m的数字，请重新输入")
            else:
                print(u"薪资必须输入数字，请重新输入")
    update_user_info(user_info)


def get_and_show_products():
    with open(ProductLst, "r") as f:
        products = eval(f.read().strip())
        print(u"商品列表：")
    for id, product in enumerate(products):
        msg = u"\033[31;1m{0}\033[0m    {1}    {2}元".format(id, product[0], product[1])
        print(msg)
    return products


def purchase(products, user_info, product_id):
    if product_id > len(products)-1 or product_id < 0:
        print(u"商品编号不存在，请仔细查看后再选择")
        return
    p_name = products[product_id][0]
    p_price = products[product_id][1]
    current_salary = user_info[:][2]
    if float(p_price) <= float(user_info[2]):
        surplus_salary = float(user_info[2]) - float(p_price)
        user_info[2] = surplus_salary
        msg = u"您成功购买商品\033[31;1m{0}\033[0m,花费\033[31;1m{1}\033[0m元,账户余额为\033[31;1m{2}\033[0m元"\
              .format(products[product_id][0], products[product_id][1], surplus_salary)
        print(msg)
        update_user_salary(user_info)
        save_purchase_history(user_info[0], p_name, p_price, current_salary, surplus_salary)
    else:
        print(u"您的账户余额为\033[31;1m{0}\033[0m元，不能够购买商品\033[31;1m{1}\033[0m"
              .format(user_info[2], products[product_id][0]))


def save_purchase_history(username, product_name, product_price, current_salary, surplus_salary):
    with open(PurchaseHistory, "a+") as f:
        lst = [str(i) for i in [username, product_name, product_price, current_salary, surplus_salary]]
        history = ",".join(lst) + "\n"
        f.write(history)


def query_purchase_history(username):
    with open(PurchaseHistory, "r") as f:
        print("已购买商品历史记录：")
        for line in f:
            history = line.strip().split(",")
            if username == history[0]:
                msg = u"商品:\033[31;1m{0}\033[0m  价格:\033[31;1m{1}\033[0m元  " \
                      u"账户当前金额:\033[31;1m{2}\033[0m元  账户余额：\033[31;1m{3}\033[0m元"\
                .format(history[1], history[2], history[3], history[4])
                print(msg)


def query_user_salary(username):
    with open(UserInfo, "r") as f:
        for line in f:
            user_info = line.strip().split(",")
            if username == user_info[0]:
                salary = user_info[2]
                print(u"您的当前账户余额为：\033[31;1m{0}\033[0m元".format(salary))


def work_flow():
    # 用户登录, 获得用户信息
    user_info = None
    while not user_info:
        user_info = login()
    products = get_and_show_products()
    while True:
        msg = u'''
    *******************************************************************************
        输入<\033[35;1mP\033[0m>: 显示商品列表                   输入<\033[35;1mQ\033[0m>: 查询用户当前余额
        输入<\033[35;1mH\033[0m>: 查询历史购物记录               输入商品\033[35;1m数字编号\033[0m: 购买该商品
        输入<\033[35;1mEOF\033[0m>: 退出购物系统
    *******************************************************************************'''
        print(msg)
        # 根据用户输入进行操作
        item = input(u"请输入您的操作或商品编号：")
        try:
            item = eval(item)
        except Exception as e:
            # 确保item是数字则转换为int或float类型，如果是非数字则保持原数据类型
            pass
        if item == "EOF":
            print("感谢您使用本购物系统，欢迎再次光临...")
            query_purchase_history(user_info[0])
            break
        elif item == "P":
            get_and_show_products()
        elif item == "Q":
            query_user_salary(user_info[0])
        elif item == "H":
            query_purchase_history(user_info[0])
        elif isinstance(item, int):
            purchase(products, user_info, item)
        else:
            print(u"输入值是不存在的选项，请重新输入")


def console():
    while True:
        work_flow()


if __name__ == "__main__":
    console()