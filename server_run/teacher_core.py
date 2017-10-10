# coding:utf-8
import csv, time, threading, ConfigParser
from attendance_gather import final_summary, show_attendance

class tch_sign:
    def __init__(self, TeacherID, CourseID):
        self.TeacherID = TeacherID
        self.CourseID = CourseID
        self.SeqID = 1
        self.r = 0 # || 0:初始状态，无读写权限|| 1：未迟到窗口 || 2：迟到窗口 || 3：抽点窗口 ||
        self.sum_data = []
        self.detail_data = []
        self.course_students_list = []

    def start_auto(self): #开启时间窗口
        config = ConfigParser.ConfigParser()
        config.read('../interior/settings.ini')
        time_limit = int(config.get('time', 'timewindow')) #自主考勤最大持续时间
        data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (self.TeacherID, self.CourseID)))]
        for row in data:
            if data == []:
                self.SeqID = 1
            else:
                self.SeqID = len(row)
        print '第 %s 次考勤：' % self.SeqID
        self.detail_data.append(['StuID', 'checkinTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult'])
        self.Starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #获取当前时间
        data = [Stu_id[0] for Stu_id in self.course_students_list]
        for Stu_id in data:
            self.detail_data.append([Stu_id, self.Starttime, 'NULL', 'auto', 'False', '缺勤'])
        _t = threading.Timer(20*60)
        self.r = 1
        _t.start()
        self.write_seq()
        t = threading.Timer((time_limit-20)*60, self.close_all) #定时器
        self.r = 2
        t.start()
        self.r = 0

    def close_all(self):
        pass

    def exe_lea(self):
        while 1:
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            lea_student_list = [stu for stu in csv.reader(open('../data/lea/%s_%s_lea.csv' % (self.TeacherID,self.CourseID)))]
            if not lea_student_list:
                print '没有请假的学生'
                return False
            print '系统正在为您列出学生请假名单：'
            print lea_student_list
            print ('>>>输入学号,考勤次序号给予请假 ||0.退出') #raw_input  得到的是str
            f1 = raw_input('学号:')
            f2 = raw_input('考勤次序号:')
            if f1 == '0':
                break
            tem = []
            flag = 1
            for row in lea_student_list:
                tem.append(row)
                if f1 == row[0] and f2 == row[1]:
                    tem.pop()
            if flag == 1:
                print '请假失败,请检查输入'
                return
            csv.writer(open('../data/lea/%s_%s_lea.csv' % (self.TeacherID, self.CourseID), 'wb')).writerows(tem)
            self.alter_detail_sum(f1, f2, '请假')

                # self.aotu_data.append([lea_student_list[int(choose) - 1], nowTime, '请假的ProofPath', 'man', 'True', '请假'])

    def handle_data(self):
        if self.r != 0:
            print '考勤窗口未关闭,不能维护数据'
            return False
        stuID = raw_input('>>请输入学号：')
        data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv'%(self.TeacherID,self.CourseID)))]
        for row in data:
            if stuID == row[0]:
                row.pop(0)
                i = 0
                for line in row:
                    i += 1
                    print '该学生考勤次序：状态信息——>||%s:%s||' % (str(i),line)
        SeqID = raw_input('>>请输入考勤次序号：')
        studata = [stu[0] for stu in self.course_students_list]
        if studata.count(stuID) != 0:
            while 1:
                checkinResult = raw_input('>>您要把该学生的考勤状态修改成：（出勤, 请假, 迟到, 早退, 缺勤) || 0.退出')
                if checkinResult == '0':
                    break
                if ['出勤', '请假', '迟到', '早退', '缺勤'].count(checkinResult) != 0:
                    self.alter_detail_sum(stuID, SeqID, checkinResult)
                else:
                    print '输入格式错误'
        else:
            print '此学号所对应的学生不在本课堂上'

    def alter_detail_sum(self, stu_id, seq_id, check_status):
        sum_data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv'%(self.TeacherID,self.CourseID)))]
        detail_data = [row for row in csv.reader(open('../data/%s_%s_%s_checkinDetail.csv' % (self.TeacherID, self.CourseID, seq_id)))]
        if not sum_data or not detail_data:
            print '次序号输入异常'
            return
        tem_sum = [];tem_detail = []
        for row in sum_data:
            tem_sum.append(row)
            if row[0] == stu_id:
                tem_sum.pop()
                d = row; d[int(seq_id)] = check_status
                tem_sum.append(d)
        for row in detail_data:
            tem_detail.append(row)
            if row[0] == stu_id:
                tem_detail.pop()
                d = row; d[4] = 'man'; d[5] = check_status
                tem_detail.append(d)
        csv.writer(open('../data/%s_%s_%s_checkinDetail.csv' % (self.TeacherID, self.CourseID, seq_id), 'wb')).writerows(tem_detail)
        csv.writer(open('../data/sum/%s_%s_sum.csv' % (self.TeacherID, self.CourseID), 'wb')).writerows(tem_sum)
        print '修改成功'

    def search_stu(self):
        course = []
        self.course_students_list = []
        for row in [row for row in csv.DictReader(open('../interior/courseInfo.csv'))]:
            if row['TeacherID'] == str(self.TeacherID) and row['CourseID'] == str(self.CourseID):
                course.append(row['ClassName'])
        for row in [row for row in csv.DictReader(open('../interior/studentinfo.csv'))]:
            if course.count(row['ClassID']) != 0:
                self.course_students_list.append([row['StuID'],row['WeChatID']])

    def write_sum(self):
        sum_data = [row for row in csv.reader(open('../data/sum/%s_%s_sum.csv' % (self.TeacherID, self.CourseID)))]
        if not sum_data:
            sum_data = [[Stu_id[0]] for Stu_id in self.course_students_list]
            sum_data.insert(0, ['StuID'])
        with open('../data/%s_%s_%s_checkinDetail.csv' % (self.TeacherID ,self.CourseID, self.SeqID)) as csvfile:
            reader = csv.DictReader(csvfile)
            sumdata = [[stu['StuID'], stu['checkinResult']] for stu in reader]
            sum_data[0].append('checkin%d' % self.SeqID)
        j = 0
        for id in sum_data:
            for stu in sumdata:
                if stu[0] == id[0]:
                    sum_data[j].append(stu[1])
                    continue
            j += 1
        csv.writer(open('../data/sum/%s_%s_sum.csv' % (self.TeacherID, self.CourseID), 'wb')).writerows(sum_data)

    def write_seq(self):
        seq_data = [row for row in csv.reader(open('../data/seq.csv'))]
        if not seq_data:
            seq_data.append(['TeacherID', 'self.CourseID', 'SeqID', 'StartTime'])
        seq_data.append([self.TeacherID, self.CourseID, self.SeqID, self.Starttime])
        csv.writer(open('../data/seq.csv', 'wb')).writerows(seq_data)

if __name__ == "__main__":
    t = tch_sign('2004633','51610189')
    t.exe_lea()