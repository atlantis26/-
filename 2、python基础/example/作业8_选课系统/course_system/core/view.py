# coding:utf-8
class StudentView(object):
    """学员视图"""
    def register(self):
        """注册"""
        pass

    def pay(self):
        """交学费"""
        pass

    def select(self):
        """选择班级"""
        pass


class TeacherView(object):
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


class MangerView(object):
    """管理视图"""
    def create_teacher(self):
        """创建讲师"""
        pass

    def create_class(self):
        """创建班级"""
        pass

    def create_course(self):
        """创建课程"""
        pass
