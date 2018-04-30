# coding:utf-8
import os

InfoFile = os.path.join(os.path.curdir, "info.txt")


def query():
    username = input(u"请输入要查询的员工姓名:")
    with open(InfoFile, "r") as f:
        for line in f:
            user = line.strip().split(" ")
            if user[0] == username:
                return u"{0}的工资是：{1}。".format(user[0], user[1])
    return u"员工'{0}'不存在，请核对后再尝试".format(username)


def modify():
    info = input(u"请输入要修改的员工姓名和工资，用空格分隔（例如：Alex 10）:")
    user_info = info.strip().split(" ")
    if len(user_info) != 2:
        return u"输入数据格式有误，修改失败，请核对后再试"
    if not user_is_exist(user_info[0]):
        return u"员工'{0}'不存在，请核对后再尝试".format(user_info[0])
    temp_file = os.path.join(os.path.curdir, "info_temp.txt")
    tmp = open(temp_file, 'w')
    with open(InfoFile, "r+") as f:
        for line in f:
            user = line.strip().split(" ")
            if user[0] == user_info[0]:
                line = " ".join(user_info)
            tmp.write(line)
        tmp.close()
    os.remove(InfoFile)
    os.rename(temp_file, InfoFile)
    return u"修改成功！"


def insert():
    info = input(u"请输入要增加的员工姓名和工资，共空格分割（例如：Eric 100000）:")
    user_info = info.strip().split(" ")
    if len(user_info) != 2:
        return u"输入数据格式有误，新增失败，请核对后再试"
    if user_is_exist(user_info[0]):
        return u"员工'{0}'已存在，请核对后再尝试".format(user_info[0])
    with open(InfoFile, "a") as f:
        f.write(" ".join(user_info) + "\n")
    return u"增加成功！"


def user_is_exist(username):
    with open(InfoFile, 'r') as f:
        for line in f:
            user_info = line.strip().split(" ")
            if username == user_info[0]:
                return True


def validate_info():
    with open(InfoFile, 'r') as f:
        for line in f:
            user_info = line.strip().split(" ")
            if len(user_info) == 1 and user_info[0] == "":
                pass
            elif len(user_info) == 2:
                pass
            else:
                raise Exception(u"用户表内数据格式有误，请联系管理员，错误信息：'{0}'".format(line))


def work_flow():
    while True:
        msg = u'''
    ************************************************************
        1. 查询员工工资                       2. 修改员工工资

        3. 增加新员工记录                     4. 退出
    ************************************************************'''
        print(msg)
        item = input(u"请输入编号进行操作>>：")
        if item == "1":
            print(query())
        elif item == "2":
            print(modify())
        elif item == "3":
            print(insert())
        elif item == "4":
            print(u"再见！")
            break
        else:
            print(u"编号不存在，请核对后再重新输入")


def console():
    validate_info()
    work_flow()


if __name__ == "__main__":
    console()