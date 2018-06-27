# coding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey
from model import BaseModel


class StudentModel(BaseModel):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    qq = Column(String(50))
    class_id = Column(Integer, ForeignKey('class.id'))


class TeacherModel(BaseModel):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class ClassModel(BaseModel):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class ClassRecordModel(BaseModel):
    __tablename__ = "class_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    
