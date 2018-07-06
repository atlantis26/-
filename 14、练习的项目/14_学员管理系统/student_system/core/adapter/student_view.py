# coding:utf-8
from core.handler import Handler


class StudentView(object):
    """学员视图"""
    def __init__(self, username):
        self.username = username

    def console(self):
        """ 学员视图主页"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.我的个人信息               <\033[36;1m2\033[0m>.我的作业
                    <\033[36;1m3\033[0m>.提交作业                   <\033[36;1m4\033[0m>.查看成绩与排名
                    <\033[36;1m5\033[0m>.退出视图
            """
            print(msg)
            actions = {"1": self.student_info,
                       "2": self.student_homework,
                       "3": self.commit_homework,
                       "4": self.query_score_and_rank,
                       "5": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    def student_info(self):
        rsp = Handler.show_student_info(self.username)
        if rsp.code == 200:
            student, class1 = rsp.data
            print("您的个人信息：{0}".format(student))
            print("您报名的班级：{0}".format(class1))
        print(rsp.msg)

    @staticmethod
    def student_homework():
        pass

    @staticmethod
    def commit_homework():
        class_id = input(u"请输入班级的id:").strip()
        record_id = input(u"请输入上课课程id:").strip()
        file_path = input(u"请输入您的课程作业上传文件:").strip()
        rsp = Handler.commit_homework(class_id, record_id, file_path)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    def query_score_and_rank(self):
        pass


    def logout(self):
        pass
