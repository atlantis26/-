# coding:utf-8
from core.handler import Handler


class TeacherView(object):
    """讲师视图"""
    def __init__(self, username):
        self.username = username
        self.console()

    def console(self):
        """ 教师视图主页"""
        print(u"欢迎教师‘{0}’登录本学员管理系统...".format(self.username))
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.创建班级                   <\033[36;1m2\033[0m>.删除班级
                    <\033[36;1m3\033[0m>.修改班级                   <\033[36;1m4\033[0m>.查询班级信息
                    <\033[36;1m5\033[0m>.查询班级列表               <\033[36;1m6\033[0m>.创建上课记录  
                    <\033[36;1m7\033[0m>.查询上课记录列表            <\033[36;1m8\033[0m>.根据上课记录查询作业
                    <\033[36;1m9\033[0m>.修改学员作业成绩            <\033[36;1m10\033[0m>.根据qq号添加班级学员
                    <\033[36;1m11\033[0m>.退出视图
            """
            print(msg)
            actions = {"1": self.create_class,
                       "2": self.delete_class,
                       "3": self.modify_class,
                       "4": self.query_class,
                       "5": self.list_class,
                       "6": self.create_record,
                       "7": self.list_record,
                       "8": self.list_homework_by_record_id,
                       "9": self.update_homework_score,
                       "10": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    @staticmethod
    def create_class():
        name = input(u"请输入班级名称：").strip()
        rsp = Handler.create_class(name)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    @staticmethod
    def delete_class():
        class_id = input(u"请输入班级的id：").strip()
        rsp = Handler.delete_class(class_id)
        print(rsp.msg)

    @staticmethod
    def modify_class():
        class_id = input(u"请输入班级的id：").strip()
        name = input(u"请输入班级名称：").strip()
        rsp = Handler.update_class(class_id, name)
        print(rsp.msg)

    @staticmethod
    def query_class():
        class_id = input(u"请输入班级的id：").strip()
        rsp = Handler.query_class(class_id)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    @staticmethod
    def list_class():
        rsp = Handler.list_class()
        if rsp.code == 200:
            for cl in rsp.data:
                print(cl)
        print(rsp.msg)

    def create_record(self):
        class_id = input(u"请输入班级的id：").strip()
        description = input(u"请输入课程|作业的描述信息：").strip()
        rsp = Handler.create_record(self.username, class_id, description)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    @staticmethod
    def list_record():
        rsp = Handler.list_record()
        if rsp.code == 200:
            for r in rsp.data:
                print(r)
        print(rsp.msg)

    @staticmethod
    def list_homework_by_record_id():
        record_id = input(u"请输入上课记录的id：").strip()
        rsp = Handler.list_homework_by_record_id(record_id)
        if rsp.code == 200:
            for h in rsp.data:
                print(h)
        print(rsp.msg)

    @staticmethod
    def update_homework_score():
        homework_id = input(u"请输入学员的家庭作业记录id：").strip()
        score = eval(input(u"请输入该作业的成绩分数：").strip())
        rsp = Handler.update_homework_score(homework_id, score)
        print(rsp.msg)

    @staticmethod
    def class_add_student_by_qq():
        class_id = input(u"请输入班级的id：").strip()
        qq = input(u"请输入注册学员的qq号：").strip()
        rsp = Handler.class_add_student_by_qq(class_id, qq)
        print(rsp.msg)

    @staticmethod
    def logout():
        print("欢迎您再次访问本系统，再见")
        exit()
