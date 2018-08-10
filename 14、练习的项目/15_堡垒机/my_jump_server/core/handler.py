# _*_coding:utf-8_*_
from models.db_handler import DatabaseHandler
from core.utils import print_err, yaml_parser
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
            data = user_obj.__dict__
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
        logger.debug(ResponseData(code, msg, ).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def select_host_by_group(user_id):
        """根据主机组来选择目标登录主机"""
        try:
            user = DatabaseHandler.query_user_profile_by_id(user_id)
            print(u"您具有访问权限的主机组如下：")
            for index, group in enumerate(user.groups):
                print(u"id：{0}    主机组名：{1}".format(group.id, group.name))
            choice1 = input(u"请输入选择的主机组的id:").strip()
            if not choice1:
                raise SomethingError(u"主机组id不存在")
            print(u"您选择的主机组下可访问的主机列表如下：")
            for index, host in enumerate(user.groups[choice1].bind_hosts):
                print(u"id：{0}   主机名称：{1}   ip地址：{2}  登录账号：".format(host.id,
                                                                    host.hostname,
                                                                    host.ip_addr,
                                                                    host.remoteuser.username))
            host_id = input(u"请输入选择的主机的id")
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
            for index, host in enumerate(user.bind_hosts):
                print(u"id：{0}   主机名称：{1}   ip地址：{2}  登录账号：".format(host.id,
                                                                    host.hostname,
                                                                    host.ip_addr,
                                                                    host.remoteuser.username))
            host_id = input(u"请输入选择的主机的id")
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
            host_obj = DatabaseHandler.query_host_by_id(host_id)
            if not host_obj:
                raise SomethingError(u"目标主机不存在")
            user_obj = DatabaseHandler.query_user_profile_by_id(user_id)
            if not user_obj:
                raise SomethingError(u"用户不存在")
            if host_id not in [host.id for host in user_obj.bind_hosts]:
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
    def create_users(user_file, role_id):
        """创建系统用户"""
        source = yaml_parser(user_file)
        if source:
            for key, val in source.items():
                print(key, val)
                user = DatabaseHandler.create_user(username=key, password=val.get('password'), role_id=role_id)
                if val.get('groups'):
                    groups = DatabaseHandler.list_group_by_name_list(val.get('groups'))
                    if not groups:
                        print_err("none of [%s] exist in group table." % val.get('groups'), quit=True)
                    user.groups = groups
                if val.get('bind_hosts'):
                    bind_hosts = common_filters.bind_hosts_filter(val)
                    obj.bind_hosts = bind_hosts
                # print(obj)
                session.add(obj)
            session.commit()

    @staticmethod
    def create_groups(argvs):
        '''
        create groups
        :param argvs:
        :return:
        '''
        if '-f' in argvs:
            group_file = argvs[argvs.index("-f") + 1]
        else:
            print_err("invalid usage, should be:\ncreategroups -f <the new groups file>", quit=True)
        source = yaml_parser(group_file)
        if source:
            for key, val in source.items():
                print(key, val)
                obj = models.Group(name=key)
                if val.get('bind_hosts'):
                    bind_hosts = common_filters.bind_hosts_filter(val)
                    obj.bind_hosts = bind_hosts

                if val.get('user_profiles'):
                    user_profiles = common_filters.user_profiles_filter(val)
                    obj.user_profiles = user_profiles
                session.add(obj)
            session.commit()

    @staticmethod
    def create_hosts(argvs):
        '''
        create hosts
        :param argvs:
        :return:
        '''
        if '-f' in argvs:
            hosts_file = argvs[argvs.index("-f") + 1]
        else:
            print_err("invalid usage, should be:\ncreate_hosts -f <the new hosts file>", quit=True)
        source = yaml_parser(hosts_file)
        if source:
            for key, val in source.items():
                print(key, val)
                obj = models.Host(hostname=key, ip_addr=val.get('ip_addr'), port=val.get('port') or 22)
                session.add(obj)
            session.commit()

    @staticmethod
    def create_bindhosts(argvs):
        '''
        create bind hosts
        :param argvs:
        :return:
        '''
        if '-f' in argvs:
            bindhosts_file = argvs[argvs.index("-f") + 1]
        else:
            print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>", quit=True)
        source = yaml_parser(bindhosts_file)
        if source:
            for key, val in source.items():
                # print(key,val)
                host_obj = session.query(models.Host).filter(models.Host.hostname == val.get('hostname')).first()
                assert host_obj
                for item in val['remote_users']:
                    print(item)
                    assert item.get('auth_type')
                    if item.get('auth_type') == 'ssh-passwd':
                        remoteuser_obj = session.query(models.RemoteUser).filter(
                            models.RemoteUser.username == item.get('username'),
                            models.RemoteUser.password == item.get('password')
                        ).first()
                    else:
                        remoteuser_obj = session.query(models.RemoteUser).filter(
                            models.RemoteUser.username == item.get('username'),
                            models.RemoteUser.auth_type == item.get('auth_type'),
                        ).first()
                    if not remoteuser_obj:
                        print_err("RemoteUser obj %s does not exist." % item, quit=True)
                    bindhost_obj = models.BindHost(host_id=host_obj.id, remoteuser_id=remoteuser_obj.id)
                    session.add(bindhost_obj)
                    # for groups this host binds to
                    if source[key].get('groups'):
                        group_objs = session.query(models.Group).filter(
                            models.Group.name.in_(source[key].get('groups'))).all()
                        assert group_objs
                        print('groups:', group_objs)
                        bindhost_obj.groups = group_objs
                    # for user_profiles this host binds to
                    if source[key].get('user_profiles'):
                        userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                            source[key].get('user_profiles')
                        )).all()
                        assert userprofile_objs
                        print("userprofiles:", userprofile_objs)
                        bindhost_obj.user_profiles = userprofile_objs
                        # print(bindhost_obj)
            session.commit()

    @staticmethod
    def create_remoteusers(argvs):
        '''
        create remoteusers
        :param argvs:
        :return:
        '''
        if '-f' in argvs:
            remoteusers_file = argvs[argvs.index("-f") + 1]
        else:
            print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>", quit=True)
        source = yaml_parser(remoteusers_file)
        if source:
            for key, val in source.items():
                print(key, val)
                obj = models.RemoteUser(username=val.get('username'), auth_type=val.get('auth_type'),
                                        password=val.get('password'))
                session.add(obj)
            session.commit()
