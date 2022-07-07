
import time
import datetime

def getDaysinWeek():
    today = datetime.date.today()
    year, week_num, day_of_week = today.isocalendar()
    print(week_num)
    WEEK  = week_num
    startdate = time.asctime(time.strptime('2022 %d 1' % WEEK, '%Y %W %w'))
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = [startdate]
    for i in range(1, 7):
        dates.append(startdate + datetime.timedelta(days=i))

    return dates,week_num
def getDaysinWeekWithWeekNum(weeknum):
    WEEK  = weeknum
    startdate = time.asctime(time.strptime('2022 %d 1' % WEEK, '%Y %W %w'))
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = [startdate]
    for i in range(1, 7):
        dates.append(startdate + datetime.timedelta(days=i))

    return dates
def getWeekDayStr(date):
    days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    return days[date.weekday()]

# days=getDaysinWeekWithWeekNum(26)
# for day in days:
#     print(day.date(),getWeekDayStr(day))
# days=getDaysinWeek()
# for day in days:
#     print(day.date(),getWeekDayStr(day))



