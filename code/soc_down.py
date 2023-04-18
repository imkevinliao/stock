import random

import akshare as ak
import pandas as pd

from common import *

os.environ['no_proxy'] = '*'


def get_flow_name():
    filepath = join(save_path_data, "板块资金流排名.csv")
    if not os.path.exists(filepath):
        data = ak.stock_sector_fund_flow_rank()
        data.to_csv(filepath)
    data = pd.read_csv(filepath)
    flow_name = []
    for index, row in data.iterrows():
        flow_name.append(str(row["名称"]))
    if flow_name is None:
        raise "error, get flow name failed."
    return flow_name


def get_industry_flow(industry_name):
    new_fold = join(save_path_data, f"行业历史资金流_{current_day}")
    if not os.path.exists(new_fold):
        os.makedirs(new_fold)
    filepath = join(new_fold, f"{industry_name}.csv")
    print(f"start download {filepath}.")
    data = ak.stock_sector_fund_flow_hist(symbol=industry_name)
    data.to_csv(filepath)
    download_delay = random.randint(1, 10)
    print(f"{filepath} download succeed. time delay {download_delay} seconds.")
    time.sleep(download_delay)


def get_all_industry_flow():
    names = get_flow_name()
    for name in names:
        get_industry_flow(industry_name=name)
    print(f"get_all_industry_flow ok.")


if __name__ == '__main__':
    get_all_industry_flow()
    ...
