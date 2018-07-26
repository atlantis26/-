# coding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 创建多对多表
host_m2m_remoteuser = Table("host_m2m_remoteuser", Base.metadata,
                            Column("host_id", Integer, ForeignKey("host.id")),
                            Column("remoteuser_id", Integer, ForeignKey("remote_user.id"))
                            )


class Host(Base):
    __tableName__ = "host"
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True)
    ip = Column(String(64), unique=True)
    port = Column(Integer, default=22)
    remote_users = relationship("RemoteUser", secondary=host_m2m_remoteuser, backref="hosts")

    def __repr__(self):
        return self.hostname


class HostGroup(Base):
    __tableName__ = "host_group"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)

    def __repr__(self):
        return self.name


class RemoteUser(Base):
    __tableName__ = "remote_user"
    __table_args__ = (UniqueConstraint("auth_type", "username", "password"))   # 联合唯一
    AuthTypes = [(u"ssh-password", "SSH/Password"),
                 (u"ssh-key", "SSH/KEY")]
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(128))
    auth_type = Column(ChoiceType(AuthTypes))

    def __repr__(self):
        return self.username


class UserProfile(Base):
    __tableName__ = "user_profile"
    username = Column(String(32), unique=True)
    password = Column(String(128))

    def __repr__(self):
        return self.username

