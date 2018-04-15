# coding:utf-8
from conf.settings import DB_Users, DB_Flows_History, DB_Schools
from core.orm import SomeError
import pickle
import os
import logging

logger = logging.getLogger("atm.users")


def load_user_pkl(name):
    """加载用户数据,文件读取对象pkl字符串，并重构存储对象"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(name))
    if not os.path.exists(user_file):
        msg = u"加载用户{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    with open(user_file, 'r') as f:
        data = pickle.load(f)
        msg = u"加载用户{0}数据成功".format(name)
        logger.debug(msg)
    return data


def save_user_pkl(user):
    """保存用户数据，文件存储保存对象的pkl字符串"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(user.name))
    with open(user_file, 'w') as f:
        pickle.dump(user, f)
        f.flush()
    msg = u"保存用户{0}数据成功".format(user.name)
    logger.debug(msg)


def load_flow_pkl(name):
    """加载用户流水数据,文件读取对象pkl字符串，并重构存储对象"""
    user_flow_dir = os.path.join(DB_Flows_History, name)
    if not os.path.exists(user_flow_dir):
        msg = u"加载用户{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    flow_file_list = list()
    for root, dirs, files in os.walk(user_flow_dir):
        for file in files:
            flow_file = os.path.join(root, file)
            with open(flow_file, 'r') as f:
                data = pickle.load(f)
                flow_file_list.append(data)
    msg = u"加载用户{0}数据成功".format(name)
    logger.debug(msg)
    return flow_file_list


def save_flow_pkl(flow):
    """保存用户流水数据，文件存储保存对象的pkl字符串"""
    user_flow_dir = os.path.join(DB_Flows_History, flow.user_name)
    if not os.path.exists(user_flow_dir):
        os.mkdir(user_flow_dir)
    user_flow_file = os.path.join(user_flow_dir, "{0}.pkl".format(flow.time_stamp))
    with open(user_flow_file, 'w') as f:
        pickle.dump(flow, f)
        f.flush()
    msg = u"保存用户{0}的消费流水数据成功".format(flow.user_name)
    logger.debug(msg)


def load_school_pkl(name):
    """加载学校数据,文件读取对象pkl字符串，并重构存储对象"""
    user_file = os.path.join(DB_Schools, "{0}.pkl".format(name))
    if not os.path.exists(user_file):
        msg = u"加载学校{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    with open(user_file, 'r') as f:
        data = pickle.load(f)
        msg = u"加载学校{0}数据成功".format(name)
        logger.debug(msg)
    return data


def save_school_pkl(school):
    """保存学校数据，文件存储保存对象的pkl字符串"""
    user_file = os.path.join(DB_Schools, "{0}.pkl".format(school.name))
    with open(user_file, 'w') as f:
        pickle.dump(school, f)
        f.flush()
    msg = u"保存学校{0}数据成功".format(school.name)
    logger.debug(msg)


