# coding:utf-8
from conf.settings import DB_Users, DB_Flows_History
from core.orm import ResponseData
import pickle
import os
import logging

logger = logging.getLogger("course_system.db")


def load_user_pkl(name):
    """加载用户数据,文件读取对象pkl字符串，并重构存储对象"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(name))
    if not os.path.exists(user_file):
        code = 400
        msg = u"加载用户{0}数据失败,无此用户信息".format(name)
        data = None
    else:
        rsp = load_pkl(user_file)
        code = 200
        msg = u"加载用户{0}数据成功".format(name)
        data = rsp.data
    logger.debug(ResponseData(code, msg, data.__dict__).__dict__)

    return ResponseData(code, msg, data)


def save_user_pkl(user):
    """保存用户数据，文件存储保存对象的pkl字符串"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(user.name))
    rsp = save_pkl(user, user_file)
    if rsp.code == 200:
        code = 200
        msg = u"保存用户{0}数据成功,详细：{1}".format(user.name, user.__dict__)
    else:
        code = 400
        msg = u"保存用户{0}数据失败".format(user.name)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def load_flow_pkl(name):
    """加载用户流水数据,文件读取对象pkl字符串，并重构存储对象"""
    user_flow_dir = os.path.join(DB_Flows_History, name)
    if not os.path.exists(user_flow_dir):
        code = 400
        msg = u"加载用户{0}的消费流水数据失败，无流水数据".format(name)
        data = None
    else:
        data = list()
        for root, dirs, files in os.walk(user_flow_dir):
            for file in files:
                rsp = load_pkl(os.path.join(root, file))
                name = rsp.data
                data.append(name)
        code = 200
        msg = u"加载用户{0}消费流水数据成功,详细：{1}".format(name, [flow.__dict__ for flow in data])
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)


def save_flow_pkl(flow):
    """保存用户流水数据，文件存储保存对象的pkl字符串"""
    user_flow_dir = os.path.join(DB_Flows_History, flow.user_name)
    if not os.path.exists(user_flow_dir):
        os.mkdir(user_flow_dir)
    user_flow_file = os.path.join(user_flow_dir, "{0}.pkl".format(flow.time_stamp))
    rsp = save_pkl(flow, user_flow_file)
    if rsp.code == 200:
        code = 200
        msg = u"保存用户{0}的消费流水数据成功,详细：{1}".format(flow.user_name, flow.__dict__)
    else:
        code = 400
        msg = u"保存用户{0}的消费流水数据失败".format(flow.user_name)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def load_pkl(file_path):
    """加载pkl数据,文件读取对象pkl字符串，并重构存储对象"""
    if not os.path.exists(file_path):
        code = 400
        msg = u"加载pkl文件{0}的数据失败".format(file_path)
        data = None
    else:
        with open(file_path, 'r') as f:
            data = pickle.load(f)
        code = 200
        msg = u"加载pkl文件{0}的数据成功".format(file_path)
    logger.debug(ResponseData(code, msg, data.__dict__).__dict__)

    return ResponseData(code, msg, data)


def save_pkl(obj, file_path):
    """保存pkl数据，文件存储保存对象的pkl字符串"""
    with open(file_path, 'w') as f:
        pickle.dump(obj, f)
        f.flush()
    code = 200
    msg = u"保存对象的pkl字符串到文件{0}内成功，对象详细：{1}".format(file_path, obj.__dict__)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


