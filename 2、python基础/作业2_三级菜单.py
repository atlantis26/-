# conding:utf-8

MENU_FILE = u"E:\\menu_info.txt"

def console():
    main()

def menu_info(file_path):
    """
    文本中放置的是json格式字符串，是符合三级目录的数据内容
    """
    with open(file_path, "r") as f:
        return eval(f.read())
    
def choose(menu, item):
    if isinstance(menu, dict):
        value = menu[item]
        print(vaule)
        return value
    else:
        msg = u"已经是最后的菜单项，无法再选择..."
        print(msg)
        return

def eof():
    print(u"退出系统...")
    exit()
    
def main():
    menu_info = menu_info(MENU_FILE)
    print(menu_info)
    while True:
        info = choose(menu_info)
        
