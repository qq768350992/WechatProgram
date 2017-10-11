# coding:utf-8
import csv

def get_teacher_id(course_id):
    tem = [row[2] for row in csv.reader(open('../interior/courseInfo.csv'))];tem.pop(0)
    data = [[row[0],row[2]] for row in csv.reader(open('../interior/courseInfo.csv'))];data.pop(0)
    for row in list(set(tem)):  # set集合 优点不重复 以教工号为主
        for d in data:
            if row == d[1] and course_id == d[0]:
                return d[1]

def get_stu_wechat_list(course_id):
    course = []
    stu_wechat_list = []
    for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
        if row['TeacherID'] == get_teacher_id(course_id) and row['CourseID'] == course_id:
            course.append(row['ClassName'])
    for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
        if course.count(row['ClassID']) != 0:
            stu_wechat_list.append(row['WeChatID'])
    return stu_wechat_list

def set_r(r, list, course_id):
    tem = []
    for row in list:
        tem.append(row)
        if row[0] == course_id:
            tem.pop();d = row;d[1] = r;tem.append(d)
    return tem

def get_seq_id(course_id):
    data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (get_teacher_id(course_id), course_id)))]
    if not data:
        return 1
    else:
        return len(data)





