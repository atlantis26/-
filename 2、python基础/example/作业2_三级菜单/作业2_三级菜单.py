# coding:utf-8
import os

MENU_FILE = os.path.join(os.path.curdir, "menu_info.txt")


def init_menu(file_path):
    with open(file_path, "r") as f:
        return eval(f.read().strip())


def print_menu(menu):
    if not isinstance(menu, (dict, list)):
        print("已经没有可选菜单项")
    else:
        for i in menu:
            print(i)
    msg = u'''
    ***********************************
    输入<EOF>: 退出菜单系统
    输入<REBACK>: 返回上一级菜单
    输入某一菜单项: 进入下一级菜单
    ***********************************'''
    print(msg)


def get_current_menu(menu, menu_depth):
    """
    通过菜单和菜单深度表，生成当前所在一级的子菜单；
    注意：这里遇坑了,传递的参数menu_depth实际与我的全局变量menu_depth在内存中是同一个对象，虽然是对传参使用
    pop（）方法但实际会修改这个对象，但并不要修改对象，知识要生成子菜单，所以通过分片赋值获得新的对象,解决问题
    """
    depth = menu_depth[:]
    if len(depth) != 0:
        key = depth.pop(0)
        current_menu = menu[key]
        return get_current_menu(current_menu, depth)
    else:
        current_menu = menu
    return current_menu


def next_menu(menu, menu_depth, item):
    """
    根据当前菜单与输入菜单项，修改菜单深度表，
    """
    if item in menu:
        if isinstance(menu, dict):
            menu_depth.append(item)
        elif isinstance(menu, list):
            print(u"已经处于最底层菜单，无法再选择，请重新选择或返回上一级菜单")
        else:
            print(u"菜单系统有误，请联系管理员")
    else:
        print(u"输入菜单项不存在或者不是当前可选项，请重新选择进入")
    return menu_depth


def last_menu(menu_depth):
    depth = menu_depth[:]
    if len(depth) != 0:
        depth.pop()
    else:
        print(u"已经是最上级菜单,不能再返回上一级")
    return depth


def work_flow(menu):
    """
    定义一个菜单深度表menu_depth，以便做出‘选择进入’操作后，定位应该停留在菜单的位置
    """
    menu_depth = list()
    while True:
        current_menu = get_current_menu(menu, menu_depth)
        print_menu(current_menu)
        item = input(u"请选择进入：")
        if item == "EOF":
            print(u"感谢使用本菜单系统，欢迎再次使用")
            exit()
        elif item == "REBACK":
            menu_depth = last_menu(menu_depth)
        else:
            menu_depth = next_menu(current_menu, menu_depth, item)


def console():
    menu = init_menu(MENU_FILE)
    work_flow(menu)


if __name__ == "__main__":
    console()
