import calendar
import math
from datetime import datetime, timedelta


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


if __name__ == '__main__':
    month = 3
    work_days, _ = calc_month_workdays(month=month)
    average_day_time = 9
    r_time = work_days * average_day_time
    print(f"{month}月份要求工时:{r_time}")

"""
3月份要求工时:207
"""
