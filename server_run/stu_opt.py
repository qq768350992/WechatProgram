#coding:utf-8
from course import *
class Stu_Operator:
    def __init__(self, list):
        self.list = list

    def get_my_course(self, wechat_id):
        for row in self.list:
            tem_list = get_stu_wechat_list(row[0])
            if tem_list.count(wechat_id)!=0:
                return row[0]
        print '考勤窗口未开启'
        return False

    def get_my_course_r(self, wechat_id):
        for row in self.list:
            tem_list = get_stu_wechat_list(row[0])
            if tem_list.count(wechat_id)!=0:
                return row

    def start_checkin(self, wechat_id):
        r = self.get_my_course_r(wechat_id)[1]
        if r == 0:
            print '考勤窗口未开启'
            return False
        elif r == 1:
            pass
        elif r == 2:
            pass
        else:
            pass

    def look_history_checkin(self):
        pass

#######################################################################