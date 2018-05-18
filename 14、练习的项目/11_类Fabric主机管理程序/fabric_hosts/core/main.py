# coding:utf-8
from core.manager import HostsManager


def host_execute_cmd(hostname, port, username, password, cmd):
    client = HostsManager.host.create_session(hostname, port, username, password)
    rsp = client.execute(cmd)
    client.close()
    return rsp


def host_put_file(hostname, port, username, password, local_path, remote_path):
    client = HostsManager.host.create_sftp_session(hostname, port, username, password)
    rsp = client.put(local_path, remote_path)
    client.close()
    return rsp


def host_get_file(hostname, port, username, password, remote_path, local_path):
    client = HostsManager.host.create_sftp_session(hostname, port, username, password)
    rsp = client.put(remote_path, local_path)
    client.close()
    return rsp


def host_group_get_file(host_id, cmd):
    hosts = HostsManager.host_group
    rsp = hosts.get(cmd)
    hosts.close()
    return rsp


def host_group_put_file(host_id, cmd):
    hosts = HostsManager.host_group
    rsp = hosts.put(cmd)
    hosts.close()
    return rsp
