import datetime
import json
import os.path
from enum import Enum

import akshare as ak
import pandas as pd
from matplotlib import pyplot as plt, dates
from common import *


class CodeType(Enum):
    STOCK = (1, "股票")
    FUND = (2, "基金")
    INDEX = (3, "指数")
    BOND = (4, "债券")


def global_download():
    if not os.path.exists(save_global):
        os.makedirs(save_global)
    # 股票指数-成份股-所有可以获取的指数表
    data = ak.index_stock_info()
    filepath = os.path.join(save_global, "股票指数表.csv")
    data.to_csv(filepath)
    # A 股股票代码和简称
    data = ak.stock_info_a_code_name()
    filepath = os.path.join(save_global, "stock_info_a_code_name.csv")
    data.to_csv(filepath)
    # 公募基金-基本信息
    data = ak.fund_name_em()
    filepath = os.path.join(save_global, "公募基金表.csv")
    data.to_csv(filepath)
    # 指数型基金-基本信息
    data = ak.fund_info_index_em()
    filepath = os.path.join(save_global, "fund_info_index_em.csv")
    data.to_csv(filepath)


class DownloadCode:
    """
    code = "000002"
    codetype = CodeType.STOCK
    """
    
    def __init__(self, code, codetype):
        self.code = code
        self.codetype = codetype
        self.time_range = ("19700101", "22220101")
    
    def set_time_range(self, value=("19700101", "22220101")):
        self.time_range = value
    
    def get_filepath(self):
        filename = f"{self.code}.csv"
        if self.codetype == CodeType.STOCK:
            filepath = join(save_stock, filename)
        elif self.codetype == CodeType.FUND:
            filepath = join(save_fund, filename)
        elif self.codetype == CodeType.INDEX:
            filepath = join(save_index, filename)
        elif self.codetype == CodeType.BOND:
            filepath = join(save_bond, filename)
        else:
            raise "codetype error."
        return filepath
    
    def __get_data(self):
        code = self.code
        if self.codetype == CodeType.STOCK:
            data = ak.stock_zh_a_hist(symbol=code, start_date=self.time_range[0], end_date=self.time_range[1])
            # data = ak.stock_zh_a_daily(symbol=code, start_date=self.time_range[0], end_date=self.time_range[1])
        elif self.codetype == CodeType.FUND:
            data = ak.fund_etf_fund_info_em(fund=code, start_date=self.time_range[0], end_date=self.time_range[1])
        elif self.codetype == CodeType.INDEX:
            data = ak.stock_zh_index_daily(symbol=code)
            # data = ak.stock_zh_index_daily_em(symbol=code)
            # data = ak.stock_zh_index_daily_tx(symbol=code)
        elif self.codetype == CodeType.BOND:
            data = ak.bond_zh_hs_daily(symbol=code)
        else:
            raise "codetype error."
        if data is None:
            raise "get data error."
        return data
    
    @staticmethod
    def save(data: pd.DataFrame, filepath):
        target_dir = os.path.dirname(filepath)
        if not os.path.exists(target_dir):
            print(f"target_dir will be create:{target_dir}")
            os.makedirs(target_dir)
        data.to_csv(filepath)
    
    def download(self, delay=0):
        if delay > 0:
            time.sleep(delay)
        data = self.__get_data()
        self.save(data, self.get_filepath())


class UpdateCode(DownloadCode):
    def __init__(self, code, codetype):
        super().__init__(code, codetype)
        self.update_flag = False
    
    def force_update(self):
        self.update_flag = True
    
    def update_state(self):
        """文件最后修改时间和当前时间不一致则更新"""
        if self.update_flag:
            return True
        filepath = super().get_filepath()
        filetime = time.localtime(os.path.getmtime(filepath))
        file_day = time.strftime("%Y%m%d", filetime)
        if current_day != file_day:
            print(f"today is {current_day}, file day is {file_day}")
            self.update_flag = True
        else:
            self.update_flag = False
    
    def update(self):
        self.update_state()
        if self.update_flag:
            print(f"update {self.code} file")
            super().download()


class MyJson:
    def __init__(self, code: str, codetype: CodeType):
        self.code = code
        self.codetype = codetype
        self.filepath = json_filepath
    
    def get_content(self) -> dict:
        with open(self.filepath, "r", encoding="utf-8") as f:
            content = json.loads(f.read())
        return content
    
    def get_index_code(self):
        symbol_code = self.code
        if self.codetype != CodeType.INDEX:
            return symbol_code
        content = self.get_content()["index"]
        for key, value in content.items():
            if self.code in key:
                symbol_code = key
                break
        return symbol_code
    
    def get_name(self):
        content = self.get_content()
        stock = content["stock"]
        fund = content["fund"]
        index = content["index"]
        name = ""
        if self.codetype == CodeType.STOCK:
            for key, value in stock.items():
                if self.code in key:
                    name = value
        elif self.codetype == CodeType.FUND:
            for key, value in fund.items():
                if self.code in key:
                    name = value
        elif self.codetype == CodeType.INDEX:
            for key, value in index.items():
                if self.code in key:
                    name = value
        if name:
            return name
        else:
            return None


class Analyze(UpdateCode):
    def __init__(self, code: str, codetype: CodeType):
        super().__init__(code, codetype)
        if self.codetype == CodeType.INDEX:
            self.code = MyJson(code, codetype).get_index_code()
        else:
            self.code = code
        self.codetype = codetype
        self.data = pd.DataFrame
        self.time = ("19700101", "22220101")
        self.support_type = [CodeType.STOCK, CodeType.FUND, CodeType.INDEX]
        self.__prepare_data()
    
    def get_name(self):
        if not os.path.exists(json_filepath):
            return None
        inst = MyJson(code=self.code, codetype=self.codetype)
        name = inst.get_name()
        return name
    
    def get_raw_data(self) -> pd.DataFrame:
        filepath = super().get_filepath()
        if not os.path.exists(filepath):
            super().download()
        else:
            super().update()
        data = pd.read_csv(filepath)
        return data
    
    def __prepare_data(self):
        data = self.get_raw_data()
        if self.codetype == CodeType.STOCK:
            data["日期"] = pd.to_datetime(data["日期"])
        elif self.codetype == CodeType.FUND:
            data["净值日期"] = pd.to_datetime(data["净值日期"])
        elif self.codetype == CodeType.INDEX:
            data["date"] = pd.to_datetime(data["date"])
        else:
            raise f"support codetype is {self.support_type}"
        self.data = data
    
    def basic_info(self):
        data = self.data
        records = data.shape[0]
        if self.codetype == CodeType.STOCK:
            h_records = data.loc[data["收盘"] == data["收盘"].max()]
            l_records = data.loc[data["收盘"] == data["收盘"].min()]
            latest_record = data.loc[data["日期"] == data["日期"].max()]
        elif self.codetype == CodeType.FUND:
            h_records = data.loc[data["单位净值"] == data["单位净值"].max()]
            l_records = data.loc[data["单位净值"] == data["单位净值"].min()]
            latest_record = data.loc[data["净值日期"] == data["净值日期"].max()]
        elif self.codetype == CodeType.INDEX:
            h_records = data.loc[data["close"] == data["close"].max()]
            l_records = data.loc[data["close"] == data["close"].min()]
            latest_record = data.loc[data["date"] == data["date"].max()]
        else:
            raise f"support codetype is {self.support_type}"
        print(f"{self.code} records:{records}")
        print(f"high_record:\n{h_records}\nlow_record:\n{l_records}\nlatest_record:\n{latest_record}\n")
    
    def query(self, compare_price=None, start_time=None, end_time=None):
        """
        compare_price：如果不指定则默认当前价格作为比较价格
        """
        start_time = self.time[0] if not start_time else start_time
        end_time = self.time[1] if not end_time else end_time
        s_date = datetime.datetime.strptime(str(start_time), '%Y%m%d').date()
        e_date = datetime.datetime.strptime(str(end_time), '%Y%m%d').date()
        if self.codetype == CodeType.STOCK:
            all_data = self.data[self.data["日期"].isin(pd.date_range(s_date, e_date))]
            price = all_data.loc[all_data.loc[:, "收盘"].index.tolist()[-1]]["收盘"]
            compare_price = price if not compare_price else compare_price
            up_compare_price = all_data[all_data["收盘"] > compare_price]
        elif self.codetype == CodeType.FUND:
            all_data = self.data[self.data["净值日期"].isin(pd.date_range(s_date, e_date))]
            price = all_data.loc[all_data.loc[:, "单位净值"].index.tolist()[-1]]["单位净值"]
            compare_price = price if not compare_price else compare_price
            up_compare_price = all_data[all_data["单位净值"] > compare_price]
        elif self.codetype == CodeType.INDEX:
            all_data = self.data[self.data["date"].isin(pd.date_range(s_date, e_date))]
            price = all_data.loc[all_data.loc[:, "close"].index.tolist()[-1]]["close"]
            compare_price = price if not compare_price else compare_price
            up_compare_price = all_data[all_data["close"] > compare_price]
        else:
            raise f"support codetype is {self.support_type}"
        all_records = all_data.shape[0]
        up_compare_price_records = up_compare_price.shape[0]
        print(f"during:({s_date},{e_date}) has records {all_records}.")
        print(f"price > {compare_price} has records:{up_compare_price_records}")
    
    def plot(self, data_counts=30):
        data = self.data
        user_data = data.tail(data_counts)
        if data_counts <= 7:
            formatter = dates.DateFormatter("%d")
            user_interval = dates.DayLocator(interval=1)
        elif data_counts <= 30:
            formatter = dates.DateFormatter("%d")
            user_interval = dates.DayLocator(interval=7)
        elif data_counts <= 180:
            formatter = dates.DateFormatter("%m")
            user_interval = dates.MonthLocator(interval=1)
        elif data_counts <= 365:
            formatter = dates.DateFormatter("%m")
            user_interval = dates.MonthLocator(interval=3)
        else:
            formatter = dates.DateFormatter("%Y")
            user_interval = dates.YearLocator()
        fig = plt.figure()
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
        plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
        name = self.get_name()
        if name:
            title_text = f"{name}({self.code})"
        else:
            title_text = f"{self.code}"
        
        def get_time_info(time_start, time_end):
            s = time_start.strftime("%Y/%m/%d")
            e = time_end.strftime("%Y/%m/%d")
            return f"{s} - {e}"
        
        if self.codetype == CodeType.STOCK:
            ax = plt.subplot(212)
            ax.text(0.02, 0.9, c="b", s=get_time_info(data["日期"].iloc[0], data["日期"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(data["日期"], data["收盘"], color="b")
            ax = plt.subplot(211)
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_major_locator(user_interval)
            ax.text(0.04, 0.9, c="b", s=get_time_info(user_data["日期"].iloc[0], user_data["日期"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(user_data["日期"], user_data["收盘"], color="r")
        elif self.codetype == CodeType.FUND:
            ax = plt.subplot(212)
            ax.text(0.02, 0.9, c="b", s=get_time_info(data["净值日期"].iloc[0], data["净值日期"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(data["净值日期"], data["单位净值"], color="b")
            ax = plt.subplot(211)
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_major_locator(user_interval)
            ax.text(0.04, 0.9, c="b", s=get_time_info(user_data["净值日期"].iloc[0], user_data["净值日期"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(user_data["净值日期"], user_data["单位净值"], color="r")
        elif self.codetype == CodeType.INDEX:
            ax = plt.subplot(212)
            ax.text(0.02, 0.9, c="b", s=get_time_info(data["date"].iloc[0], data["date"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(data["date"], data["close"], color="b")
            ax = plt.subplot(211)
            ax.xaxis.set_major_formatter(formatter)
            ax.xaxis.set_major_locator(user_interval)
            ax.text(0.04, 0.9, c="b", s=get_time_info(user_data["date"].iloc[0], user_data["date"].iloc[-1]),
                    transform=ax.transAxes)
            plt.title(title_text, color="k")
            plt.plot(user_data["date"], user_data["close"], color="r")
        else:
            raise f"support codetype is {self.support_type}"
        if name:
            image_name = f"{self.code}__{name}.jpg"
        else:
            image_name = f"{self.code}__{self.codetype.value[1]}.jpg"
        image_path = os.path.join(save_path_image, image_name)
        if not os.path.exists(save_path_image):
            os.makedirs(save_path_image)
        plt.savefig(image_path)
        plt.show()
