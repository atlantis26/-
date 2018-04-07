# coding:utf-8
from conf.setting import StaffFields, StaffTable, DB_DIR
from orm import ResponseData
import os


def get_all_item_index(items):
    """解析sql查询项，返回查询项的索引列表"""
    if items == "*":
        items = StaffFields
    else:
        items = [i.strip() for i in items.split(",")]
    return [StaffFields.index(i) for i in items]


def get_item_index(item):
    """获得查询条件项在单条表数据的索引"""
    return StaffFields.index(item)


def select_like(condition):
    """执行like条件查询，返回符合条件员工的全部信息"""
    user_list = list()
    condition = [i.strip().strip("'").strip('"') for i in condition.split("like")]
    index = get_item_index(condition[0])
    with open(StaffTable, "r") as table:
        for line in table:
            user_info = line.strip().split(",")
            if condition[1] in user_info[index]:
                user_list.append(user_info)
    return user_list


def select_eq(condition):
    """执行'='条件查询，返回符合条件员工的全部信息"""
    user_list = list()
    condition = [i.strip().strip("'").strip('"') for i in condition.split("=")]
    index = get_item_index(condition[0])
    with open(StaffTable, "r") as table:
        for line in table:
            user_info = line.strip().split(",")
            if user_info[index] == condition[1]:
                user_list.append(user_info)
    return user_list


def select_gt(condition):
    """执行'>'条件查询，返回符合条件员工的全部信息"""
    user_list = list()
    condition = [i.strip().strip("'").strip('"') for i in condition.split(">")]
    index = get_item_index(condition[0])
    with open(StaffTable, "r") as table:
        for line in table:
            user_info = line.strip().split(",")
            if user_info[index] > condition[1]:
                user_list.append(user_info)
    return user_list


def select_lt(condition):
    """执行'<'条件查询，返回符合条件员工的全部信息"""
    user_list = list()
    condition = [i.strip().strip("'").strip('"') for i in condition.split("<")]
    index = get_item_index(condition[0])
    with open(StaffTable, "r") as table:
        for line in table:
            user_info = line.strip().split(",")
            if user_info[index] < condition[1]:
                user_list.append(user_info)
    return user_list


def select_ne(condition):
    """执行'!='条件查询，返回符合条件员工的全部信息"""
    user_list = list()
    condition = [i.strip().strip("'").strip('"') for i in condition.split("!=")]
    index = get_item_index(condition[0])
    with open(StaffTable, "r") as table:
        for line in table:
            user_info = line.strip().split(",")
            if user_info[index] != condition[1]:
                user_list.append(user_info)
    return user_list


def select_le():
    """执行'<='条件查询，返回符合条件员工的全部信息"""
    pass


def select_ge():
    """执行'>='条件查询，返回符合条件员工的全部信息"""
    pass


def get_last_staff_id():
    """读取信息存储文件内容"""
    count = 0
    with open(StaffTable, "r") as f:
        for line in f:
            count += 1
    return count


def phone_is_exists(phone):
    """检查电话号码是否已存在"""
    flag = False
    with open(StaffTable, "r") as f:
        phone_index = StaffFields.index("phone")
        for line in f:
            if phone == line.strip().split(",")[phone_index]:
                flag = True
    return flag


def user_is_exists_by_id(staff_id):
    """检查电话号码是否已存在"""
    flag = False
    with open(StaffTable, "r") as f:
        staff_id_index = StaffFields.index("staff_id")
        for line in f:
            if staff_id == line.strip().split(",")[staff_id_index]:
                flag = True
    return flag


def execute_condition(condition):
    """解析sql查询条件, 执行查询"""
    if "like" in condition:
        code = 200
        msg = "查询成功"
        data = select_like(condition)
    elif "=" in condition:
        code = 200
        msg = "查询成功"
        data = select_eq(condition)
    elif ">" in condition:
        code = 200
        msg = "查询成功"
        data = select_gt(condition)
    elif "<" in condition:
        code = 200
        msg = "查询成功"
        data = select_lt(condition)
    else:
        code = 400
        msg = u"暂不支持此sql语句查询条件，请核对后再试"
        data = None

    return ResponseData(code, msg, data)
