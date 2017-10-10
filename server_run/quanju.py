# #coding:utf-8
# import csv
# class Queue:
#     def __init__(self):
#         self.list = []
#         self.tem_list = [] #wechatid, r, course_id, teacher_id, seq_id
#     def login_and_add_list(self):
#         tea_wechat_id = raw_input('input your wechatID')
#         tea_id = ''
#         for row in [row for row in csv.DictReader(open('../interior/teacherInfo.csv'))]:
#             if row['WeChatID'] == tea_wechat_id:
#                 tea_id = row['TeacherID']
#         if tea_id == '':
#             print '无此微信号'
#             return
#         tea_course_id = raw_input('input your courseID')
#
#
#      def build_wechat_id(self):
#         stu_wechat_id_list = []
#         course = []
#         for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
#             if row['TeacherID'] == tea_id and row['CourseID'] == tea_course_id:
#                 course.append(row['ClassName'])
#         for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
#             if course.count(row['ClassID']) != 0:
#                 stu_wechat_id_list.append(row['WeChatID'])
#         return stu_wechat_id_list
#
#      def build_
#
#
#
