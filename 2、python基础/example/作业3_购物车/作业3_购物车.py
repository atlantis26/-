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
        msg = u"抱歉，你的账号密码已经连续错误3次，账号将被锁定10分钟无法登陆"
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
                user_info_lst = user_info
                line = ",".join(user_info_lst) + "\n"
            tmp.write(line)
        tmp.close()
    os.remove(UserInfo)
    os.rename(temp_file, UserInfo)


def update_user_salary(user_info):
    if user_info[2] == "":
        salary = input(u"你是第一次使用本系统，请输入你的薪资金额（元）: ")
        user_info[2] = salary
        update_user_info(user_info)


def get_and_show_products():
    with open(ProductLst, "r") as f:
        products = eval(f.read().strip())
        print(u"商品列表：")
    for id, product in enumerate(products):
        msg = u"{0}    {1}    {2}元".format(id, product[0], product[1])
        print(msg)
    return products


def purchase(products, user_info):
    product_id = int(input(u"请输入要购买商品的编号："))
    product_price = products[product_id]
    if float(product_price) < float(user_info[2]):
        surplus_salary = float(user_info[2]) - float(product_price)
        user_info[2] = surplus_salary
        msg = u"用户{0}成功购买商品{1},花费{2}元,剩余薪资{3}元"\
              .format(user_info[0], products[product_id][0], products[product_id][1], surplus_salary)
        print(msg)
        update_user_salary(user_info)
        update_purchase_history(msg)
    else:
        print(u"你的剩余薪资为{0}，不能够购买商品{1}".format(user_info[2], products[product_id][0]))


def update_purchase_history(purchase_history):
    pass


def work_flow():
    user_info = None
    while not user_info:
        user_info = login()
    update_user_salary(user_info)
    products = get_and_show_products()
    purchase(products, user_info)


def console():
    work_flow()


if __name__ == "__main__":
    console()