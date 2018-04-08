# coding:utf-8
from common import *
import re


def select():
    """暂时只支持‘like’、‘=’、‘>’、‘<’ 4种查询条件的查询"""
    sql = input(u"请输入sql查询语句：")
    p = r'select\s+(?P<items>.*?)\s+from\s+(?P<table>.*?)\s+where\s+(?P<condition>.*?)$'
    result = re.search(p, sql)
    data = list()
    if result:
        items = result.group("items").strip()
        index_lst = get_all_item_index(items)
        condition = result.group("condition").strip()
        rsp = execute_condition(condition)
        if rsp.code == 200:
            for user in rsp.data:
                data.append([user[i] for i in index_lst])
            msg = u"查询成功，共查询到{0}条信息".format(len(data))
        else:
            msg = rsp.msg
    else:
        msg = u"sql查询语句语法有误，请核对后再试"
    for user in data:
        print(user)
    print(msg)


def create():
    """创建员工信息"""
    name = input(u"请输入员工姓名：")
    age = input(u"请输入员工年龄：")
    phone = input(u"请输入员工手机号：")
    dept = input(u"请输入所属部门：")
    enroll_date = input(u"请输入入职日期：")
    staff_id = str(get_last_staff_id() + 1)
    user = ",".join([staff_id, name, age, phone, dept, enroll_date]) + "\n"
    if not phone_is_exists(phone):
        with open(StaffTable, "a") as f:
            f.write(user)
            f.flush()
        msg = u"创建新员工信息成功"
    else:
        msg = u"创建新员工信息失败，手机号已经存在"
    print(msg)


def modify():
    """修改员工信息"""
    p = r'UPDATE\s+(?P<staff_table>.*?)\s+SET\s+(?P<new_kv>.*?)\s+where\s+(?P<kv>.*?)$'
    sql = input(u"请输入sql修改信息语句：")
    result = re.search(p, sql)
    if result:
        new_kv = [i.strip().strip("'").strip('"') for i in result.group("new_kv").split("=")]
        kv = [i.strip().strip("'").strip('"') for i in result.group("kv").split("=")]
        temp_file = os.path.join(DB_DIR, "db", "staff_tmp.txt")
        key_index = StaffFields.index(kv[0])
        new_kv_index = StaffFields.index(new_kv[0])
        tmp = open(temp_file, "w")
        with open(StaffTable, 'r') as f:
            for line in f:
                user = line.strip().split(",")
                if user[key_index] == kv[1]:
                    user[new_kv_index] = new_kv[1]
                    line = ",".join(user) + "\n"
                tmp.write(line)
                tmp.flush()
            tmp.close()
        os.remove(StaffTable)
        os.rename(temp_file, StaffTable)
        msg = u"修改员工信息成功"
    else:
        msg = u"修改员工信息失败，请核对sql语句是否有效"
    print(msg)


def delete():
    """删除员工信息"""
    staff_id = input(u"请输入员工id：")
    if user_is_exists_by_id(staff_id):
        temp_file = os.path.join(DB_DIR, "db", "staff_tmp.txt")
        tmp = open(temp_file, "w")
        with open(StaffTable, 'r') as f:
            for line in f:
                user = line.strip().split(",")
                if user[0] == staff_id:
                    continue
                tmp.write(line)
                tmp.flush()
            tmp.close()
        os.remove(StaffTable)
        os.rename(temp_file, StaffTable)
        msg = u"删除员工信息成功"
    else:
        msg = "删除员工信息失败，输入的员工id不存在"
    print(msg)


def console_help():
    """打印操作选项信息"""
    msg = u"""-------------------------------------------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.sql语句查询员工信息
            <\033[36;1m2\033[0m>.创建新员工信息
            <\033[36;1m3\033[0m>.sql语句修改员工信息                     
            <\033[36;1m4\033[0m>.删除员工信息
    """
    print(msg)


def console():
    msg = u"***欢迎访问员工信息管理系统***"
    print(msg)
    action = {"1": select,
              "2": create,
              "3": modify,
              "4": delete}
    while True:
        console_help()
        key = input("请输入操作选项编号>: ")
        if key not in action:
            print(u"输入的操作选项不存在，请核对后再尝试")
            continue
        action[key]()


if __name__ == "__main__":
    console()
