# coding:utf-8

USER_INFO = "E:\\user_info.txt"

def console():
    logined = False
    while not logined:
        logined = login()
    do_something()

def login():
    username = input(u"请输入账号: ")
    if not auth_username(username):
        msg = u"用户'{0}'不存在".format(username)
        print(msg)
        return False
    
    count = 0
    while count<3:
        passwd = input(u"请输入密码: ")
        if auth(username, passwd):
            msg = u"欢迎用户'{0}'登陆系统".format(username)
            print(msg)
            return True
        count += 1
        print(u"密码错误...")
    else:
        msg = u"抱歉，你的账号密码已经连续错误3次，账号将被锁定10分钟无法登陆"
        print(msg)
        lock_user(username)

def auth_username(username):
    with open(USER_INFO, 'r') as f:
        for line in f:
            if username == line.split(",")[0].strip():
                return True

def auth(username, passwd):
    """
    假定用户信息文件user_info.txt中存放用户信息格式为单行，账号和密码以逗号分开
    例如：zhangsan,123456
          lisi,123456
    """
    with open(USER_INFO, 'r') as f:
        for line in f:
            if ','.join([username, passwd]) == line.strip():
                return True
            
def lock_user(username):
    pass
            
def do_something():
    print("do something...")

    
if __name__=="__main__":
    a = console()
            
