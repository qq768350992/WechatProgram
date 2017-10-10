#!coding:utf-8
import time, csv, random
class Stu_Various:
    def __init__(self, Teacher):
        self.t = Teacher

    def stu_login(self):
        if self.t.r == 0:
            print '考勤未开始，无法考勤'
            return False
        wechat_id = raw_input('>>输入你的微信号:')
        data = [[row[0], row[1]] for row in self.t.course_students_list]
        flag = False
        for row in data:
            if row[1].count(wechat_id) == 1:
                Stu_id = row[0]
                self.aotu_login(Stu_id)
                flag = True
                break
        if flag == False:
            print '此课程无此微信号，无法考勤'

    def aotu_login(self, Stu_id):
        num = random.randint(0,10)
        if num >= 3:
            print '>>>%s已登录' % Stu_id
            print '>>>开始认证...'
            tem = []
            for row in self.t.detail_data:
                tem.append(row)
                if row[0] == Stu_id:
                    if self.login_detail(tem, Stu_id) == False:
                        return False
            self.t.detail_data = tem
            print '签到成功'
        else:
            print '考勤认证失败，请重新自拍或联系教师'

    def login_detail(self, tem, Stu_id):
        if tem[5] == '请假':
            print '您请过假了，无法考勤'
            return
        if tem[5] == '早退':
            print '您早退了，无法考勤'
            return
        ProofPath = '\Proof\%s_%s_%s_%s.jpg' % (Stu_id, self.t.CourseID, self.t.SeqID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if self.t.r == 1:
            tem.pop()
            tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '出勤'])
        elif self.t.r == 2:
            if tem[5] == '缺勤':
                tem.pop()
                tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '迟到'])
            elif tem[5] == '出勤':
                print '你状态已是出勤，不要重复考勤啦'
        elif self.t.r == 3:
            if tem[5] == '早退1': #原来是出勤
                tem.pop()
                tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '出勤'])
            elif tem[5] == '早退2':
                tem.pop()
                tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '迟到'])
            elif tem[5] == '缺勤':
                tem.pop()
                tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '迟到'])

    def auto_com_lea(self):
        if self.t.r != 0:
            print '考勤未开启，无法请假'
            return False
        wechat_id = raw_input('>>输入你的微信号')
        data = [[row[0],row[1]] for row in self.t.course_students_list]; flag = False; lea_student_list = []
        for row in data:
            if row[1].count(wechat_id) == 1:
                Stu_id = row[0]
                num = random.randint(0, 10)
                ProofPath = '\Proof\%s_%s_%s_%s.jpg' % (Stu_id, self.t.CourseID, self.t.SeqID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print '>>>%s已登录' % Stu_id
                print '正在认证假条...'
                if num >= 3:
                    tem = []
                    for row in self.t.detail_data:
                        tem.append(row)
                        if row[5] == '请假':
                            print '你已请过假，不能再请假了'
                            return False
                        if row[0] == Stu_id:
                            tem.pop()
                            tem.append([Stu_id, self.t.Starttime, ProofPath, 'auto', 'True', '请假'])
                    self.t.detail_data = tem
                    print '请假成功'
                    flag = True
                else:
                    seq_data = [row[0] for row in csv.reader(open('../data/lea/%s_%s_lea.csv' % (self.t.TeacherID, self.t.CourseID)))]
                    if seq_data.count(Stu_id) != 0:
                        print '假条认证失败，但假条已上传给老师，你可以重新上传假条继续认证或者找老师手工请假'
                        return False
                    lea_student_list.append([str(Stu_id), self.t.SeqID])
                    csv.writer(open('../data/lea/%s_%s_lea.csv' % (self.t.TeacherID, self.t.CourseID), 'wb')).writerows(lea_student_list)
                    print '假条认证失败，但假条已上传给老师，你可以重新上传假条继续认证或者找老师手工请假'
        if flag == False:
            print '此课程无此微信号，无法请假'