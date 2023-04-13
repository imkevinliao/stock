import json
import os.path
import shutil

import akshare as ak
import pandas as pd
from easydict import EasyDict

from config import *

index_path = join(json_source_path, f"证券指数表.csv")
fund_path = join(json_source_path, f"公募基金表.csv")
stock_path = join(json_source_path, f"A股股票表.csv")


def get_fund() -> dict:
    if not os.path.exists(fund_path):
        fund_name_em = ak.fund_name_em()
        fund_name_em.to_csv(fund_path)
    fund_dict = dict()
    data = pd.read_csv(fund_path)
    for index, row in data.iterrows():
        key = str(row["基金代码"]).zfill(6)
        value = str(row["基金简称"])
        fund_dict[f"{key}"] = str(value)
    return fund_dict


def get_index() -> dict:
    if not os.path.exists(index_path):
        stock_zh_index_spot_df = ak.stock_zh_index_spot()
        stock_zh_index_spot_df.to_csv(index_path)
    
    index_dict = dict()
    data = pd.read_csv(index_path)
    for index, row in data.iterrows():
        key = str(row["代码"])
        value = str(row["名称"])
        index_dict[f"{key}"] = str(value)
    return index_dict


def get_stock() -> dict:
    if not os.path.exists(stock_path):
        stock_info_a_code_name = ak.stock_info_a_code_name()
        stock_info_a_code_name.to_csv(stock_path)
    
    stock_dict = dict()
    data = pd.read_csv(stock_path)
    for index, row in data.iterrows():
        key = str(row["code"]).zfill(6)
        value = str(row["name"])
        stock_dict[f"{key}"] = str(value)
    return stock_dict


def gen_json(code_dict: dict):
    with open(json_filename, "w", encoding="utf-8") as f:
        json_str = json.dumps(code_dict, indent=4, ensure_ascii=False)
        f.write(json_str)


def core():
    if not os.path.exists(json_source_path):
        os.mkdir(json_source_path)
    code = EasyDict()
    code.index = get_index()
    code.fund = get_fund()
    code.stock = get_stock()
    gen_json(code)


# 重新下载资源文件用于生成json
def regenerate():
    shutil.rmtree(json_source_path)
    core()


if __name__ == '__main__':
    core()
