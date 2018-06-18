# coding:utf-8
from core.db_handler import save_host, modify_host, delete_host, query_host, list_hosts, get_new_host_id
from core.rpc_handler import Shell, TransPort
from core.orm import Host, SomeError, ResponseData
import logging

logger = logging.getLogger("fabric.host")


class HostHandler(object):
    @staticmethod
    def create_session(hostname, port, username, password):
        """创建ssh客户端连接实例"""
        return Shell(hostname, port, username, password)

    @staticmethod
    def create_sftp_session(hostname, port, username, password):
        """创建sftp客户端连接实例"""
        return TransPort(hostname, port, username, password)

    @staticmethod
    def create(ip, port, username, password):
        """添加新主机信息"""
        try:
            host_id = get_new_host_id()
            host = Host(host_id, ip, port, username, password)
            save_host(host)
            code = 200
            msg = "添加服务器主机信息成功"
            data = host.__dict__
        except SomeError as e:
            code = 400
            msg = "添加服务器主机信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def delete(host_id):
        """删除主机信息"""
        try:
            delete_host(host_id)
            code = 200
            msg = "删除主机信息成功"
        except SomeError as e:
            code = 400
            msg = "删除主机信息失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def modify(host_id, ip, port, username, password):
        """修改主机信息"""
        try:
            host = Host(host_id, ip, port, username, password)
            modify_host(host_id, host)
            code = 200
            msg = "修改主机信息成功"
            data = host.__dict__
        except SomeError as e:
            code = 400
            msg = "修改主机信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def detail(host_id):
        """查询主机信息详情"""
        try:
            data = query_host(host_id)
            code = 200
            msg = "查询主机信息成功"
        except SomeError as e:
            code = 400
            msg = "查询主机信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list():
        """查询主机列表信息"""
        try:
            data = list_hosts()
            code = 200
            msg = "查询主机列表信息成功"
        except SomeError as e:
            code = 400
            msg = "查询主机列表信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)
