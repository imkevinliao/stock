import os.path
import shutil

import os
import time
from os.path import join

current_day = time.strftime("%Y%m%d", time.localtime())
current_hour = time.localtime().tm_hour
current_min = time.localtime().tm_min

current = os.path.dirname(__file__)
root_dir = os.path.dirname(current)
save_path_data = os.path.join(root_dir, "data")
save_path_image = join(root_dir, "image")
save_path_json = join(root_dir, "json")

save_stock = join(save_path_data, "stock")
save_fund = join(save_path_data, "fund")
save_index = join(save_path_data, "index")
save_bond = join(save_path_data, "bond")
save_global = join(save_path_data, "global")

json_filepath = os.path.join(save_path_json, "code_config.json")


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_dir(path):
    if os.path.exists(path):
        os.remove(path)


def delete_dirs(path):
    if os.path.exists(path):
        shutil.rmtree(path)
