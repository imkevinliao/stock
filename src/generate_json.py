import json
import os.path

import akshare as ak
import pandas as pd
from easydict import EasyDict

from config import *


def get_index() -> dict:
    filepath = join(save_path_global, f"股票指数数据_{current_day}.csv")
    if not os.path.exists(filepath):
        if not os.path.exists(save_path_global):
            os.mkdir(save_path_global)
        stock_zh_index_spot_df = ak.stock_zh_index_spot()
        stock_zh_index_spot_df.to_csv(filepath)
    
    index_dict = dict()
    data = pd.read_csv(filepath)
    for index, row in data.iterrows():
        key = row["代码"]
        value = row["名称"]
        index_dict[f"{key}"] = str(value)
    return index_dict


def gen_json(code_dict: dict):
    with open(json_filename, "w", encoding="utf-8") as f:
        json_str = json.dumps(code_dict, indent=4, ensure_ascii=False)
        f.write(json_str)


if __name__ == '__main__':
    code = EasyDict()
    code.index = get_index()
    gen_json(code)
