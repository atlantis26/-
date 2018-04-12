# coding:utf-8
from conf.settings import DB_Accounts, DB_Flows_History, DB_Schools
from core.orm import SomeError
import pickle
import os
import logging

logger = logging.getLogger("atm.accounts")


def load_account_pkl(name):
    """加载账户数据,文件读取对象pkl字符串，并重构存储对象"""
    account_file = os.path.join(DB_Accounts, "{0}.pkl".format(name))
    if not os.path.exists(account_file):
        msg = u"加载账户{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    with open(account_file, 'r') as f:
        data = pickle.load(f)
        msg = u"加载账户{0}数据成功".format(name)
        logger.debug(msg)
    return data


def save_account_pkl(account):
    """保存账户数据，文件存储保存对象的pkl字符串"""
    account_file = os.path.join(DB_Accounts, "{0}.pkl".format(account.name))
    with open(account_file, 'w') as f:
        pickle.dump(account, f)
        f.flush()
    msg = u"保存账户{0}数据成功".format(account.name)
    logger.debug(msg)


def load_flow_pkl(name):
    """加载账户流水数据,文件读取对象pkl字符串，并重构存储对象"""
    account_file = os.path.join(DB_Flows_History, "{0}.pkl".format(name))
    if not os.path.exists(account_file):
        msg = u"加载账户{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    with open(account_file, 'r') as f:
        data = pickle.load(f)
        msg = u"加载账户{0}数据成功".format(name)
        logger.debug(msg)
    return data


def save_flow_pkl(flow):
    """保存账户流水数据，文件存储保存对象的pkl字符串"""
    account_flow_dir = os.path.join(DB_Flows_History, flow.account_name)
    if not os.path.exists(account_flow_dir):
        os.mkdir(account_flow_dir)
    account_flow_file = os.path.join(account_flow_dir, "{0}.pkl".format(flow.time_stamp))
    with open(account_flow_file, 'w') as f:
        pickle.dump(flow, f)
        f.flush()
    msg = u"保存账户{0}的消费流水数据成功".format(flow.account_name)
    logger.debug(msg)


def load_school_pkl(name):
    """加载学校数据,文件读取对象pkl字符串，并重构存储对象"""
    account_file = os.path.join(DB_Schools, "{0}.pkl".format(name))
    if not os.path.exists(account_file):
        msg = u"加载学校{0}数据失败".format(name)
        logger.debug(msg)
        raise SomeError(msg)
    with open(account_file, 'r') as f:
        data = pickle.load(f)
        msg = u"加载学校{0}数据成功".format(name)
        logger.debug(msg)
    return data


def save_school_pkl(school):
    """保存学校数据，文件存储保存对象的pkl字符串"""
    account_file = os.path.join(DB_Schools, "{0}.pkl".format(school.name))
    with open(account_file, 'w') as f:
        pickle.dump(school, f)
        f.flush()
    msg = u"保存学校{0}数据成功".format(school.name)
    logger.debug(msg)


