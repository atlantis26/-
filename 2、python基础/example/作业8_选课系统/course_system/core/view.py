# coding:utf-8


class _BaseView(object):
    def __init__(self, schools=list()):
        self.schools = schools

    @property
    def list_school_name(self):
        return [school.school_name for school in self.schools]


class StudentView(_BaseView):
    """学员视图"""
    def register(self):
        """注册学校课程"""
        # 选择学校
        schools = self.list_school_name
        print(u"你可以报名注册的学校： ")
        for school in schools:
            print(school)
        # 选择课程
        # 选择班级
        pass

    def pay(self):
        """交学费"""
        pass

    def select(self):
        """选择班级"""
        pass


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
