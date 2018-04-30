# coding:utf-8
from conf.settings import DB_Users, DB_Flows_History, RP, ResourcePoolDir
from core.orm import SomeError
import pickle
import os
import logging

logger = logging.getLogger("system.db")


def save_resources_pool():
    """更新教学资源池的数据到文件，则通过pickle保存对象"""
    resource_pool_file = os.path.join(ResourcePoolDir, "ResourcePool.pkl")
    save_pkl(RP, resource_pool_file)


def load_user_pkl(username):
    """加载用户数据,文件读取对象pkl字符串，并重构存储对象"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(username))
    if not os.path.exists(user_file):
        raise SomeError(u"加载用户{0}数据失败,无此用户信息".format(username))
    return load_pkl(user_file)


def save_user_pkl(user):
    """保存用户数据，文件存储保存对象的pkl字符串"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(user.username))
    save_pkl(user, user_file)


def load_flow_pkl(username):
    """加载用户流水数据,文件读取对象pkl字符串，并重构存储对象"""
    user_flow_dir = os.path.join(DB_Flows_History, username)
    if not os.path.exists(user_flow_dir):
        raise SomeError(u"加载用户{0}的消费流水数据失败，无流水数据".format(username))
    else:
        flow_list = list()
        for root, dirs, files in os.walk(user_flow_dir):
            for file in files:
                data = load_pkl(os.path.join(root, file))
                flow_list.append(data)
    return flow_list


def save_flow_pkl(flow):
    """保存用户流水数据，文件存储保存对象的pkl字符串"""
    user_flow_dir = os.path.join(DB_Flows_History, flow.username)
    if not os.path.exists(user_flow_dir):
        os.mkdir(user_flow_dir)
    user_flow_file = os.path.join(user_flow_dir, "{0}.pkl".format(flow.time_stamp))
    save_pkl(flow, user_flow_file)


def load_pkl(file_path):
    """加载pkl数据,文件读取对象pkl字符串，并重构存储对象"""
    if not os.path.exists(file_path):
        raise SomeError(u"加载pkl数据文件{0}失败".format(file_path))
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def save_pkl(obj, file_path):
    """保存pkl数据，文件存储保存对象的pkl字符串"""
    with open(file_path, 'wb+') as f:
        pickle.dump(obj, f)
        f.flush()
