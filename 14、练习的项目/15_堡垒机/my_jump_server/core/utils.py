# coding:utf-8
import yaml
import os
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def yaml_parser(yml_filename):
    """解析yml文件内容转为字典数据"""
    try:
        if not os.path.exists(yml_filename):
            raise SomethingError(u"配置文件不存在")
        yml_file = open(yml_filename, 'r')
        data = yaml.load(yml_file)
        return data
    except Exception as e:
        raise SomethingError(u"解析配置文件失败，原因：{0}".format(str(e)))


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomethingError(Exception):
    """自定义异常错误"""
    pass

