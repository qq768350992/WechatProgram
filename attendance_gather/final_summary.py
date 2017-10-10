#!coding:utf-8
import textwrap, csv
class Final_Sum:
#每节课出勤率, 平均出勤率, 每次上课出勤情况统计表(平时成绩表)
    def __init__(self, TeacherID, CourseID):
        self.TeacherID = TeacherID
        self.CourseID = CourseID
        self.len_row = 0
        self.student_msg = self.get_student_msg() #学生日常考勤信息

    def get_student_msg(self): #初始化
        student_msg = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (self.TeacherID, self.CourseID)))]
        if student_msg != []:
            student_msg.pop(0)
        return student_msg

    def get_attandance_msg(self): #学生考勤信息
        for row in self.student_msg:
            self.len_row = len(row)
            break
        sum_atd = 0
        for i in range(1, self.len_row):
            queqin_tem = []
            chuqin = 0; chidao = 0; zaotui = 0; queqin = 0; qingjia = 0
            for row in self.student_msg:
                if row[i] == '出勤':
                    chuqin += 1
                elif row[i] == '迟到':
                    chidao += 1
                elif row[i] == '早退':
                    zaotui += 1
                elif row[i] == '缺勤':
                    queqin += 1
                    queqin_tem.append(row[0])
                else:
                    qingjia += 1
            print '第 %s 节次出勤率: %.2f%%' % (i, float(chuqin) / (chuqin + chidao + zaotui + queqin + qingjia) * 100)
            sum_atd += float(chuqin) / (chuqin + chidao + zaotui + queqin + qingjia) * 100
        print '\n----平均出勤率----: %.2f%%' % (sum_atd/(self.len_row-1))

    def get_score(self): #学生平均分
        stu_score = []
        for row in self.student_msg:
            tem_score = 100
            for i in range(1, len(row)): #每个人100分 缺勤 -3 迟到 -1 早退 -1
                if ['迟到','早退'].count(row[i]):
                    tem_score -= 3
                elif ['缺勤'].count(row[i]):
                    tem_score -= 5
                else:
                    pass
                if tem_score < 0: #平时分最少 0
                    tem_score = 0
            stu_score.append([row[0], tem_score])
        if stu_score == []:
            return False
        print '\n-----平时分------：'
        print(textwrap.fill(str(stu_score), width=30)) #格式化