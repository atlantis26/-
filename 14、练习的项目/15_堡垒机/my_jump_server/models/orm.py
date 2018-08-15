# coding:utf-8
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from models import Base


BindHost2Group = Table('bindhost_2_group', Base.metadata,
                       Column('bindhost_id', ForeignKey('bind_host.id'), primary_key=True),
                       Column('group_id', ForeignKey('group.id'), primary_key=True),
                       )

BindHost2UserProfile = Table('bindhost_2_userprofile', Base.metadata,
                             Column('bindhost_id', ForeignKey('bind_host.id'), primary_key=True),
                             Column('uerprofile_id', ForeignKey('user_profile.id'), primary_key=True),
                             )

Group2UserProfile = Table('group_2_userprofile', Base.metadata,
                          Column('userprofile_id', ForeignKey('user_profile.id'), primary_key=True),
                          Column('group_id', ForeignKey('group.id'), primary_key=True),
                          )


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(128), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))
    groups = relationship('Group', secondary=Group2UserProfile)
    bind_hosts = relationship('BindHost', secondary=BindHost2UserProfile)
    role = relationship('Role')

    def __repr__(self):
        return "<UserProfile(id='%s',username='%s')>" % (self.id, self.username)


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True, nullable=False)


class RemoteUser(Base):
    __tablename__ = 'remote_user'
    AuthTypes = [
        (u'ssh-passwd', u'SSH/Password'),
        (u'ssh-key', u'SSH/KEY'),
    ]
    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(64), nullable=False)
    password = Column(String(255))

    __table_args__ = (UniqueConstraint('auth_type', 'username', 'password', name='_user_passwd_uc'),)

    def __repr__(self):
        return "<RemoteUser(id='%s',auth_type='%s',user='%s')>" % (self.id, self.auth_type, self.username)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_addr = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)
    bind_hosts = relationship("BindHost")

    def __repr__(self):
        return "<Host(id='%s',hostname='%s')>" % (self.id, self.hostname)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True)
    bind_hosts = relationship("BindHost", secondary=BindHost2Group)
    # bind_hosts = relationship("BindHost", secondary=BindHost2Group, back_populates='groups')
    user_profiles = relationship("UserProfile", secondary=Group2UserProfile)

    def __repr__(self):
        return "<HostGroup(id='%s',name='%s')>" % (self.id, self.name)


class BindHost(Base):
    __tablename__ = 'bind_host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('host.id'))
    remoteuser_id = Column(Integer, ForeignKey('remote_user.id'))
    host = relationship("Host")
    remoteuser = relationship("RemoteUser")
    groups = relationship("Group", secondary=BindHost2Group, back_populates='bind_hosts')
    user_profiles = relationship("UserProfile", secondary=BindHost2UserProfile)

    __table_args__ = (UniqueConstraint('host_id', 'remoteuser_id', name='_bindhost_and_user_uc'),)

    def __repr__(self):
        return "<BindHost(id='%s',name='%s',user='%s')>" % (self.id,
                                                            self.host.hostname,
                                                            self.remoteuser.username)


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    bind_host_id = Column(Integer, ForeignKey('bind_host.id'))
    action_choices = [(0, 'CMD'), (1, 'Login'), (2, 'Logout')]
    action_type = Column(ChoiceType(action_choices))
    cmd = Column(String(255))
    date = Column(DateTime)
    user_profile = relationship("UserProfile")
    bind_host = relationship("BindHost")
