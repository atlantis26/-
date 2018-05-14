# coding:utf-8
import sys
import hashlib


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    """自定义异常错误"""
    pass


def show_process(total_size, sub_size, total_arrow=50):
    """打印进度条"""
    percent = float(sub_size)/float(total_size)
    arrow_num = int(total_arrow * percent)
    line_num = total_arrow - arrow_num
    process_bar = "[{0}{1}]{2}%".format(">" * arrow_num, "-" * line_num, "%.2f" % (percent*100))
    sys.stdout.write("\r")
    sys.stdout.flush()
    # 先输入\r移动光标到最左侧且不会换行，再输入进度条字符串
    sys.stdout.write(process_bar)
    sys.stdout.flush()


def get_file_md5(file_path):
    """计算文件md5 code"""
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for line in f:
            md5.update(line)
    return md5.hexdigest()
