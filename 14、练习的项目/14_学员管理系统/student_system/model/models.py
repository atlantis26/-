# coding:utf-8
from sqlalchemy import Column, Integer, String, ForeignKey
from model import BaseModel


class Student(BaseModel):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    qq = Column(String(50))


class Teacher(BaseModel):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class Class(BaseModel):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class ClassRecord(BaseModel):
    __tablename__ = "class_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(String(50))

