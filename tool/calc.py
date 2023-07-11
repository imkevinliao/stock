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




def exchange(amount=10000, broker_rate=0.25 * 0.001, transfer_rate=0.02 * 0.001, stamp_duty=0.001):
    # 单次交易成本 2w以内手续费5￥
    broker_cost = amount * broker_rate
    transfer_cost = amount * transfer_rate
    buy_cost = broker_cost + transfer_cost
    
    broker_cost = amount * broker_rate
    if broker_cost < 5:
        broker_cost = 5
    transfer_cost = amount * transfer_rate
    stamp_cost = amount * stamp_duty
    sell_cost = broker_cost + transfer_cost + stamp_cost
    
    buy_sell_cost = buy_cost + sell_cost
    return round(buy_sell_cost, 2)

def cost(amount, in_price, out_price):
    # 股票交易，金额，买入价格，卖出价格
    earn = amount * ((out_price - in_price) / in_price)
    cost_must = exchange(amount)
    earn = earn - cost_must
    return earn


def compound_interest():  # 复利投资
    months = 12
    init_amount = 5 * 10000
    invest_per_month = 3 * 1000
    year_rate = 3 * 0.01
    invest_years = 10
    month_rate = year_rate / months
    
    # 本金复利计算
    gain1 = init_amount * (1 + month_rate) ** (months * invest_years)
    cost1 = init_amount
    # 定投计算
    gain2 = invest_per_month * (1 + month_rate) * (-1 + (1 + month_rate) ** (months * invest_years)) / month_rate
    cost2 = invest_per_month * months * invest_years
    
    print(
        f"基本信息:\n初始资金:{init_amount / 10000}万,年化收益利率{year_rate},每月定投:{invest_per_month / 1000}千,投资时间{invest_years}年")
    
    print(f"本金收益:{int(gain1 - cost1) / 10000}万,收益率:{(gain1 - cost1) / cost1:0.3}")
    print(f"定投收益:{int(gain2 - cost2) / 10000}万,收益率:{(gain2 - cost2) / cost2:0.3}")
    print(
        f"综合收益:{int(gain2 + gain1 - cost1 - cost2) / 10000}万,综合成本:{int(cost1 + cost2) / 10000}万,综合收益率:{int(gain1 + gain2 - cost1 - cost2) / (cost1 + cost2):0.3}")
    
    """
    基本信息:
    初始资金:5.0万,年化收益利率0.03,每月定投:3.0千,投资时间10年
    本金收益:1.7467万,收益率:0.349
    定投收益:6.0272万,收益率:0.167
    综合收益:7.7739万,综合成本:41.0万,综合收益率:0.19
    """
    
if __name__ == '__main__':
    in_data = (None, 0.029, None, 12000, None)
    calc(capital=in_data[0], year_rate=in_data[1], day_rate=in_data[2], year_gain=in_data[3], day_gain=in_data[4])
    
    
    
"""
计算的结果：
本金：413793.1034
年利率：0.029000，日利率：0.00007945
年收益：12000.00，日收益：32.8767
"""
