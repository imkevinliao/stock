import datetime
import os
import time
from enum import Enum, auto

import akshare as ak
import pandas as pd
from matplotlib import pyplot as plt

BASIC_PATH = os.path.dirname(__file__)
HERE = BASIC_PATH

STOCK_SAVE_PATH = os.path.join(BASIC_PATH, "stock")
FUND_SAVE_PATH = os.path.join(BASIC_PATH, "fund")
BOND_SAVE_PATH = os.path.join(BASIC_PATH, "bond")
INDEX_SAVE_PATH = os.path.join(BASIC_PATH, "index")
GLOBAL_SAVE_PATH = os.path.join(BASIC_PATH, "global")
ALL_SAVE_PATH = [STOCK_SAVE_PATH,
                 FUND_SAVE_PATH,
                 BOND_SAVE_PATH,
                 INDEX_SAVE_PATH,
                 ]


class DownloadType(Enum):
    NULL = auto()
    STOCK = auto()  # 股票
    FUND = auto()  # 基金
    BOND = auto()  # 债券
    INDEX = auto()  # 指数


class Download:
    """
    filename = code +  file_extension
    example:
        000002.csv
    
    给定证券类型能更准确的下载，不给定则全部下载,考虑到批量抓取的问题，下载应该要有一定延迟
    example a:
        inst = Download(code=["000002"],securities_type=Securities.STOCK)
        # inst.run()
        inst.run_delay（3）
    example b:
        inst = Download(code=["000002"])
        # inst.run()
        inst.run_daley(3)
    """
    
    def __init__(self, code="000002", securities_type: DownloadType = None,
                 time_range=("19700101", "22220101"), enable_error_print=False):
        self.securities_type = securities_type
        self.codes = self.__check_code(code)
        self.time_range = time_range
        self.__file_extension = ".csv"
        self.enable = enable_error_print
        self.__create_download_dir()
    
    @staticmethod
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
    
    def __download_stock(self):
        for code in self.codes:
            data = None
            status = False
            try:
                if not status:
                    data = ak.stock_zh_a_hist(symbol=code, start_date=self.time_range[0], end_date=self.time_range[1])
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            try:
                if not status:
                    data = ak.stock_zh_a_daily(symbol=code, start_date=self.time_range[0], end_date=self.time_range[1])
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            if status:
                filepath = os.path.join(STOCK_SAVE_PATH, str(code) + self.__file_extension)
                data.to_csv(filepath)
                print(f"stock {code} downloaded successfully.")
            else:
                if self.enable:
                    print(f"error: stock {code} download failed.")
    
    def __download_fund(self):
        for code in self.codes:
            data = None
            status = False
            try:
                if not status:
                    data = ak.fund_etf_fund_info_em(fund=code, start_date=self.time_range[0],
                                                    end_date=self.time_range[1])
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            if status:
                filepath = os.path.join(FUND_SAVE_PATH, str(code) + self.__file_extension)
                data.to_csv(filepath)
                print(f"fund {code} downloaded successfully.")
            else:
                if self.enable:
                    print(f"error: fund {code} download failed.")
    
    def __download_bond(self):
        for code in self.codes:
            data = None
            status = False
            try:
                if not status:
                    data = ak.bond_zh_hs_daily(symbol=code)
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            if status:
                filepath = os.path.join(BOND_SAVE_PATH, str(code) + self.__file_extension)
                data.to_csv(filepath)
                print(f"bond {code} downloaded successfully.")
            else:
                if self.enable:
                    print(f"error: bond {code} download failed.")
    
    def __download_index(self):
        for code in self.codes:
            data = None
            status = False
            try:
                if not status:
                    data = ak.stock_zh_index_daily(symbol=code)
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            try:
                if not status:
                    data = ak.stock_zh_index_daily_em(symbol=code)
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            try:
                if not status:
                    data = ak.stock_zh_index_daily_tx(symbol=code)
                    status = True
            except Exception as e:
                if self.enable:
                    print(e)
            if status:
                filepath = os.path.join(INDEX_SAVE_PATH, str(code) + self.__file_extension)
                data.to_csv(filepath)
                print(f"index {code} downloaded successfully.")
            else:
                if self.enable:
                    print(f"error: index {code} download failed.")
    
    @staticmethod
    def global_download():
        # 股票指数-成份股-所有可以获取的指数表
        data = ak.index_stock_info()
        filepath = os.path.join(GLOBAL_SAVE_PATH, "stock_index_info.csv")
        data.to_csv(filepath)
        # A 股股票代码和简称
        data = ak.stock_info_a_code_name()
        filepath = os.path.join(GLOBAL_SAVE_PATH, "stock_a_code.csv")
        data.to_csv(filepath)
        # 公募基金-基本信息
        data = ak.fund_name_em()
        filepath = os.path.join(GLOBAL_SAVE_PATH, "fund_name.csv")
        data.to_csv(filepath)
        # 指数型基金-基本信息
        data = ak.fund_info_index_em()
        filepath = os.path.join(GLOBAL_SAVE_PATH, "fund_info_index.csv")
        data.to_csv(filepath)
    
    @staticmethod
    def __create_dirs(paths):
        if isinstance(paths, list):
            for path in paths:
                if not os.path.exists(path):
                    os.mkdir(path)
        elif isinstance(paths, str):
            path = paths
            if not os.path.exists(path):
                os.mkdir(path)
    
    def __create_download_dir(self):
        if self.securities_type == DownloadType.STOCK:
            self.__create_dirs(STOCK_SAVE_PATH)
        elif self.securities_type == DownloadType.FUND:
            self.__create_dirs(FUND_SAVE_PATH)
        elif self.securities_type == DownloadType.BOND:
            self.__create_dirs(BOND_SAVE_PATH)
        elif self.securities_type == DownloadType.INDEX:
            self.__create_dirs(INDEX_SAVE_PATH)
        else:
            pass
    
    def download(self):
        if self.securities_type == DownloadType.STOCK:
            self.__download_stock()
        elif self.securities_type == DownloadType.FUND:
            self.__download_fund()
        elif self.securities_type == DownloadType.BOND:
            self.__download_bond()
        elif self.securities_type == DownloadType.INDEX:
            self.__download_index()
        else:
            print(f"securities_type doesn't exist. download nothing.")
    
    def guess_download(self):
        """
        只给定了代码，但是没给定证券类型，全部类型都尝试下一遍
        """
        self.__create_dirs(ALL_SAVE_PATH)
        self.__download_stock()
        self.__download_fund()
        self.__download_bond()
        self.__download_index()
    
    def run_delay(self, delay=3):
        codes = self.codes
        for code in codes:
            self.codes = self.__check_code(code)
            self.run()
            time.sleep(delay)
    
    def run(self):
        if self.securities_type:
            self.download()
        else:
            self.guess_download()


class AnalyzeStock:
    def __init__(self, code="000002"):
        self.__code = code
        self.__file_extension = ".csv"
        self.__filepath = os.path.join(STOCK_SAVE_PATH, f"{code}{self.__file_extension}")
        self.__check_filepath()
        self.__data = pd.read_csv(self.__filepath)
        self.__data_initialize()
    
    def __check_filepath(self):
        if not os.path.exists(self.__filepath):
            Download(code=self.__code, securities_type=DownloadType.STOCK).run()
            if not os.path.exists(self.__filepath):
                raise Exception(f"download stock {self.__code} error!")
    
    def __data_initialize(self):
        self.__data["日期"] = pd.to_datetime(self.__data["日期"])
    
    def info(self):
        data = self.__data
        print(f"下面展示文件 {self.__filepath} 的详细数据：{self.__code}")
        records = data.shape[0]
        high_price = data["收盘"].max()
        low_price = data["收盘"].min()
        high_price_records = data.loc[data["收盘"] == high_price]
        low_price_records = data.loc[data["收盘"] == low_price]
        print(f"最高价格一共有 {len(high_price_records)} 条，最高价详细数据：\n{high_price_records}")
        print(f"最低价格一共有 {len(low_price_records)} 条，最低价详细数据：\n{low_price_records}")
        print(f"一共有 {records} 条数据，最高：{high_price}, 最低：{low_price}")
    
    def query(self, compare_price: float, plot=False, start_time="19700101", end_time="22220101"):
        s_date = datetime.datetime.strptime(str(start_time), '%Y%m%d').date()
        e_date = datetime.datetime.strptime(str(end_time), '%Y%m%d').date()
        all_data = self.__data[self.__data["日期"].isin(pd.date_range(s_date, e_date))]
        all_records = all_data.shape[0]
        compare_results_high = all_data[all_data["收盘"] > compare_price]
        compare_records = compare_results_high.shape[0]
        print(f"在查询时间范围内有 {all_records} 条数据，价格高于 {compare_price} 的有 {compare_records} 条记录，"
              f"历史上有 {(compare_records / all_records) * 100:0.2f}% 的时间高于 {compare_price}")
        if plot is True:
            ax = plt.subplot(1, 1, 1)
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
            plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
            plt.title(f"stock {self.__code}", color="k")
            plt.plot(all_data["日期"], all_data["收盘"], color="b")
            ax.text(0.8, 0.9, c="b", s="---历史走势", transform=ax.transAxes)
            ax.text(0.8, 0.8, c="r", s="---比较价格", transform=ax.transAxes)
            text = f"数据个数：{all_records}\n高于 {compare_price} 数据个数：{compare_records}"
            ax.text(0.05, 0.9, c="k", s=text, transform=ax.transAxes)
            plt.axhline(y=compare_price, c="r")
            plt.show()


class AnalyzeFund:
    def __init__(self, code="510310"):
        self.__code = code
        self.__file_extension = ".csv"
        self.__filepath = os.path.join(FUND_SAVE_PATH, f"{code}{self.__file_extension}")
        self.__check_filepath()
        self.__data = pd.read_csv(self.__filepath)
        self.__data_initialize()
    
    def __data_initialize(self):
        self.__data["净值日期"] = pd.to_datetime(self.__data["净值日期"])
    
    def __check_filepath(self):
        if not os.path.exists(self.__filepath):
            Download(code=self.__code, securities_type=DownloadType.FUND).run()
            if not os.path.exists(self.__filepath):
                raise Exception(f"download stock {self.__code} error!")
    
    def info(self):
        data = self.__data
        print(f"下面展示文件 {self.__filepath} 的详细数据：{self.__code}")
        records = data.shape[0]
        high_price = data["单位净值"].max()
        low_price = data["单位净值"].min()
        high_price_records = data.loc[data["单位净值"] == high_price]
        low_price_records = data.loc[data["单位净值"] == low_price]
        print(f"最高价格一共有 {len(high_price_records)} 条，最高价详细数据：\n{high_price_records}")
        print(f"最低价格一共有 {len(low_price_records)} 条，最低价详细数据：\n{low_price_records}")
        print(f"一共有 {records} 条数据，最高：{high_price}, 最低：{low_price}")
    
    def query(self, compare_price: float, plot=False, start_time="19700101", end_time="22220101"):
        s_date = datetime.datetime.strptime(str(start_time), '%Y%m%d').date()
        e_date = datetime.datetime.strptime(str(end_time), '%Y%m%d').date()
        all_data = self.__data[self.__data["净值日期"].isin(pd.date_range(s_date, e_date))]
        all_records = all_data.shape[0]
        compare_results_high = all_data[all_data["单位净值"] > compare_price]
        compare_records = compare_results_high.shape[0]
        print(f"在查询时间范围内有 {all_records} 条数据，价格高于 {compare_price} 的有 {compare_records} 条记录，"
              f"历史上有 {(compare_records / all_records) * 100:0.2f}% 的时间高于 {compare_price}")
        if plot is True:
            ax = plt.subplot(1, 1, 1)
            plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
            plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
            plt.title(f"stock {self.__code}", color="k")
            plt.plot(all_data["净值日期"], all_data["单位净值"], color="b")
            ax.text(0.8, 0.9, c="b", s="---历史走势", transform=ax.transAxes)
            ax.text(0.8, 0.8, c="r", s="---比较价格", transform=ax.transAxes)
            text = f"数据个数：{all_records}\n高于 {compare_price} 数据个数：{compare_records}"
            ax.text(0.05, 0.9, c="k", s=text, transform=ax.transAxes)
            plt.axhline(y=compare_price, c="r")
            plt.show()
