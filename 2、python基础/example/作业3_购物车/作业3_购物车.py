# coding:utf-8
import  os

ProductLst = os.path.join(os.path.curdir, "products.txt")
UserInfo = os.path.join(os.path.curdir, "user.txt")
PurchaseHistory = os.path.join(os.path.curdir, "purchase_history.txt")


def login():
    username = input(u"请输入账号: ")
    if not auth_username(username):
        msg = u"用户'{0}'不存在".format(username)
        print(msg)
        return False
    count = 0
    while count < 3:
        password = input(u"请输入密码: ")
        if auth(username, password):
            msg = u"欢迎用户'{0}'登陆系统".format(username)
            print(msg)
            return True
        count += 1
        print(u"密码错误...")
    else:
        msg = u"抱歉，你的账号密码已经连续错误3次，账号将被锁定10分钟无法登陆"
        print(msg)
        lock_user(username)

def lock_user(username):
    pass


def auth_username(username):
    with open(UserInfo, 'r') as f:
        for line in f:
            if username == line.strip().split(",")[1]:
                return True


def auth(username, password):
    with open(UserInfo, 'r') as f:
        for line in f:
            if if username == line.strip().split(",")[1] and :
                return True


def init_users(file_path, username, password):
    """
    假定用户信息文件user.txt中存放单个用户信息格式为一行，类似数据库的结构，字段间逗号分开，不同列为不同字段信息
    例如：编号id,用户名，密码，工资余额
          1,zhangsan,123456,10000
          2,lisi,123456,
    """
    with open(file_path, "r+") as f:
        for line in f:
            user_info = line.strip().split(",")
            if username == user_info[1]:





def show_product_list():
    pass


def read_file():
    def payment():
        """
        结算操作
        :return:
        """
        pass


def console():
    pass