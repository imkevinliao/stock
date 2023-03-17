import collections
import functools
import inspect
from decimal import getcontext, Decimal

YEAR2DAY = 365


def calc(capital=None, year_rate=None, day_rate=None, year_gain=None, day_gain=None):
    """
    给定本金，利率，收益，三者任意其二，计算其他参数值
    """

    def recalculate(year, day, max_error_range=0.1):
        if year == 0 or day == 0:
            raise Exception("0 is not allowed.")
        getcontext().prec = 10
        new_day = Decimal(year) / YEAR2DAY
        year_offsets = abs((float(new_day) - day) / day)
        new_year = Decimal(day) * YEAR2DAY
        day_offsets = abs((float(new_year) - year) / year)
        if min(year_offsets, day_offsets) > max_error_range:
            raise Exception(f"给定的 {year} 和 {day} 数值关系不匹配,若无法确保两者一致，请只给一个")
        else:
            if year_offsets > day_offsets:
                day = year / YEAR2DAY
            elif day_offsets > year_offsets:
                year = day * YEAR2DAY
        return year, day

    condition_nums = 0
    flag_capital = False
    flag_rate = False
    flag_gain = False
    if capital:
        flag_capital = True
        condition_nums = condition_nums + 1
    if year_rate or day_rate:
        flag_rate = True
        condition_nums = condition_nums + 1
    if year_gain or day_gain:
        flag_gain = True
        condition_nums = condition_nums + 1
    if condition_nums < 2:
        raise Exception("请至少给两个不同类型的条件")

    if year_rate and day_rate:
        year_rate, day_rate = recalculate(year_rate, day_rate)
    elif year_rate:
        day_rate = year_rate / YEAR2DAY
    elif day_rate:
        year_rate = day_rate * YEAR2DAY

    if year_gain and day_gain:
        year_gain, day_gain = recalculate(year_gain, day_gain)
    elif year_gain:
        day_gain = year_gain / YEAR2DAY
    elif day_gain:
        year_gain = day_gain * YEAR2DAY

    if condition_nums == 3:
        print(f"您给定了所有条件，暂不对您给定数值合理性验证，下面是转化结果：")
    elif condition_nums == 2:
        if not flag_capital:
            capital = year_gain / year_rate
        elif not flag_gain:
            year_gain = capital * year_rate
            day_gain = year_gain / YEAR2DAY
        elif not flag_rate:
            year_rate = year_gain / capital
            day_rate = year_rate / YEAR2DAY
        print(f"计算的结果：")
    print(f"本金：{capital:0.04f}")
    print(f"年利率：{year_rate:0.06f}，日利率：{day_rate:0.08f}")
    print(f"年收益：{year_gain:0.02f}，日收益：{day_gain:0.04f}")


if __name__ == '__main__':
    in_data = (10000, 0.020075, None, None, None)
    calc(capital=in_data[0], year_rate=in_data[1], day_rate=in_data[2], year_gain=in_data[3], day_gain=in_data[4])
