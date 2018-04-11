# coding:utf-8


class School(object):
    """学校"""
    def __init__(self, school_name, courses=list(), classes=list(), teachers=list(), students=list()):
        self.school_name = school_name
        self.courses = courses
        self.classes = classes
        self.teachers = teachers
        self.students = students

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

    def student_is_exists(self, student_id):
        """判断学生已存在,学号唯一"""
        if [student for student in self.students if student.student_id == student_id]:
            return True

    @property
    def get_student_id(self):
        """生成新学员的学号"""
        return len(self.students) + 1

    @property
    def get_employee_id(self):
        """生成新讲师的工号"""
        return len(self.teachers) + 1

    def create_course(self, name, cycle, price):
        """创建课程"""
        if self.course_is_exists(name):
            raise SomeError(u"{0}课程已存在".format(name))
        course = Course(name, cycle, price)
        self.courses.append(course)
        code = 200
        msg = u"创建课程{0}成功".format(name)

        return ResponseData(code, msg, course)

    def create_class(self, name, course_name, teacher_id):
        """创建班级"""
        if not self.course_is_exists(course_name):
            raise SomeError(u"{0}课程不存在".format(course_name))
        if not self.teacher_is_exists(teacher_id):
            raise SomeError(u"编号为{0}的讲师不存在".format(teacher_id))
        if self.class_is_exists(name):
            raise SomeError(u"{0}班级已经存在".format(name))
        class1 = Class(name, course_name, teacher_id)
        self.classes.append(class1)
        code = 200
        msg = u"创建班级{0}成功".format(name)

        return ResponseData(code, msg, class1)

    def create_student(self, name, class_name):
        """创建学员"""
        if self.class_is_exists(class_name):
            raise SomeError(u"{0}班级不存在".format(class_name))
        student_id = self.get_student_id
        student = Student(student_id, name, class_name)
        self.students.append(student)
        code = 200
        msg = u"报名成功，创建学员{0}成功".format(name)

        return ResponseData(code, msg, student)

    def create_teacher(self, name):
        emp_id = self.get_employee_id
        teacher = Teacher(emp_id, name, self.school_name)
        self.teachers.append(teacher)
        code = 200
        msg = u"创建讲师{0}成功".format(name)

        return ResponseData(code, msg, teacher)


class Course(object):
    """课程"""
    def __init__(self, name, cycle, price):

        self.name = name
        self.cycle = cycle
        self.price = price


class Teacher(object):
    """讲师"""
    def __init__(self, emp_id, name, school_name):
        self.emp_id = emp_id
        self.name = name
        self.school_name = school_name


class Student(object):
    """学生"""
    def __init__(self, student_id, name, class_name):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name


class Class(object):
    """班级"""
    def __init__(self, name, course, teacher):
        self.name = name
        self.course = course
        self.teacher = teacher


class EnrollCourse(object):
    """已选课程"""
    def __init__(self, student, school, course, class1, payment, time_stamp):
        self.student = student
        self.school = school
        self.course = course
        self.class1 = class1
        self.payment = payment
        self.time_stamp = time_stamp


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
