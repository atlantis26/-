# coding:utf-8


class School(object):
    """学校: 包含学校名称、开的课程列表、班级列表、教师列表"""
    def __init__(self, school_id, name):
        self.id = school_id
        self.name = name

    @property
    def __school_id(self):
        return self.id

    def create_course(self, course_id, course_name, cycle, price):
        """创建新课程"""
        course = Course(course_id, course_name, cycle, price, self.__school_id)
        return course

    def create_class(self, class_id, class_name, course_id, student_id_list=list()):
        """创建新班级"""
        class1 = Class(class_id, class_name, course_id, self.__school_id, student_id_list)
        return class1


class Class(object):
    """班级：包含班级名称、课程名、学员列表等属性"""
    def __init__(self, class_id, name, course_id, school_id, student_id_list=list()):
        self.id = class_id
        self.name = name
        self.course_id = course_id
        self.school_id = school_id
        self.student_id_list = student_id_list

    def add_student(self, student_id):
        """班级添加学员"""
        student_id_list = self.student_id_list[:]
        if student_id in student_id_list:
            raise SomeError(u"添加失败，学员{0}已经在学员列表当中".format(student_id))
        student_id_list.append(student_id)
        self.student_id_list = student_id_list


class Course(object):
    """课程：包含课程名称、学习周期、学费价格等属性"""
    def __init__(self, course_id, name, cycle, price, school_id):
        self.id = course_id
        self.name = name
        self.cycle = cycle
        self.price = price
        self.school_id = school_id


class Teacher(object):
    """讲师角色：包含讲师员工编号、姓名、系统用户名、管理的班级的id列表等属性"""
    def __init__(self, teacher_id, name, username, class_id_list=list()):
        self.id = teacher_id
        self.name = name
        self.username = username
        self.class_id_list = class_id_list

    def add_class(self, class_id):
        """新增负责的班级"""
        class_id_list = self.class_id_list[:]
        if class_id in class_id_list:
            raise SomeError(u"添加失败，班级{0}已经在班级列表当中".format(class_id))
        class_id_list.append(class_id)
        self.class_id_list = class_id_list


class Student(object):
    """学员角色: 包括学号、姓名、 系统用户名、已报名课程id列表等属性"""
    def __init__(self, student_id, name, username, course_id_list=list()):
        self.id = student_id
        self.name = name
        self.username = username
        self.course_id_list = course_id_list

    def add_course(self, course_id):
        """新增学习的课程"""
        course_id_list = self.course_id_list[:]
        if course_id in course_id_list:
            raise SomeError(u"添加失败，课程{0}已经在学习列表当中".format(course_id))
        course_id_list.append(course_id)
        self.course_id_list = course_id_list


class User(object):
    """用户orm模型, 包括系统用户名、密码、余额、身份角色"""
    def __init__(self, username, password, balance, role):
        self.username = username
        self.password = password
        self.balance = balance
        self.role = role


class Flow(object):
    """用户单笔消费流水信息，包括时间戳、用户名、事件、详细信息"""
    def __init__(self, time_stamp, username, action, details):
        self.time_stamp = time_stamp
        self.username = username
        self.action = action
        self.details = details


class ResponseData(object):
    """统一返回数据"""
    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class SomeError(Exception):
    """自定义异常错误"""
    pass
