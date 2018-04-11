# coding:utf-8
from core.orm import SomeError


class _BaseView(object):
    def __init__(self, schools=list()):
        self.schools = schools

    @property
    def list_schools(self):
        """列出所有的学校"""
        return self.schools

    @property
    def list_all_courses(self):
        """列出所有的课程"""
        course_list = list()
        for cl in [school.courses for school in self.schools]:
            course_list.extend(cl)
        return list(set(course_list))


class StudentView(_BaseView):
    """学员视图"""
    def __init__(self, student, schools):
        self.student = student
        _BaseView.__init__(self, schools)

    def get_school_by_name(self, school_name):
        """根据名字查询学校"""
        school_list = [s for s in self.list_schools if s.school_name == school_name]
        if not school_list:
            raise SomeError(u"{0}学校不存在".format(school_name))
        return school_list[0]

    def get_course_by_name(self, school_name, course_name):
        """根据名字查询课程"""
        school = self.get_school_by_name(school_name)
        course_list = [c for c in school.courses if c.name == course_name]
        if not course_list:
            raise SomeError(u"{0}学校不存在{1}课程".format(school_name, course_name))
        return course_list[0]

    def get_classes_by_course(self, school_name, course_name):
        """根据学校课程名查询班级"""
        school = self.get_school_by_name(school_name)
        return [cls for cls in school.classes if cls.course == course_name]

    def get_schools_by_course(self, course_name):
        """列出有课程的学校"""
        school_list = list()
        for school in self.schools:
            for course in school.courses:
                if course.name == course_name:
                    school_list.append(school)
        return school_list

    def select_by_school(self, username):
        """按照学校选课程报名"""
        try:
            schools = self.list_schools
            print(u"查询可报名的学校： ")
            for school in schools:
                print(school.school_name)
            school_name = input(u"请输入您选择的学校：").strip()
            school = self.get_school_by_name(school_name)
            print(u"可选择的课程：")
            for course in school.courses():
                print(course.name)
            course_name = input(u"请输入您的选择的课程：").strip()
            print(u"可选择的班级：")
            class_list = self.get_classes_by_course(school_name, course_name)
            for class1 in class_list:
                print(class1.name)
            class_name = input(u"请输入您选择的班级：").strip()
            if not [c for c in class_list if c.name == class_name]:
                raise SomeError(u"{0}学校的{1}课程不存在{2}班级)".format(school_name, course_name, class_name))
            rsp = school.create_student(username, class_name)
            msg = rsp.msg
        except SomeError as e:
            msg = "报名课程失败，原因：{0}".format(str(e))
        print(msg)

    def select_by_course(self, username):
        """按照课程选学校报名"""
        try:
            courses_list = self.list_all_courses
            print(u"查询报名学习的课程： ")
            for courses in courses_list:
                print(courses.name)
            course_name = input(u"请输入您选择的课程：").strip()
            school_list = self.get_schools_by_course(course_name)
            print(u"可选择的学校：")
            for school in school_list:
                print(school.school_name)
            school_name = input(u"请输入您的选择的学校：").strip()
            print(u"可选择的班级：")
            class_list = self.get_classes_by_course(school_name, course_name)
            for class1 in class_list:
                print(class1.name)
            class_name = input(u"请输入您选择的班级：").strip()
            if not [c for c in class_list if c.name == class_name]:
                raise SomeError(u"{0}学校的{1}课程不存在{2}班级)".format(school_name, course_name, class_name))
            school = self.get_school_by_name(school_name)
            rsp = school.create_student(username, class_name)
            msg = rsp.msg
        except SomeError as e:
            msg = "报名课程失败，原因：{0}".format(str(e))
        print(msg)



    def pay(self):
        """交学费"""
        pass


    def __str__(self):
        msg = ""


class TeacherView(_BaseView):
    """讲师视图"""
    def select_class(self):
        """选择班级"""
        pass

    def list_students(self):
        """查看班级学员列表"""
        pass

    def modify_student(self):
        """修改学员成绩"""
        pass


class MangerView(_BaseView):
    """管理视图"""

    def __init__(self):
        self.teachers = list()
        self.classes = list()
        self.courses = list()

    def create_teacher(self, teacher):
        """创建讲师"""
        self.teachers.append(teacher)

    def create_class(self, cls):
        """创建班级"""
        self.classes.append(cls)

    def create_course(self, course):
        """创建课程"""
        self.courses.append(course)
