import csv
import datetime

from matplotlib import dates, pyplot as plt

from soc import Analyze, CodeType

filepath = r"../data/三大指数历史收益率.csv"


def get_index_close(data, year):
    year_data = data[data["date"].dt.strftime('%Y') == f'{year}']
    data_head_tail = year_data.iloc[[0, -1]]
    close_head = data_head_tail["close"].iloc[0]  # 年初第一条数据
    close_tail = data_head_tail["close"].iloc[1]  # 年末最后一条数据
    return close_head, close_tail


def index():
    def get_year_rate(_data):
        year_rate = []
        last_idx = len(_data) - 1
        for idx, value in enumerate(_data):
            _year = value[0]
            head_close = value[1]
            if idx != last_idx:
                tail_close = _data[idx + 1][1]
                rate = (tail_close - head_close) / head_close
                rate = round(rate, 3)
                year_rate.append([_year, rate])
        return year_rate
    
    years = [str(i) for i in range(2006, 2024)]
    data_50 = Analyze(code="sh000016", codetype=CodeType.INDEX).data
    data_500 = Analyze(code="sh000905", codetype=CodeType.INDEX).data
    data_300 = Analyze(code="sh000300", codetype=CodeType.INDEX).data
    list_50 = []
    list_500 = []
    list_300 = []
    for year in years:
        head, tail = get_index_close(data_50, year)
        list_50.append([year, head])
        head, tail = get_index_close(data_500, year)
        list_500.append([year, head])
        head, tail = get_index_close(data_300, year)
        list_300.append([year, head])
    formatter = dates.DateFormatter("%Y")
    user_interval = dates.YearLocator(base=2)
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
    ax = plt.subplot()
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(user_interval)
    new_years = [datetime.datetime.strptime(year, "%Y") for year in years]
    plt.plot(new_years, [value[1] for value in list_50], color='g', label="上证50")
    plt.plot(new_years, [value[1] for value in list_500], color='r', label="中证500")
    plt.plot(new_years, [value[1] for value in list_300], color='b', label="沪深300")
    plt.legend(bbox_to_anchor=(0.25, 0.95), loc=1, borderaxespad=0)
    plt.show()
    rate_50 = get_year_rate(_data=list_50)
    rate_500 = get_year_rate(_data=list_500)
    rate_300 = get_year_rate(_data=list_300)
    col_1 = [i[0] for i in rate_50]
    col_2 = [i[1] for i in rate_50]
    col_3 = [i[1] for i in rate_500]
    col_4 = [i[1] for i in rate_300]
    all_rate = list(zip(col_1, col_2, col_3, col_4))
    with open(filepath, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["年份", "上证50", "中证500", "沪深300"])
        writer.writerows(all_rate)


if __name__ == '__main__':
    index()
