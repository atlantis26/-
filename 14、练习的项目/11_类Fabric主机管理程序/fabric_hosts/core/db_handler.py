# coding:utf-8
from conf.settings import DB_Host, DB_HostGroups
from core.orm import SomeError
import os
import json


def save_host(host):
    """添加/修改后，保存主机信息"""
    json_file = os.path.join(DB_Host, "{0}.json".format(host.host_id))
    if os.path.exists(json_file):
        raise SomeError("id编号为{0}的主机已存在".format(host.host_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(host.__dict__))


def modify_host(host_id, new_host):
    """添加/修改后，保存主机信息"""
    json_file = os.path.join(DB_Host, "{0}.json".format(host_id))
    if not os.path.exists(json_file):
        raise SomeError("id编号为{0}的主机不存在".format(host_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(new_host.__dict__))


def delete_host(host_id):
    """删除主机信息"""
    json_file = os.path.join(DB_Host, "{0}.json".format(host_id))
    if not os.path.exists(json_file):
        raise SomeError("id编号为{0}的主机不存在".format(host_id))
    os.remove(json_file)


def query_host(host_id):
    """查询单个主机信息"""
    json_file = os.path.join(DB_Host, "{0}.json".format(host_id))
    with open(json_file, "r") as f:
        return json.loads(f.read())


def list_hosts():
    """查询主机列表信息"""
    root, dirs, files = next(os.walk(DB_Host))
    host_id_list = [f.split(".")[0] for f in files if f.endswith(".json")]
    return [query_host(host_id) for host_id in host_id_list]


def save_host_group(host_group):
    """添加/修改后，保存主机组信息"""
    json_file = os.path.join(DB_Host, "{0}.json".format(host_group.group_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(host_group.__dict__))


def modify_host_group(group_id, new_group):
    """添加/修改后，保存主机信息"""
    json_file = os.path.join(DB_HostGroups, "{0}.json".format(group_id))
    if not os.path.exists(json_file):
        raise SomeError("id编号为{0}的主机组不存在".format(group_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(new_group.__dict__))


def delete_host_group(group_id):
    """删除主机组信息"""
    json_file = os.path.join(DB_HostGroups, "{0}.json".format(group_id))
    if not os.path.exists(json_file):
        raise SomeError("id为{0}的主机组不存在".format(group_id))
    os.remove(json_file)


def query_host_group(group_id):
    """查询单个主机组信息"""
    json_file = os.path.join(DB_HostGroups, "{0}.json".format(group_id))
    with open(json_file, "r") as f:
        return json.loads(f.read())


def list_host_groups():
    """查询主机组列表信息"""
    root, dirs, files = next(os.walk(DB_HostGroups))
    host_group_id_list = [f.split(".")[0] for f in files if f.endswith(".json")]
    return [query_host_group(group_id) for group_id in host_group_id_list]


def get_new_host_id():
    """新增时，生成新主机id编号"""
    num = len(list_hosts())
    return "hostCode" + str(num)


def get_new_host_group_id():
    """新增时，生成新主机组id编号"""
    num = len(list_host_groups())
    return "hostGroupCode" + str(num)
