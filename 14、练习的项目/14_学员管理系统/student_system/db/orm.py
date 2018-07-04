# coding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from db import BaseModel


# 创建多对多关系表，在数据中实体存在的表，在另外两个主表中一个表中删除某条数据，关系标中对应的关系也会自动删除
user_m2m_class = Table("user_m2m_class", BaseModel.metadata,
                       Column("id", Integer, primary_key=True, autoincrement=True),
                       Column("class_id", Integer, ForeignKey("class.id")),
                       Column("user_id", Integer, ForeignKey("user.id")))


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    account = Column(String(50))
    password = Column(String(50))
    qq = Column(String(50))
    role_id = Column(Integer, ForeignKey('role.id'))
    # relationship用于快捷查询关联的所有班级对象，不会在表中建立实体对象
    class1 = relationship('Class', secondary=user_m2m_class, backref='user')
    role = relationship('Role', backref='user')

    def __repr__(self):
        return self.name


class Role(BaseModel):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __repr__(self):
        return self.name


class Class(BaseModel):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    # relationship的设置，用于正向快捷查询关联的所有学生\老师对象，不会在表中建立实体对象
    student = relationship('User', secondary=user_m2m_class, backref='class')

    def __repr__(self):
        return self.name


class CourseRecord(BaseModel):
    __tablename__ = "course_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    teacher_id = Column(Integer, ForeignKey('user.id'))
    # 外键ForeignKey的设置，以class_id为例，只是方便反向的查询班级class表时，查询返回对象包含了关联的class_record
    class_id = Column(Integer, ForeignKey('class.id'))
    description = Column(String(100))

    def __repr__(self):
        return u"开课记录, 日期:{0}，内容描述:{1}".format(self.datetime, self.description)


class Homework(BaseModel):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True, autoincrement=True)
    homework_path = Column(String(100))  # 学生打包上传的作业文件，存放在仓库的路径地址
    record_id = Column(Integer, ForeignKey('course_record.id'))
    student_id = Column(Integer, ForeignKey('user.id'))
    score = Column(Integer, default=None)
