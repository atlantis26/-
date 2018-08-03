# _*_coding:utf-8_*_
from models.orm import UserProfile, AuditLog
from models import DBSession
from core.utils import print_err, yaml_parser
from core import ssh_login
from core.utils import SomethingError


class BaseHandler(object):
    @staticmethod
    def auth():
        """ 用户登录认证"""
        count = 0
        while count < 3:
            username = input(u"请输入用户账号：").strip()
            if len(username) == 0:
                print(u"账号不能为空")
            password = input(u"请输入账号密码：").strip()
            if len(password) == 0:
                print(u"密码不能为空")
            session = DBSession()
            user_obj = session.query(UserProfile).filter(UserProfile.username == username,
                                                         UserProfile.password == password).first()
            session.close()
            if user_obj:
                return user_obj
            else:
                print(u"账户或密码错误, 你还有{0}次机会.".format(3-count-1))
                count += 1
        else:
            print_err(u"输入错误账号密码次数过多")

    @staticmethod
    def record_log(user_id, bind_host_id, action, cmd, timestamp):
        """数据库内记录用户操作的日志"""
        session = DBSession()
        log = AuditLog(user_id=user_id, bind_host_id=bind_host_id, action_type=action, cmd=cmd, date=timestamp)
        session.add(log)
        session.commit()
        session.close()

    @staticmethod
    def show_user_info(user_obj):
        pass

    @staticmethod
    def start_session():
        user = BaseHandler.auth()
        if user:
            print(u"欢迎用户{0}登录本系统...".format(user.username))
            exit_flag = False
            while not exit_flag:
                if user.bind_hosts:
                    print('\033[32;1mz.\tungroupped hosts (%s)\033[0m' %len(user.bind_hosts) )
                for index, group in enumerate(user.host_groups):
                    print('\033[32;1m{0}.\t{1} ({2})\033[0m'.format(index, group.name,  len(group.bind_hosts)) )

                choice = input("[%s]:" % user.username).strip()
                if len(choice) == 0:continue
                if choice == 'z':
                    print("------ Group: ungroupped hosts ------" )
                    for index,bind_host in enumerate(user.bind_hosts):
                        print("  %s.\t%s@%s(%s)"%(index,
                                                  bind_host.remoteuser.username,
                                                  bind_host.host.hostname,
                                                  bind_host.host.ip_addr,
                                                  ))
                    print("----------- END -----------" )
                elif choice.isdigit():
                    choice = int(choice)
                    if choice < len(user.groups):
                        print("------ Group: %s ------"  % user.groups[choice].name )
                        for index,bind_host in enumerate(user.groups[choice].bind_hosts):
                            print("  %s.\t%s@%s(%s)"%(index,
                                                      bind_host.remoteuser.username,
                                                      bind_host.host.hostname,
                                                      bind_host.host.ip_addr,
                                                      ))
                        print("----------- END -----------" )

                        #host selection
                        while not exit_flag:
                            user_option = input("[(b)back, (q)quit, select host to login]:").strip()
                            if len(user_option)==0:continue
                            if user_option == 'b':break
                            if user_option == 'q':
                                exit_flag=True
                            if user_option.isdigit():
                                user_option = int(user_option)
                                if user_option < len(user.groups[choice].bind_hosts) :
                                    print('host:',user.groups[choice].bind_hosts[user_option])
                                    print('audit log:',user.groups[choice].bind_hosts[user_option].audit_logs)
                                    ssh_login.ssh_login(user,
                                                        user.groups[choice].bind_hosts[user_option],
                                                        session,
                                                        log_recording)
                    else:
                        print("no this option..")


class ManagerHandler(BaseHandler):
    def __init__(self):
        BaseHandler.__init__(self)

    @staticmethod
    def create_users(argvs):
        '''
        create little_finger access user
        :param argvs:
        :return:
        '''
        if '-f' in argvs:
            user_file = argvs[argvs.index("-f") + 1]
        else:
            print_err("invalid usage, should be:\ncreateusers -f <the new users file>", quit=True)

        source = yaml_parser(user_file)
        if source:
            for key, val in source.items():
                print(key, val)
                obj = models.UserProfile(username=key, password=val.get('password'))
                if val.get('groups'):
                    groups = session.query(models.Group).filter(models.Group.name.in_(val.get('groups'))).all()
                    if not groups:
                        print_err("none of [%s] exist in group table." % val.get('groups'), quit=True)
                    obj.groups = groups
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
