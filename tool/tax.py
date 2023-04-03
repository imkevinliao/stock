def taxable(amount):
    """
    级数	累计预扣预缴应纳税所得额	预扣率（%）	速算扣除数
    1	不超过36,000元的部分	3	0
    2	超过36,000元至144,000元的部分	10	2520
    3	超过144,000元至300,000元的部分	20	16920
    4	超过300,000元至420,000元的部分	25	31920
    5	超过420,000元至660,000元的部分	30	52920
    6	超过660,000元至960,000元的部分	35	85920
    7	超过960,000元的部分	45	181920
    """
    if isinstance(amount, int):
        pass
    elif isinstance(amount, float):
        pass
    else:
        raise Exception(f"amount should be number.")
    if amount < 0:
        raise Exception(f"amount should be positive number.")
    if amount == 0:
        return 0
    tax_rate = [0.03, 0.1, 0.2, 0.25, 0.30, 0.35, 0.45]
    tax_class = [0, 36000, 144000, 300000, 420000, 660000, 960000]
    tax_amount = 0
    if amount > tax_class[-1]:
        tax_amount = tax_amount + (amount - tax_class[-1]) * tax_rate[-1]
        amount = tax_class[-1]
    if amount > tax_class[-2]:
        tax_amount = tax_amount + (amount - tax_class[-2]) * tax_rate[-2]
        amount = tax_class[-2]
    if amount > tax_class[-3]:
        tax_amount = tax_amount + (amount - tax_class[-3]) * tax_rate[-3]
        amount = tax_class[-3]
    if amount > tax_class[-4]:
        tax_amount = tax_amount + (amount - tax_class[-4]) * tax_rate[-4]
        amount = tax_class[-4]
    if amount > tax_class[-5]:
        tax_amount = tax_amount + (amount - tax_class[-5]) * tax_rate[-5]
        amount = tax_class[-5]
    if amount > tax_class[-6]:
        tax_amount = tax_amount + (amount - tax_class[-6]) * tax_rate[-6]
        amount = tax_class[-6]
    if amount > tax_class[-7]:
        tax_amount = tax_amount + amount * tax_rate[-7]
    return tax_amount


"""
t_class = [0, 36000, 144000, 300000, 420000, 660000, 960000]
t_result = [taxable(i) for i in t_class]        # [0, 1080.0, 11880.0, 43080.0, 73080.0, 145080.0, 250080.0]
print(f"个人所得税档位和对应纳税金额速览:\n{[(i,j) for i,j in zip(t_class,t_result)]}")
-------result---------
个人所得税档位和对应纳税金额速览:
[(0, 0), (36000, 1080.0), (144000, 11880.0), (300000, 43080.0), (420000, 73080.0), (660000, 145080.0), (960000, 250080.0)]
"""


def personal_income_tax(year_income=None):
    """
    第一次用中文做变量，确实有些不习惯，但是易于理解才是王道.
    还好是unicode编码可以这么写，如果是ascii码就不能这么写了.
    """
    年收入 = 8000 * 12
    住房租金专项扣除 = 1500 * 12  # 三个档位：1500,1100,800
    社会保险公积金 = 5000  # 五险一金 养老 医疗 失业保险 住房公积金
    个税起征点 = 5000 * 12
    住房贷款利息专项扣除 = 0  # 自己有房子住
    子女教育专项扣除 = 0
    大病医疗专项扣除 = 0
    继续教育专项扣除 = 0
    赡养老人专项扣除 = 0
    if year_income:
        年收入 = year_income
    计税金额 = 年收入 - 住房租金专项扣除 - 个税起征点 - 子女教育专项扣除 - 大病医疗专项扣除 - 社会保险公积金 - 继续教育专项扣除 - 住房贷款利息专项扣除 - 赡养老人专项扣除
    tax_determination_amount = 计税金额
    
    if tax_determination_amount < 0:
        print(f"工资太低不配交税,这是一件悲伤的事情.")
    else:
        tax_amount = taxable(tax_determination_amount)
        print(f"应纳税金额为:{tax_amount}")


if __name__ == '__main__':
    month_incomes = [i * 1000 for i in range(5, 25)]
    year_incomes = [i * 12 for i in month_incomes]
    for m, y in zip(month_incomes, year_incomes):
        print(f"月入:{m}", end=",")
        personal_income_tax(year_income=y)
"""
月入:5000,工资太低不配交税,这是一件悲伤的事情.
月入:6000,工资太低不配交税,这是一件悲伤的事情.
月入:7000,应纳税金额为:30.0
月入:8000,应纳税金额为:390.0
月入:9000,应纳税金额为:750.0
月入:10000,应纳税金额为:1180.0
月入:11000,应纳税金额为:2380.0
月入:12000,应纳税金额为:3580.0
月入:13000,应纳税金额为:4780.0
月入:14000,应纳税金额为:5980.0
月入:15000,应纳税金额为:7180.0
月入:16000,应纳税金额为:8380.0
月入:17000,应纳税金额为:9580.0
月入:18000,应纳税金额为:10780.0
月入:19000,应纳税金额为:12080.0
月入:20000,应纳税金额为:14480.0
月入:21000,应纳税金额为:16880.0
月入:22000,应纳税金额为:19280.0
月入:23000,应纳税金额为:21680.0
月入:24000,应纳税金额为:24080.0
"""
