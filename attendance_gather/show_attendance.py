#coding:utf-8
import json, csv
def msg(list): #显示学生考勤信息
    # list:传入学生考勤列表
    i = 1
    for stu in [row for row in csv.reader(open('../interior/studentinfo.csv'))]:
        for row in list:
            if stu.count(row) != 0: #格式化处理
                d = stu
                d.pop()
                if i < 10:
                    print '',i,
                else:
                    print i,
                print json.dumps(d, encoding="utf-8", ensure_ascii=False)  #显示学生考勤信息
                i += 1
                break
    return i-1 #list中人数

def atd(TeacherID, CourseID, SeqID): #学生考勤信息
    queqin_tem = []
    chuqin = 0; chidao = 0; zaotui = 0; queqin = 0; qingjia = 0
    data = [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (TeacherID, CourseID, SeqID)))]
    if data != []:
        data.pop(0)
    for row in data:
        if row[5] == '出勤':
            chuqin += 1
        elif row[5] == '迟到':
            chidao += 1
        elif row[5] == '早退':
            zaotui += 1
        elif row[5] == '缺勤':
            queqin += 1
            queqin_tem.append(row[0])
        else:
            qingjia += 1
    print '出勤率: %.2f%%' % (float(chuqin) / (chuqin + chidao + zaotui + queqin + qingjia) * 100)
    print '请假人数: %d' % qingjia
    print '缺勤学生名单:'
    msg(queqin_tem)