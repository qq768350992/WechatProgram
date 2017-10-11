# coding:utf-8
import stu_opt
import threading
import ConfigParser
from course import *
import open_checkin


class Core:
    def __init__(self):
        self.list = [['516188',0,1,2]]

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
        start_time = op.get_start_time()

        if op.can_add(self.list) == True:
            op.error()
            self.list.append([course_id, 1, op.get_end_time(), op.get_class_over_time(start_time)])
        elif op.can_add(self.list) == False:
            op.error()
            return
        else:
            op.error()
            for row in self.list:
                if row[0] == op.can_add(list):
                    row[0] = course_id 1
                    row[1] = 0
                    row[2] = op.get_end_time()
                    row[3]=op.get_class_over_time(start_time)
        print self.list
        t1 = threading.Timer(2, self.close, (2, course_id))
        t1.start()

        t2 = threading.Timer(5, self.close, (0, course_id))
        t2.start()

    def close(self, r, course_id):
        if r == 0:
            i = 0
            for row in self.list:
                if row[0] == course_id:
                    self.list.pop(i)
                i += 1
        else:
            self.list = set_r(r, self.list, course_id)
        print self.list

#################################################
if __name__ == '__main__':
    c = Core()
    c.tea_check_in('51610189')