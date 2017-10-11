# coding:utf-8
import time,ConfigParser,re
from course import *

class Check_In:
    def __init__(self, course_id):
        self.course_id = course_id
        self.msg = ''

    def get_start_time(self):
        return time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]

    def get_end_time(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../interior/settings.ini')
        time_limit = int(cf.get('time', 'timewindow'))*60
        local_time = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        return time_limit + local_time

    def get_class_over_time(self, start_time):
        cf = ConfigParser.ConfigParser()
        cf.read('../interior/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        Time_info = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)
        first_time = Time_info[0]
        last_time = Time_info[len(Time_info)-1]
        for row in Time_info:
            if start_time > row[0] and start_time < row[1]:
                return row[1]
        if start_time < first_time[0] or start_time > last_time[0]:
            return first_time[1]
        return False

    # has list 是否已存在
    # for 自己
    def has_tea_wechat(self, list):
        for row in list:
            if get_teacher_id(row[0]) == get_teacher_id(self.course_id):
                if row[2] <= row[3]:
                    return True
                elif self.get_start_time() > row[3]:
                    return row[0]
        return False

    # for other 可以不要 被has_stu_wechat取代 cuo
    def has_course(self, list):
        for row in list:
            if self.course_id == row[0]:
                if row[2] <= row[3]:
                    return True
                elif self.get_start_time() > row[3]:
                    return row[0]
        return False

    # for other 此函数不面向学生look
    def has_stu_wechat(self, list):
        stu_data = get_stu_wechat_list(self.course_id)
        for row in list:
            stu_tem = get_stu_wechat_list(row[0])
            for d in stu_data:
                if stu_tem.count(d) != 0:
                    if row[2] <= row[3]:
                        return True
                    elif self.get_start_time() > row[3]:
                        return row[0]
        return False

    def error(self):
        print '%s' % self.msg

    # 当前时间还在本节课节次中
    def can_add(self, list):
        if type(self.has_course(list)) != bool:
            return self.has_course(list)
        if type(self.has_tea_wechat(list)) != bool:
            return self.has_tea_wechat(list)
        if type(self.has_stu_wechat(list)) != bool:
            return self.has_stu_wechat(list)
        if self.has_tea_wechat(list) == True:
            if self.has_course(list) == True:
                self.msg = '此课程的时间窗口已被你开启过,且仍在运行'
                return False
            else:
                self.msg = '你有其它课程的时间窗口仍在运行'
                return False
        else:
            if self.has_course(list) != False:
                self.msg = '此课程的时间窗口被其它老师占用'
                return False
            elif self.has_stu_wechat(list) != False:
                self.msg = '此课程的部分学生在上课'
                return False
            else:
                return True

# if __name__ == '__main__':
#     open = Check_In('51610189')
#     list = [['51610166',1,44,3]]
#     print open.can_add(list)