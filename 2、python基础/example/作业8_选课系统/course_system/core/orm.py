# coding:utf-8


class School(object):
    """学校"""
    def __init__(self, courses=None, classes=None):
        self.course = courses if courses is not None else []
        self.classes = classes if classes is not None else []


class Course(object):
    """课程"""
    def __init__(self, cycle, price):
        self.cycle = cycle
        self.price = price


class Teacher(object):
    """讲师"""
    def __init__(self, school):
        self.school = school


class Student(object):
    """学生"""
    def __init__(self, school, cls):
        self.school = school
        self.cls = cls


class Class(object):
    """班级"""
    def __init__(self, course, teacher):
        self.course = course
        self.teacher = teacher

