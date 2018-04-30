# coding:utf-8
import re


def add(item):
    """处理+的运算"""
    p = r'\d+\.?\d*\+\d+\.?\d*'
    while item.count("+") > 0:
        s1 = re.findall(p, item)
        s2 = [str(k[0] + k[1]) for k in
              [[float(j[0].strip()), float(j[1].strip())] for j in [i.split("+") for i in s1]]]
        for i, j in zip(s1, s2):
            item = item.replace(i, j)
        item = replace_calc(item)
    return item


def sub(item):
    """处理-的运算"""
    p = r'\d+\.?\d*\-\d+\.?\d*'
    while item.count("-") > 1 or (item.count("-") == 1 and re.findall(p, item)):
        s1 = re.findall(p, item)
        s2 = [str(k[0] - k[1]) for k in
              [[float(j[0].strip()), float(j[1].strip())] for j in [i.split("-") for i in s1]]]
        for i, j in zip(s1, s2):
            item = item.replace(i, j)
        item = replace_calc(item)
    return item


def multi(item):
    """处理*的运算, 考虑'a*-b'这样的情况，所以正则匹配时加入-？匹配符"""
    p = r'\d+\.?\d*\*-?\d+\.?\d*'
    while item.count("*") > 0:
        s1 = re.findall(p, item)
        s2 = [str(k[0] * k[1]) for k in
              [[float(j[0].strip()), float(j[1].strip())] for j in [i.split("*") for i in s1]]]
        for i, j in zip(s1, s2):
            item = item.replace(i, j)
        item = replace_calc(item)
    return item


def div(item):
    """处理/的运算，考虑'a/-b'这样的情况，所以正则匹配时加入-？匹配符"""
    p = r'\d+\.?\d*\/-?\d+\.?\d*'
    while item.count("/") > 0:
        s1 = re.findall(p, item)
        s2 = [str(k[0] / k[1]) for k in
              [[float(j[0].strip()), float(j[1].strip())] for j in [i.split("/") for i in s1]]]
        for i, j in zip(s1, s2):
            item = item.replace(i, j)
        item = replace_calc(item)
    return item


def calc1(item):
    """最小括号运算内的运算，由于除法分子/分母的特殊性，必须先算除法，再乘法，最后加减法"""
    item = div(item)
    item = multi(item)
    item = add(item)
    item = sub(item)
    return item


def replace_calc(string):
    """进行相连的加减符号间的运算和替换"""
    return string.replace("+-", "-").replace("-+", "-").replace("--", "+").replace("++", "+")


def calc(string):
    """先找到最小单元的括号运算，再分别运算最小括号运算后替换字符串；递归直到算出最后结果"""
    # 先去除所有空格符
    string = string.replace(" ", "")
    p = r'\([^()]+\)'
    lst = re.findall(p, string)
    if len(lst) != 0:
        for item in lst:
            tmp = item.lstrip("(").rstrip(")")
            tmp = calc1(tmp)
            string = string.replace(item, tmp)
        # 进行符号间的运算和替换
        string = replace_calc(string)
        return calc(string)
    else:
        return calc1(string)


if __name__ == "__main__":
    a = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    rsp = calc(a)
    print(rsp)

