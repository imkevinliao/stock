# -*- coding:utf-8 -*-
import datetime
import os
import re

import akshare as ak
import pandas as pd
from matplotlib import pyplot as plt

BASIC_PATH = os.path.dirname(__file__)
STOCKS_SAVE_FOLD = "stock"
GLOBAL_SAVE_FOLD = "global"
STOCKS_SAVE_PATH = os.path.join(BASIC_PATH, STOCKS_SAVE_FOLD)
GLOBAL_SAVE_PATH = os.path.join(BASIC_PATH, GLOBAL_SAVE_FOLD)


def global_download():
    fold_path = GLOBAL_SAVE_FOLD
    if not os.path.exists(fold_path):
        os.mkdir(fold_path)
    # 股票指数-成份股-所有可以获取的指数表
    data = ak.index_stock_info()
    filepath = os.path.join(fold_path, "stock_index_info.csv")
    data.to_csv(filepath)
    # A 股股票代码和简称
    data = ak.stock_info_a_code_name()
    filepath = os.path.join(fold_path, "stock_a_code.csv")
    data.to_csv(filepath)
    # 公募基金-基本信息
    data = ak.fund_name_em()
    filepath = os.path.join(fold_path, "fund_name.csv")
    data.to_csv(filepath)
    # 指数型基金-基本信息
    data = ak.fund_info_index_em()
    filepath = os.path.join(fold_path, "fund_info_index.csv")
    data.to_csv(filepath)


def __check_code(code):
    new_code = []
    if isinstance(code, int):
        new_code.append(str(code))
    elif isinstance(code, str):
        new_code.append(code)
    elif isinstance(code, tuple):
        new_code = list(code)
    elif isinstance(code, list):
        new_code = code
    else:
        raise Exception("Input Code Type Error!")
    return new_code


def __try_download(code, time_range):
    data = None
    ok = 1
    default = 0
    status = default
    # 股票-历史数据
    try:
        if status != ok:
            data = ak.stock_zh_a_hist(symbol=code, start_date=time_range[0], end_date=time_range[1])
            status = ok
    except Exception as e:
        pass
    try:
        if status != ok:
            data = ak.stock_zh_a_daily(symbol=code, start_date=time_range[0], end_date=time_range[1])
            status = ok
    except Exception as e:
        pass
    if status == ok:
        return data
    # 基金-etf 历史数据
    try:
        if status != ok:
            data = ak.fund_etf_fund_info_em(fund=code, start_date=time_range[0], end_date=time_range[1])
            status = ok
    except Exception as e:
        pass
    if status == ok:
        return data
    # 债券-沪深债券 历史数据
    try:
        if status != ok:
            data = ak.bond_zh_hs_daily(symbol=code)
            status = ok
    except Exception as e:
        pass
    if status == ok:
        return data
        # 指数历史数据
    try:
        if status != ok:
            date = ak.stock_zh_index_daily(symbol=code)
            status = ok
    except Exception as e:
        pass
    try:
        if status != ok:
            data = ak.stock_zh_index_daily_em(symbol=code)
            status = ok
    except Exception as e:
        pass
    try:
        if status != ok:
            data = ak.stock_zh_index_daily_tx(symbol=code)
            status = ok
    except Exception as e:
        pass
    if status == ok:
        return data
    return data


def stock_download(code: list = None, time_range=("19700101", "22220101")):
    fold_path = STOCKS_SAVE_PATH
    if not os.path.exists(fold_path):
        os.mkdir(fold_path)
    codes = __check_code(code)
    for code in codes:
        data = __try_download(code=code, time_range=time_range)
        if data is not None:
            fullname = f"{code}.csv"
            filepath = os.path.join(fold_path, fullname)
            data.to_csv(filepath)
            print(f"{code} data save to {fold_path}.")
        else:
            print(f"Error:{code} data download failed.")


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
