import time,ConfigParser,re
cf = ConfigParser.ConfigParser()
cf.read('../interior/settings.ini')
info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
Time_info = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)
print  time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
print Time_info




