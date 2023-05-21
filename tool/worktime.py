import calendar
import math
from datetime import datetime, timedelta

from enum import Enum
from operator import itemgetter

import chinese_calendar as cc


class Week(Enum):
    Monday = (1, "星期一")
    Tuesday = (2, "星期二")
    Wednesday = (3, "星期三")
    Thursday = (4, "星期四")
    Friday = (5, "星期五")
    Saturday = (6, "周六")
    Sunday = (7, "周末")


def str2time(start_date, end_date):
    try:
        s_date = datetime.strptime(str(start_date), "%Y%m%d")
        e_date = datetime.strptime(str(end_date), "%Y%m%d")
    except ValueError:
        raise "input date format error. date example:20210304"
    return s_date, e_date


def tuple2time(start_date, end_date):
    # s_date, e_date = datetime(2020, 3, 1), datetime(2020, 4, 1)
    try:
        s_date = datetime(year=start_date[0], month=start_date[1], day=start_date[2])
        e_date = datetime(year=end_date[0], month=end_date[1], day=end_date[2])
    except TypeError:
        raise "date format error. date example:(2020, 3, 1)"
    return s_date, e_date


def get_days(s_date, e_date):
    """
    [s_date,e_data]
    """
    all_days = [s_date + timedelta(idx + 0) for idx in range((e_date - s_date).days + 1)]
    workdays = sum(1 for day in all_days if day.weekday() < 5)
    weekends = sum(1 for day in all_days if day.weekday() >= 5)
    return workdays, weekends


def calc_month_workdays(month=datetime.today().month, year=datetime.today().year):
    """
    计算某月工作日天数, 返回工作日天数，休息日天数
    """
    if isinstance(month, int) or isinstance(month, float):
        month = math.ceil(month)
        if 1 <= month <= 12:
            pass
        else:
            raise "month should be in [1, 12]"
    elif isinstance(month, str):
        try:
            month = int(month)
        except ValueError:
            raise f"can't change {month} to int type."
    month_days = calendar.monthrange(year, month)[1]  # 该月对应的天数
    s_date, e_date = tuple2time((year, month, 1), (year, month, month_days))
    workdays, weekends = get_days(s_date=s_date, e_date=e_date)
    return workdays, weekends


def demo_use_standard_library():
    month = 3
    work_days, _ = calc_month_workdays(month=month)
    average_day_time = 9
    r_time = work_days * average_day_time
    print(f"{month}月份要求工时:{r_time}")


def get_dates(_year, _month) -> list:
    """获取某个月份的所有日期 datetime格式"""
    _, month_days = calendar.monthrange(_year, _month)
    s_date = datetime(_year, _month, 1)
    e_date = datetime(_year, _month, month_days)
    _dates = [(s_date + timedelta(idx)).date() for idx in range((e_date - s_date).days + 1)]
    return _dates


def calc_workday(year=None, month=None, day=None):
    try:
        import chinese_calendar as cc
    except ImportError:
        raise f"please install third-part library: pip install chinesecalendar"
    current = datetime.now()
    year = current.year if not year else year
    month = current.month if not month else month
    day = current.day if not day else day
    current_user = datetime(year=year, month=month, day=day)

    month_days = calendar.monthrange(year, month)[1]
    s_date, e_date = tuple2time((year, month, 1), (year, month, month_days))
    all_days = [s_date + timedelta(idx + 0) for idx in range((e_date - s_date).days + 1)]
    all_date = [i.date() for i in all_days]

    # 当天不计入，计算本月当天之前的工作天数和休息天数
    count_current_workday = 0
    count_current_weekday = 0
    for day in all_days:
        if day < current_user:
            if cc.is_workday(day):
                count_current_workday = count_current_workday + 1
            else:
                count_current_weekday = count_current_weekday + 1

    count_month_workday = 0
    count_month_weekday = 0
    for day in all_days:
        if cc.is_workday(day):
            count_month_workday = count_month_workday + 1
        else:
            count_month_weekday = count_month_weekday + 1

    return count_month_workday, count_month_weekday, count_current_workday, count_current_weekday


def demo_use_third_library():
    month_workday, month_weekday, current_workday, current_weekday = calc_workday(month=4, day=6)
    print(month_workday)
    print(month_weekday)
    print(current_workday)
    print(current_weekday)


if __name__ == '__main__':
    dates = get_dates(2023, 5)
    enum_workday = []
    enum_weekend = []
    for date in dates:
        day = date.day
        if cc.is_workday(date):
            enum_workday.append(day)
        else:
            enum_weekend.append(day)
    current_date = datetime.now().date()
    count_worked_days = 0
    count_off_days = 0
    for date in dates:
        if cc.is_workday(date) and (date < current_date):
            count_worked_days += 1
        elif cc.is_holiday(date) and (date < current_date):
            count_off_days += 1
    print(f"已经工作天数:{count_worked_days}\n剩余工作天数:{len(enum_workday) - count_worked_days}(含今天)")
    print(f"已经休息天数:{count_off_days}\n剩余休息天数:{len(enum_weekend) - count_off_days}(含今天)")
    stand_timesheet = len(enum_workday) * 8
    fact_timesheet = len(enum_workday) * 8.5
    print(f"本月标准工时{stand_timesheet},本月实际标准工时{fact_timesheet}")

    current_timesheet = 97.065 + 12
    remain_time = fact_timesheet - current_timesheet
    remain_days = len(enum_workday) - count_worked_days

    value = []
    for i in range(1, remain_days + 1):
        j = remain_days - i
        if i * 7 + j * 12 > remain_time:
            value.append([i, j])
    value.sort(key=itemgetter(1))
    print(f"最优解：工作7小时天数{value[0][0]}，工作12小时天数{value[0][1]}")
