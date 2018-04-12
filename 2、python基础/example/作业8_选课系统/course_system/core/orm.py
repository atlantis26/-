# coding:utf-8


class School(object):
    """学校: 包含学校名称、开的课程列表、班级列表、教师列表"""
    def __init__(self, school_name, courses=list(), classes=list(), teachers=list()):
        self.school_name = school_name
        self.courses = courses
        self.classes = classes
        self.teachers = teachers

    @property
    def get_employee_id(self):
        """生成新讲师的工号"""
        return len(self.teachers) + 1

    def course_is_exists(self, name):
        """判断课程已存在, 名字唯一"""
        if [course for course in self.courses if course.name == name]:
            return True

    def class_is_exists(self, name):
        """判断班级已存在，名字唯一"""
        if [cla for cla in self.classes if cla.name == name]:
            return True

    def teacher_is_exists(self, emp_id):
        """判断教师已存在，员工编号唯一"""
        if [teacher for teacher in self.teachers if teacher.emp_id == emp_id]:
            return True

    def create_course(self, name, cycle, price):
        """创建课程"""
        if self.course_is_exists(name):
            raise SomeError(u"{0}课程已存在".format(name))
        course = Course(name, cycle, price)
        self.courses.append(course)
        code = 200
        msg = u"创建课程{0}成功".format(name)

        return ResponseData(code, msg, course)

    def create_class(self, name, course_name, student_list=list()):
        """创建班级"""
        if not self.course_is_exists(course_name):
            raise SomeError(u"{0}课程不存在".format(course_name))
        if self.class_is_exists(name):
            raise SomeError(u"{0}班级已经存在".format(name))
        class1 = Class(name, course_name, student_list)
        self.classes.append(class1)
        code = 200
        msg = u"创建班级{0}成功".format(name)

        return ResponseData(code, msg, class1)

    def create_teacher(self, name, age, sex, class_list=list()):
        emp_id = self.get_employee_id
        teacher = Teacher(emp_id, name, age, sex, class_list)
        self.teachers.append(teacher)
        code = 200
        msg = u"创建讲师{0}成功".format(name)

        return ResponseData(code, msg, teacher)


class Class(object):
    """班级：包含班级名称、课程名、学员列表等属性"""
    def __init__(self, name, course, student_list=list()):
        self.name = name
        self.course = course
        self.student_list = student_list

    @property
    def get_student_id(self):
        """生成新学员的学号"""
        return len(self.student_list) + 1

    def student_is_exists(self, student_id):
        """判断学生已存在,学号唯一"""
        if [student for student in self.student_list if student.student_id == student_id]:
            return True

    def create_student(self, name, age, sex, registered_course_list=list()):
        """创建学员"""
        student_id = self.get_student_id
        student = Student(student_id, name, age, sex, registered_course_list)
        self.student_list.append(student)
        code = 200
        msg = u"报名成功，创建学员{0}成功".format(name)

        return ResponseData(code, msg, student)


class Course(object):
    """课程：包含课程名称、学习周期、学费价格等属性"""
    def __init__(self, name, cycle, price):
        self.name = name
        self.cycle = cycle
        self.price = price


class Teacher(object):
    """讲师：包含讲师员工编号、姓名、年龄、性别、管理的班级列表等属性"""
    def __init__(self, emp_id, name, age, sex, class_list=list()):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.sex = sex
        self.class_list = class_list


class Student(object):
    """学员: 包括学号、姓名、年龄、性别、已报名课程列表等属性"""
    def __init__(self, student_id, name, age, sex, registered_course_list=list()):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.sex = sex
        self.registered_course_list = registered_course_list


class RegisteredCourse(object):
    """已报名学习课程：包括学校、课程、班级、学费支付状态，时间戳等属性"""
    def __init__(self, school, course, class1, payment_state, time_stamp):
        self.school = school
        self.course = course
        self.class1 = class1
        self.payment_state = payment_state
        self.time_stamp = time_stamp


class Account(object):
    """账户orm模型"""
    def __init__(self, name, password, balance, locked=False, is_administrator=False):
        self.name = name
        self.password = password
        self.balance = balance
        self.locked = locked
        self.is_administrator = is_administrator


class Flow(object):
    """账户单笔流水信息"""
    def __init__(self, datetime, account_name, action, details):
        self.datetime = datetime
        self.account_name = account_name
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
