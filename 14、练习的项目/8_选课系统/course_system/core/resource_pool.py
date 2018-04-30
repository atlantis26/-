# coding:utf-8
import pickle
import os


class ResourcesPool(object):
    """统一管理系统生成的学校、班级、课程、讲师、学生等资源数据"""
    def __init__(self, schools=list(), classes=list(), courses=list(), teachers=list(), students=list()):
        self.schools = schools
        self.classes = classes
        self.courses = courses
        self.teachers = teachers
        self.students = students

    @property
    def get_school_id(self):
        """生成新学校的编号"""
        return len(self.schools)

    @property
    def get_class_id(self):
        """生成新班级的编号"""
        return len(self.classes)

    @property
    def get_course_id(self):
        """生成新课程的编号"""
        return len(self.courses)

    @property
    def get_teacher_id(self):
        """生成新讲师的工号"""
        return len(self.teachers)

    @property
    def get_student_id(self):
        """生成新学员的学号"""
        return len(self.students)

    def school_is_exists(self, name):
        """判断学校已存在, 名字唯一"""
        schools = [school for school in self.schools if school.name == name]
        return schools[0] if schools else False

    def course_is_exists(self, school_id, name):
        """判断课程已存在, 同一学校课程名字唯一"""
        courses = [course for course in self.courses if (course.name == name and course.school_id == school_id)]
        return courses[0] if courses else False

    def class_is_exists(self, school_id, name):
        """判断班级已存在，同一学校班级名字唯一"""
        classes = [cla for cla in self.classes if (cla.name == name and cla.school_id == school_id)]
        return classes[0] if classes else False

    def student_is_exist(self, username):
        """判断学员已存在，学员系统用户名唯一"""
        students = [student for student in self.students if (student.username == username)]
        return students[0] if students else False

    def teacher_is_exist(self, username):
        """判断讲师已存在，讲师系统用户名唯一"""
        teachers = [teacher for teacher in self.teachers if (teacher.username == username)]
        return teachers[0] if teachers else False


def init_resources_pool(resource_pool_dir):
    """初始化系统资源池，如果已被创建保存，则通过pickle重构对象"""
    resource_pool_file = os.path.join(resource_pool_dir, "ResourcePool.pkl")
    if os.path.exists(resource_pool_file):
        with open(resource_pool_file, 'rb') as f:
            resource_pool = pickle.load(f)
    else:
        resource_pool = ResourcesPool()
        with open(resource_pool_file, 'wb') as f:
            pickle.dump(resource_pool, f)
            f.flush()
    return resource_pool
