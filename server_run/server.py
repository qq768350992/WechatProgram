# coding:utf-8
import stu_opt
import threading
import ConfigParser
from course import *
import open_checkin


class Core:
    def __init__(self):
        self.list = []

    def tea_ui(self):
        # course_id入手
        course_id = raw_input('>>你的课程号是:')

        # 1.开启考勤
        self.tea_check_in(course_id)
        # 2.抽点考勤
        self.tea_random(course_id)
        # 3.批假（简单）
        # 4.修改考勤记录
        # 5.手工批假

    def stu_ui(self):
        opt = stu_opt.Stu_Operator(self.list)

    def adm_ui(self):
        pass

    def tea_random(self, course_id):
        self.list = set_r(3, self.list, course_id)

    def tea_check_in(self, course_id):
        config = ConfigParser.ConfigParser()
        config.read('../interior/settings.ini')
        # 时间窗口持续时间
        time_limit = int(config.get('time', 'timewindow'))
        # 正点时间
        op = open_checkin.Check_In(course_id)
        if op.can_add(list) == False:
            return

        t = threading.Timer(25 * 60)
        start_time = op.get_start_time()
        self.list = set_r(1, self.list, course_id)
        self.list.append([course_id, 0, op.get_end_time(), op.get_class_over_time(start_time)])
        t.start()


        t = threading.Timer((time_limit - 25) * 60)
        self.list = set_r(2, self.list, course_id)
        t.start()
        self.list = set_r(0, self.list, course_id)
        self.list.pop()

#################################################