import calendar
import math
from datetime import datetime, timedelta
from enum import Enum


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
    """
    使用标准库函数无法准确判别节假日这类情况，所以使用第三方库 chinesecalendar 判断是否为工作日，这种计算更为准确但是需要先安装第三方库.
    """
    # 可以手动指定当前是哪一天，不指定默认是程序运行当天
    month_workday, month_weekday, current_workday, current_weekday = calc_workday(month=None, day=None)
    # 月平均工时要求
    month_average_hours = 9
    # 已经完成的工时和剩余工时(手动填写当前工时数)
    completed_work_hours = 0
    
    month_work_hours = month_workday * month_average_hours
    current_work_hours = current_workday * month_work_hours
    
    completed_workday = current_workday
    remaining_workday = month_workday - current_workday
    
    remaining_work_hours = month_work_hours - completed_work_hours
    # 计算接下来为了完成工时，需要每天工作多久：剩余工作时间/剩余工作天数
    next_day_hours = remaining_work_hours / (month_workday - current_workday)
    
    # 假定晚上19点下班，当天工时计为8小时
    base_time = [19, 8]
    off_duty = next_day_hours - base_time[1] + base_time[0]
    if off_duty > 24:
        print(f"没救了，工时补不回来的")
    if off_duty < 0:
        print(f"没救了，工时太多了，新时代卷王，加班狂魔.")
    minutes, hours = math.modf(off_duty)
    minutes = int(minutes * 60)
    hours = int(hours)
    print(f"您的下班时间为 {hours}:{minutes}")
