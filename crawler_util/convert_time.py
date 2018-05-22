import datetime


def local_date(thestr):
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
              "October", "November", "December")

    if thestr.find('(') > 0:
        thestr = thestr[0:thestr.find('(')].strip()
    time_lst = thestr.split(' ')
    lenth = len(time_lst)
    if lenth >= 3:
        year = int(time_lst[2])
        month = months.index(time_lst[1]) + 1
        day = int(time_lst[0])
        return datetime.date(year, month, day)
    elif lenth == 2:
        year = int(time_lst[1])
        month = months.index(time_lst[0]) + 1
        return datetime.date(year, month, 1)
    elif lenth == 1:
        year = int(time_lst[0])
        return datetime.date(year, 1, 1)
    return datetime.date.min


def filter_time(time):
    if time is None:
        return None
    timestr = str(time)
    res = time
    if len(timestr) == 4:
        res = int(timestr[:2])
    if len(timestr) == 5:
        tem1 = int(timestr[:2])
        if tem1 > 30:
            res = tem1
        else:
            res = int(timestr[:3])
    if len(timestr) == 6:
        res = int(timestr[:3])
    if res in range(30, 400):
        return res
    if int(timestr[:3]) in range(30, 400):
        return int(timestr[:3])
    else:
        return int(timestr[:2])
