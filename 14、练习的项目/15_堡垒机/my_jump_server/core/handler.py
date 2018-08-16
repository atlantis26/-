# _*_coding:utf-8_*_
from models.db_handler import DatabaseHandler
from models.orm import UserProfile, Role, RemoteUser, Host, Group, BindHost
from core.utils import yaml_parser
from core import ssh_login
from core.utils import SomethingError, ResponseData
import logging

logger = logging.getLogger("system.handler")


class Handler(object):
    @staticmethod
    def login(username, password):
        """ 用户登录认证"""
        try:
            if len(username) == 0:
                raise SomethingError(u"账号不能为空")
            if len(password) == 0:
                print(u"密码不能为空")
            user_obj = DatabaseHandler.query_user_profile_by_account(username, password)
            if not user_obj:
                raise SomethingError(u"用户不存在")
            code = 200
            msg = u"登录成功"
            data = user_obj.to_dict()
        except Exception as e:
            code = 400
            msg = u"登录失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_audit_log(user_id, bind_host_id, action, cmd, timestamp):
        """数据库内记录用户操作的日志"""
        try:
            DatabaseHandler.create_audit_log(user_id, bind_host_id, action, cmd, timestamp)
            code = 200
            msg = u"创建用户操作日志成功"
        except Exception as e:
            code = 400
            msg = u"创建用户操作日志成功失败，原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def select_host_by_group(user_id):
        """根据主机组来选择目标登录主机"""
        try:
            user = DatabaseHandler.query_user_profile_by_id(user_id)
            print(u"您具有访问权限的主机组如下：")
            for index, group in enumerate(user.groups):
                print(u"编号：{0}  主机组名：{1}".format(index, group.name))
            choice1 = input(u"请输入选择的主机组的编号:").strip()
            if not choice1.isdigit():
                raise SomethingError(u"主机组编号不是数字")
            elif int(choice1) > len(user.groups)-1:
                raise SomethingError(u"主机组编号不存在")
            print(u"您选择的主机组下可访问的主机列表如下：")
            for index, bind_host in enumerate(user.groups[int(choice1)].bind_hosts):
                print(u"id：{0}   主机名称：{1}   ip地址：{2}  登录账号：".format(bind_host.id,
                                                                    bind_host.host.hostname,
                                                                    bind_host.host.ip_addr,
                                                                    bind_host.remoteuser.username))
            host_id = input(u"请输入选择的主机的id：")
            code = 200
            msg = u"选择目标主机成功"
            data = host_id
        except SomethingError as e:
            code = 200
            msg = u"选择目标主机失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def select_host_by_list(user_id):
        """根据主机列表来选择目标登录主机"""
        try:
            user = DatabaseHandler.query_user_profile_by_id(user_id)
            print(u"您具有访问权限的主机列表如下：")
            for index, bind_host in enumerate(user.bind_hosts):
                print(u"id：{0}   主机名称：{1}   ip地址：{2}  登录账号：{3}".format(bind_host.id,
                                                                       bind_host.host.hostname,
                                                                       bind_host.host.ip_addr,
                                                                       bind_host.remoteuser.username))
            host_id = input(u"请输入选择的主机的id：")
            code = 200
            msg = u"登录目标主机成功"
            data = host_id
        except SomethingError as e:
            code = 200
            msg = u"选择目标主机失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def start_host_session(user_id, host_id):
        try:
            host_obj = DatabaseHandler.query_bindhost_by_id(host_id)
            if not host_obj:
                raise SomethingError(u"目标主机不存在")
            user_obj = DatabaseHandler.query_user_profile_by_id(user_id)
            if not user_obj:
                raise SomethingError(u"用户不存在")
            if int(host_id) not in [host.id for host in user_obj.bind_hosts]:
                raise SomethingError(u"没有权限访问目标主机")
            ssh_login.ssh_login(user_obj, host_obj)
            code = 200
            msg = u"登录目标主机成功"
        except SomethingError as e:
            code = 200
            msg = u"登录目标主机失败，原因：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_users(user_file):
        """创建系统用户"""
        try:
            source = yaml_parser(user_file)
            if source:
                for key, val in source.items():
                    user = UserProfile(username=key, password=val.get('password'), role_id=val.get('role_id'))
                    group_names = val.get('groups')
                    if group_names:
                        groups = DatabaseHandler.list_group_by_names(group_names)
                        if not groups:
                            raise SomethingError(u"配置文件中的主机组都不存在")
                        user.groups = groups
                    bind_host_names = val.get('bind_hosts')
                    if bind_host_names:
                        bind_hosts = DatabaseHandler.list_bindhost_by_names(bind_host_names)
                        user.bind_hosts = bind_hosts
                    DatabaseHandler.commit_orm_object(user)
            code = 200
            msg = u"创建系统用户成功"
            data = source
        except SomethingError as e:
            code = 200
            msg = u"创建系统用户失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_groups(group_file):
        """创建主机组"""
        try:
            source = yaml_parser(group_file)
            if source:
                for key, val in source.items():
                    group = Group(name=key)
                    bind_host_names = val.get('bind_hosts')
                    if bind_host_names:
                        bind_hosts = DatabaseHandler.list_bindhost_by_names(bind_host_names)
                        group.bind_hosts = bind_hosts
                    username_list = val.get('user_profiles')
                    if username_list:
                        user_profiles = DatabaseHandler.list_user_profiles_by_usernames(username_list)
                        group.user_profiles = user_profiles
                    print(group)
                    DatabaseHandler.commit_orm_object([group])
            code = 200
            msg = u"创建主机组成功"
            data = source
        # except SomethingError as e:
        except KeyboardInterrupt as e:
            code = 200
            msg = u"创建主机组失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_hosts(hosts_file):
        """创建主机"""
        try:
            source = yaml_parser(hosts_file)
            if source:
                for key, val in source.items():
                    host = Host(hostname=key, ip_addr=val.get('ip_addr'), port=val.get('port') or 22)
                    DatabaseHandler.commit_orm_object(host)
            code = 200
            msg = u"创建主机成功"
            data = source
        except SomethingError as e:
            code = 200
            msg = u"创建主机失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_bindhosts(bindhosts_file):
        """创建主机的组、登录账号、用户权限的映射关系"""
        try:
            source = yaml_parser(bindhosts_file)
            if source:
                for key, val in source.items():
                    host_name = val.get('hostname')
                    if not host_name:
                        raise SomethingError(u"配置文件内未设置主机名称")
                    host_obj = DatabaseHandler.query_host_by_name(host_name)
                    if not host_obj:
                        raise SomethingError(u"配置文件内的主机名{0}不存在".format(host_name))
                    for item in val['remote_users']:
                        auth_type = item.get('auth_type')
                        if not auth_type:
                            raise SomethingError(u"配置文件内未设置'auth_type'")
                        if item.get('auth_type') == 'ssh-passwd':
                            remoteuser_obj = DatabaseHandler.query_remote_user_by_password(item.get('username'),
                                                                                           item.get('password'))
                        else:
                            remoteuser_obj = DatabaseHandler.query_remote_user_by_auth_type(item.get('username'),
                                                                                            item.get('auth_type'))
                        if not remoteuser_obj:
                            raise SomethingError(u"配置文件内的主机登录账号'{0}'不存在".format(item.get('username')))
                        bindhost_obj = BindHost(host_id=host_obj.id, remoteuser_id=remoteuser_obj.id)

                        # for groups this host binds to
                        group_names = source[key].get('groups')
                        if group_names:
                            groups = DatabaseHandler.list_group_by_names(group_names)
                            bindhost_obj.groups = groups

                        # for user_profiles this host binds to
                        user_names = source[key].get('user_profiles')
                        if user_names:
                            userprofile_objs = DatabaseHandler.list_user_profiles_by_usernames(user_names)
                            bindhost_obj.user_profiles = userprofile_objs
                        DatabaseHandler.commit_orm_object(bindhost_obj)
            code = 200
            msg = u"创建主机与组、登录账号、用户权限关系成功"
            data = source
        except SomethingError as e:
            code = 200
            msg = u"创建主机与组、登录账号、用户权限关系失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_remoteusers(remoteusers_file):
        """配置主机的登录账号信息"""
        try:
            source = yaml_parser(remoteusers_file)
            if source:
                for key, val in source.items():
                    remote_user = RemoteUser(username=val.get('username'),
                                             auth_type=val.get('auth_type'),
                                             password=val.get('password'))
                    DatabaseHandler.commit_orm_object(remote_user)
            code = 200
            msg = u"创建主机登录账号信息成功"
            data = source
        except SomethingError as e:
            code = 200
            msg = u"创建主机登录账号信息失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def create_roles(role_file):
        """配置用户角色信息"""
        try:
            source = yaml_parser(role_file)
            if source:
                for key, names in source.items():
                    if DatabaseHandler.list_role_by_names(names):
                        raise SomethingError(u"配置文件中有角色已经存在")
                    for name in names:
                        role = Role(name=name)
                        DatabaseHandler.commit_orm_object(role)
            code = 200
            msg = u"创建新角色成功"
            data = source
        except SomethingError as e:
            code = 200
            msg = u"创建新角色失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg)
