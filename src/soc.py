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
ALL_SAVE_PATH = [STOCK_SAVE_PATH,
                 FUND_SAVE_PATH,
                 BOND_SAVE_PATH,
                 INDEX_SAVE_PATH,
                 ]
GLOBAL_SAVE_PATH = os.path.join(BASIC_PATH, "global")
IMAGE_SAVE_PATH = os.path.join(BASIC_PATH, "image")


class BaseType(Enum):
    # 如非必要，尽量不要使用枚举类型的值
    STOCK = (1, "股票")
    FUND = (2, "基金")
    BOND = (3, "债券")
    INDEX = (4, "指数")
    NULL = auto()


DownloadType = BaseType
AnalyzeType = BaseType
UpdateType = BaseType


class Download:
    """
    filename = code +  file_extension
    example:
        000002.csv
    
    给定证券类型能更准确的下载，不给定则全部下载,考虑到批量抓取的问题，下载应该要有一定延迟
    example a:
        inst = Download(code=["000002"],download_type=DownloadType.STOCK)
        # inst.run()
        inst.run_delay（3）
    example b:
        inst = Download(code=["000002"])
        # inst.run()
        inst.run_daley(3)
    """
    
    def __init__(self, code="000002", download_type: DownloadType = None,
                 time_range=("19700101", "22220101"), enable_error_print=False):
        self.download_type = download_type
        self.codes = self.__check_code(code)
        self.time_range = time_range
        self.__file_extension = ".csv"
        self.enable = enable_error_print
    
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
    
    def download(self):
        if self.download_type == DownloadType.STOCK:
            self.__create_dirs(STOCK_SAVE_PATH)
            self.__download_stock()
        elif self.download_type == DownloadType.FUND:
            self.__create_dirs(FUND_SAVE_PATH)
            self.__download_fund()
        elif self.download_type == DownloadType.BOND:
            self.__create_dirs(BOND_SAVE_PATH)
            self.__download_bond()
        elif self.download_type == DownloadType.INDEX:
            self.__create_dirs(INDEX_SAVE_PATH)
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
        if self.download_type:
            self.download()
        else:
            self.guess_download()


class Update:
    def __init__(self, code, update_type, update_filepath, start_time="20220101", end_time="22220101"):
        self.__code = code
        self.__update_type = update_type
        self.__update_filepath = update_filepath
        self.__update_start_time = start_time
        self.__update_end_time = end_time
    
    def normal_update(self):
        old_data = pd.read_csv(self.__update_filepath)
        Download(code=self.__code, download_type=self.__update_type,
                 time_range=(self.__update_start_time, self.__update_end_time)).run()
        new_data = pd.read_csv(self.__update_filepath)
        pd.concat([old_data, new_data]).to_csv(self.__update_filepath)
    
    def force_update(self):
        Download(code=self.__code, download_type=self.__update_type).run()


class Analyze:
    def __init__(self, code="000002", analyze_type=AnalyzeType.STOCK):
        if isinstance(code, int):
            code = str(code)
        self.__code = code
        self.__analyze_type = analyze_type
        self.__check_safe()
        self.__data = pd.DataFrame
        # 设置数据这部分稍显复杂，待优化
        self.__set_data()
    
    def __check_safe(self):
        current_support = [AnalyzeType.STOCK, AnalyzeType.FUND]
        if self.__analyze_type not in current_support:
            print(f"当前支持的分析类型为:{current_support}")
            raise "当前暂不支持该类型分析,请等待后续代码更新!"
    
    def manual_set_data(self, data: pd.DataFrame):
        self.__data = data
    
    def __set_data(self):
        current_date = datetime.datetime.now().date()
        yesterday_date = current_date + datetime.timedelta(days=-1)
        if AnalyzeType.STOCK == self.__analyze_type:
            filepath = os.path.join(STOCK_SAVE_PATH, f"{self.__code}.csv")
            # 文件不存在则下载，存在则更新
            if not os.path.exists(filepath):
                Download(code=self.__code, download_type=self.__analyze_type).run()
            else:
                old_data = pd.read_csv(filepath)
                old_data["日期"] = pd.to_datetime(old_data["日期"])
                old_max_date = old_data["日期"].max().date()
                if old_max_date not in [yesterday_date, current_date]:
                    s_time = str(old_max_date + datetime.timedelta(days=-1)).replace("-", "")
                    inst = Update(code=self.__code, update_type=self.__analyze_type,
                                  update_filepath=filepath, start_time=s_time)
                    inst.normal_update()
            self.__data = pd.read_csv(filepath)
            self.__data["日期"] = pd.to_datetime(self.__data["日期"])
        elif AnalyzeType.FUND == self.__analyze_type:
            filepath = os.path.join(FUND_SAVE_PATH, f"{self.__code}.csv")
            if not os.path.exists(filepath):
                Download(code=self.__code, download_type=self.__analyze_type).run()
            else:
                old_data = pd.read_csv(filepath)
                old_data["净值日期"] = pd.to_datetime(old_data["净值日期"])
                old_max_date = old_data["净值日期"].max().date()
                if old_max_date not in [yesterday_date, current_date]:
                    s_time = str(old_max_date + datetime.timedelta(days=-1)).replace("-", "")
                    inst = Update(code=self.__code, update_type=self.__analyze_type,
                                  update_filepath=filepath, start_time=s_time)
                    inst.normal_update()
            self.__data = pd.read_csv(filepath)
            self.__data["净值日期"] = pd.to_datetime(self.__data["净值日期"])
    
    def info(self):
        data = self.__data
        print(f"下面展示 {self.__code} 的详细数据:")
        records = data.shape[0]
        if self.__analyze_type == AnalyzeType.STOCK:
            high_price = data["收盘"].max()
            low_price = data["收盘"].min()
            high_price_records = data.loc[data["收盘"] == high_price]
            low_price_records = data.loc[data["收盘"] == low_price]
            latest_date = data["日期"].max()
            latest_records = data.loc[data["日期"] == latest_date]
        elif self.__analyze_type == AnalyzeType.FUND:
            high_price = data["单位净值"].max()
            low_price = data["单位净值"].min()
            high_price_records = data.loc[data["单位净值"] == high_price]
            low_price_records = data.loc[data["单位净值"] == low_price]
            latest_date = data["净值日期"].max()
            latest_records = data.loc[data["净值日期"] == latest_date]
        print(f"最高价格一共有{len(high_price_records)}条，最高价详细数据:\n{high_price_records}")
        print(f"最低价格一共有{len(low_price_records)}条，最低价详细数据:\n{low_price_records}")
        print(f"最新的一条数据是:\n{latest_records}")
        print(f"一共有{records}条数据，最高：{high_price}, 最低：{low_price}")
    
    def query(self, compare_price: float, plot=False, start_time="19700101", end_time="22220101"):
        s_date = datetime.datetime.strptime(str(start_time), '%Y%m%d').date()
        e_date = datetime.datetime.strptime(str(end_time), '%Y%m%d').date()
        if self.__analyze_type == AnalyzeType.STOCK:
            all_data = self.__data[self.__data["日期"].isin(pd.date_range(s_date, e_date))]
            compare_results_high = all_data[all_data["收盘"] > compare_price]
        elif self.__analyze_type == AnalyzeType.FUND:
            all_data = self.__data[self.__data["净值日期"].isin(pd.date_range(s_date, e_date))]
            compare_results_high = all_data[all_data["单位净值"] > compare_price]
        all_records = all_data.shape[0]
        compare_records = compare_results_high.shape[0]
        print(f"({s_date},{e_date})有{all_records}条数据,高于{compare_price}的有{compare_records}条记录")
        print(f"历史上有{(compare_records / all_records) * 100:0.2f}%的时间高于{compare_price}")
        if plot is True:
            ax = plt.subplot(1, 1, 1)
            # plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
            # plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
            plt.title(f"{self.__code}", color="k")
            if self.__analyze_type == AnalyzeType.STOCK:
                plt.plot(all_data["日期"], all_data["收盘"], color="b")
            elif self.__analyze_type == AnalyzeType.FUND:
                plt.plot(all_data["净值日期"], all_data["单位净值"], color="b")
            ax.text(0.7, 0.9, c="b", s="---Historical trends", transform=ax.transAxes)
            ax.text(0.7, 0.8, c="r", s="---Compare prices", transform=ax.transAxes)
            text = f"Records:{all_records}\n{compare_records}>{compare_price}"
            ax.text(0.05, 0.9, c="k", s=text, transform=ax.transAxes)
            plt.axhline(y=compare_price, c="r")
            image_name = f"{self.__analyze_type.value[1]}_{self.__code}.jpg"
            image_path = os.path.join(IMAGE_SAVE_PATH, image_name)
            if not os.path.exists(IMAGE_SAVE_PATH):
                os.mkdir(IMAGE_SAVE_PATH)
            plt.savefig(image_path)
            plt.show()
            plt.close()
