import datetime
import os
import re

import akshare as ak
import pandas as pd
from matplotlib import pyplot as plt


class ErrorInfo(Exception): ...


class Analyze:
    def __init__(self, csvfile, stock_name=""):
        self.csvfile = csvfile
        self.stock_name = stock_name
        self.data = pd.read_csv(self.csvfile)
        self.pretreatment()

    def __extract_stock_name(self):
        _, fullname = os.path.split(self.csvfile)
        regex = r"\d{3,8}"
        result = re.findall(regex, fullname)
        if result:
            self.stock_name = result[0]

    def pretreatment(self):
        self.data["日期"] = pd.to_datetime(self.data["日期"])
        # 如果没有给定股票代号，那么就尝试从文件名中提取
        if not self.stock_name:
            self.__extract_stock_name()

    def basic_info(self):
        data = self.data
        print(f"下面展示文件 {self.csvfile} 的详细数据：{self.stock_name}")
        records = data.shape[0]
        high_price = data["收盘"].max()
        low_price = data["收盘"].min()
        high_price_records = data.loc[data["收盘"] == high_price]
        low_price_records = data.loc[data["收盘"] == low_price]
        print(f"最高价格一共有 {len(high_price_records)} 条，最高价详细数据：\n{high_price_records}")
        print(f"最低价格一共有 {len(low_price_records)} 条，最低价详细数据：\n{low_price_records}")
        print(f"一共有 {records} 条数据，最高：{high_price}, 最低：{low_price}")

    def query_compare(self, compare_price: float, start_time="19700101", end_time="22220101", plot=False):
        s_date = datetime.datetime.strptime(str(start_time), '%Y%m%d').date()
        e_date = datetime.datetime.strptime(str(end_time), '%Y%m%d').date()
        all_data = self.data[self.data["日期"].isin(pd.date_range(s_date, e_date))]
        all_records = all_data.shape[0]
        compare_results_high = all_data[all_data["收盘"] > compare_price]
        compare_records = compare_results_high.shape[0]
        print(f"在查询时间范围内有 {all_records} 条数据，价格高于 {compare_price} 的有 {compare_records} 条记录，"
              f"历史上有 {(compare_records / all_records) * 100:0.2f}% 的时间高于 {compare_price}")
        if plot is True:
            ax = plt.subplot(1, 1, 1)
            plt.title(f"stock {self.stock_name}", color="k")
            plt.plot(all_data["日期"], all_data["收盘"], color="b")
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
            plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
            ax.text(0.8, 0.9, c="b", s="---历史走势", transform=ax.transAxes)
            ax.text(0.8, 0.8, c="r", s="---比较价格", transform=ax.transAxes)
            text = f"数据个数：{all_records}\n高于 {compare_price} 数据个数：{compare_records}"
            ax.text(0.05, 0.9, c="k", s=text, transform=ax.transAxes)
            plt.axhline(y=compare_price, c="r")
            plt.show()


class Download:
    def __init__(self, code: list = None, fold: str = None):
        self.__stock_code = code
        self.__save_fold = fold
        self.__pretreatment()
        ...

    def __check_save_fold(self):
        if not self.__save_fold:
            raise ErrorInfo("Download fold path must be given")

    def __check_stock_code(self):
        if isinstance(self.__stock_code, int):
            self.__stock_code = list[str(self.__stock_code)]
        elif isinstance(self.__stock_code, str):
            self.__stock_code = list[self.__stock_code]
        elif isinstance(self.__stock_code, tuple):
            self.__stock_code = list(self.__stock_code)
        elif isinstance(self.__stock_code, list):
            pass
        else:
            raise ErrorInfo("stock_code error!")

    def __pretreatment(self):
        if self.__stock_code:
            self.__check_stock_code()
        self.__check_save_fold()
        if not os.path.exists(self.__save_fold):
            os.mkdir(self.__save_fold)
        ...

    def reset_stock_code(self, value):
        self.__stock_code = value
        self.__check_stock_code()

    def download_basic_info(self):
        # 个股成分信息 个股信息查询
        # data = ak.index_stock_hist()
        # data = ak.stock_individual_info_em()

        data = ak.index_stock_info()
        filepath = os.path.join(self.__save_fold, "index_info.csv")
        data.to_csv(filepath)

    def download(self, time_range=("19700101", "22220101")):
        for stock in self.__stock_code:
            # 获取某个指数，例如 沪深300 指数的历史行情数据（新浪和东财）
            date = ak.stock_zh_index_daily(symbol=stock)
            data = ak.stock_zh_index_daily_em(symbol=stock)
            data = ak.stock_zh_index_daily_tx(symbol=stock)
            # 股票历史数据
            data = ak.stock_zh_a_hist(symbol=stock, start_date=time_range[0], end_date=time_range[1])
            data = ak.stock_zh_a_daily(symbol=stock, start_date=time_range[0], end_date=time_range[1])

            fullname = f"{stock}.csv"
            filepath = os.path.join(self.__save_fold, fullname)
            date.to_csv(filepath)
