# coding:utf-8
from conf.settings import DB_Host, DB_HostGroups
import os
import json


def save_host(host):
    json_file = os.path.join(DB_Host, "{0}.json".format(host.host_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(host.__dict__))


def query_host(host_id):
    json_file = os.path.join(DB_Host, "{0}.json".format(host_id))
    with open(json_file, "r") as f:
        return json.loads(f.read())


def list_hosts():
    root, dirs, files = next(os.walk(DB_Host))
    host_id_list = [f.split(".")[0] for f in files if f.endswith(".json")]
    return [query_host(host_id) for host_id in host_id_list]


def save_host_group(host_group):
    json_file = os.path.join(DB_Host, "{0}.json".format(host_group.group_id))
    with open(json_file, "w") as f:
        f.write(json.dumps(host_group.__dict__))


def query_host_group(group_id):
    json_file = os.path.join(DB_HostGroups, "{0}.json".format(group_id))
    with open(json_file, "r") as f:
        return json.loads(f.read())


def list_host_groups():
    root, dirs, files = next(os.walk(DB_HostGroups))
    host_group_id_list = [f.split(".")[0] for f in files if f.endswith(".json")]
    return [query_host_group(group_id) for group_id in host_group_id_list]


def get_new_host_id():
    return len(list_hosts())


def get_new_host_group_id():
    return len(list_host_groups())
