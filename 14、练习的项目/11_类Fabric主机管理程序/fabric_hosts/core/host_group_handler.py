# coding:utf-8
from core.db_handler import save_host_group, delete_host_group, query_host_group, query_host
from core.db_handler import list_host_groups, get_new_host_group_id, modify_host_group
from core.orm import HostGroup, SomeError, ResponseData
from core.rpc_handler import HostThread
import logging

logger = logging.getLogger("fabric.host_group")


class HostGroupHandler(object):
    @staticmethod
    def create(group_name, host_ids):
        """创建主机组信息"""
        try:
            host_ids = host_ids.split(",") if host_ids else []
            group_id = get_new_host_group_id()
            host_group = HostGroup(group_id, group_name,  host_ids)
            save_host_group(host_group)
            code = 200
            msg = "添加主机组信息成功"
            data = host_group.__dict__
        except SomeError as e:
            code = 400
            msg = "添加主机组信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def delete(group_id):
        """删除主机组信息"""
        try:
            delete_host_group(group_id)
            code = 200
            msg = "删除主机组信息成功"
        except SomeError as e:
            code = 400
            msg = "删除主机组信息失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def modify(group_id, group_name, add_hosts, delete_hosts):
        """修改主机组信息"""
        try:
            host = query_host_group(group_id)
            host_ids = host["host_id_list"]
            group_name = group_name if group_name else host["group_name"]
            add_host_ids = add_hosts.split(",") if add_hosts else []
            [query_host(host_id) for host_id in add_host_ids]
            delete_hosts = delete_hosts.split(",") if delete_hosts else []
            not_member_host = [host_id for host_id in delete_hosts if host_id not in host_ids]
            if not_member_host:
                raise SomeError(u"下列Id号的主机{0}不是组成员，移出失败".format(",".join(not_member_host)))
            [host_ids.remove(host_id) for host_id in delete_hosts]
            host_ids.extend(add_host_ids)
            new_host_id_list = list(set(host_ids))
            host_group = HostGroup(group_id, group_name, new_host_id_list)
            modify_host_group(group_id, host_group)
            code = 200
            msg = "修改主机组信息成功"
            data = host_group.__dict__
        except SomeError as e:
            code = 400
            msg = "修改主机组信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def detail(group_id):
        """查询单个主机组信息详情"""
        try:
            data = query_host_group(group_id)
            code = 200
            msg = "查询主机组信息成功"
        except SomeError as e:
            code = 400
            msg = "查询主机组信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list():
        """查询单个主机组列表信息"""
        try:
            data = list_host_groups()
            code = 200
            msg = "查询主机组列表信息成功"
        except SomeError as e:
            code = 400
            msg = "查询主机组列表信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def _execute_job(group_id, action, **kwargs):
        """批量在主机组内的全部主机上都执行任务"""
        host_group = query_host_group(group_id)
        hosts = [query_host(host_id) for host_id in host_group["host_id_list"]]
        result = {}
        threads = []
        for host in hosts:
            thread = HostThread(host, action, **kwargs)
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for thread in threads:
            result[thread.host["host_id"]] = thread.get_result()
        return result

    @staticmethod
    def execute_cmd(group_id, commands):
        """批量在主机组内的全部主机上都执行命令"""
        return HostGroupHandler._execute_job(group_id, "commands", commands=commands)

    @staticmethod
    def get(group_id, remote_path, local_dir):
        """批量在主机组内的全部主机上都执行下载"""
        return HostGroupHandler._execute_job(group_id, "get", remote_path=remote_path,  local_dir=local_dir)

    @staticmethod
    def put(group_id, local_path, remote_path):
        """批量在主机组内的全部主机上都执行上传"""
        return HostGroupHandler._execute_job(group_id, "put", local_path=local_path, remote_path=remote_path)
