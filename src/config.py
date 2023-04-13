# 文件存储路径
import os
import time
from os.path import join

basedir = os.path.dirname(__file__)
save_path_stock = join(basedir, "stock")
save_path_fund = join(basedir, "fund")
save_path_index = join(basedir, "index")
save_path_bond = join(basedir, "bond")
save_path_global = join(basedir, "global")
save_path_image = join(basedir, "image")

# 当前时间
current_day = time.strftime("%Y%m%d", time.localtime())
current_hour = time.localtime().tm_hour
current_min = time.localtime().tm_min

json_source_path = join(basedir, "code")
json_filename = "code.json"
