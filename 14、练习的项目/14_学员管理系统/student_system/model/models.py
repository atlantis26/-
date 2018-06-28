# coding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from model import BaseModel
from datetime import datetime

# 创建多对多关系表，在数据中实体存在的表，在另外两个主表中一个表中删除某条数据，关系标中对应的关系也会自动删除
class_m2m_student = Table("class_m2m_student", BaseModel,
                          Column("class_id", Integer, ForeignKey("class.id")),
                          Column("student_id", Integer, ForeignKey("student.id")))


class Student(BaseModel):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    qq = Column(String(50))
    # relationship用于快捷查询关联的所有班级对象，不会在表中建立实体对象
    class1 = relationship('Class', secondary=class_m2m_student, backref='student')

    def __repr__(self):
        return self.name


class Class(BaseModel):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    # relationship的设置，用于正向快捷查询关联的所有学生对象，不会在表中建立实体对象
    student = relationship('Student', secondary=class_m2m_student, backref='class')

    def __repr__(self):
        return self.name


class Teacher(BaseModel):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __repr__(self):
        return self.name


class CourseRecord(BaseModel):
    __tablename__ = "course_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now())
    teacher_id = Column(Integer, Column(Integer, ForeignKey('teacher.id')))
    # 外键ForeignKey的设置，以class_id为例，只是方便反向的查询班级class表时，查询返回对象包含了关联的class_record
    class_id = Column(Integer, Column(Integer, ForeignKey('class.id')))
    description = Column(String(100))

    def __repr__(self):
        return u"开课记录, 日期:{0}，内容描述:{1}".format(self.datetime, self.description)


class Homework(BaseModel):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True, autoincrement=True)
    homework_path = Column(String(100))  # 学生打包上传的作业文件，存放在仓库的路径地址
    record_id = Column(Integer, ForeignKey('course_record.id'))
    student_id = Column(Integer, ForeignKey('student.id'))
    score = Column(Integer, default=None)
