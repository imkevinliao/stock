# akshare
必须要指出 akshare 获取数据应该本着互联网爬虫原则，不给网站服务器带来压力，适量请求。稍微大点的网站基本都会做防护，阻止恶意用户请求，以保障网站正常运行服务其他用户。如果使用过程中报错很大概率会是网站对使用者ip进行了封禁，所以请适度请求。

（实时行情数据极其容易被封IP，非常不建议频繁使用） 个人感觉新浪的接口极其容易被封，东财的接口似乎对于 akshare 更宽容一些

通常 api 中带有 spot 的都需要小心使用，这种一般都是整个股市的数据，量比较大，不宜反复请求，最好保存为本地避免重复请求

```python
import akshare as ak
import pandas as pd

filepath = r"./stock_info.csv"
df = ak.stock_zh_a_spot()
df.to_csv(filepath)

data = pd.read_csv(filepath)
print(data)
```

akshare 获取到的数据均为 pandas 数据 dataframe，可以直接使用 to_csv 方法指定文件路径保存

```
 #akshare 常用的一些 API

 #指数实时行情和历史行情
 "stock_zh_index_daily"  # 股票指数历史行情数据
 "stock_zh_index_daily_tx"  # 股票指数历史行情数据-腾讯
 "stock_zh_index_daily_em"  # 股票指数历史行情数据-东方财富
 "stock_zh_index_spot"  # 股票指数实时行情数据
  
  # 股票指数-成份股
 "index_stock_cons"  # 股票指数-成份股-最新成份股获取
 "index_stock_cons_csindex"  # 中证指数-成份股
 "index_stock_cons_weight_csindex"  # 中证指数成份股的权重
 "index_stock_info"  # 股票指数-成份股-所有可以获取的指数表
 "index_stock_info_sina"  # 股票指数-成份股-所有可以获取的指数表-新浪新接口
 "index_stock_hist"  # 股票指数-历史成份股
 
  # A 股日频率数据-东方财富
 "stock_zh_a_hist"  # A 股日频率数据-东方财富
 
 # A股实时行情数据和历史行情数据
 "stock_zh_a_spot"  # 新浪 A 股实时行情数据
 "stock_zh_a_spot_em"  # 东财 A 股实时行情数据
 "stock_sh_a_spot_em"  # 东财沪 A 股实时行情数据
 "stock_sz_a_spot_em"  # 东财深 A 股实时行情数据
 "stock_bj_a_spot_em"  # 东财京 A 股实时行情数据
 "stock_new_a_spot_em"  # 东财新股实时行情数据
 "stock_kc_a_spot_em"  # 东财科创板实时行情数据
 "stock_zh_b_spot_em"  # 东财 B 股实时行情数据
 "stock_zh_a_daily"  # 获取 A 股历史行情数据(日频)
 "stock_zh_a_minute"  # 获取 A 股分时历史行情数据(分钟)
 "stock_zh_a_cdr_daily"  # 获取 A 股 CDR 历史行情数据(日频)
 
 # 个股信息查询
 "stock_individual_info_em"  # 个股信息查询
 
```



```python
import akshare as ak

df_index_info = ak.index_stock_info()  # 获取所有股票指数信息

# 获取某个指数，例如沪深300指数的历史行情数据（新浪和东财）
df_stock_zh_index_daily = ak.stock_zh_index_daily(symbol="0003000")
df_stock_zh_index_daily_em = ak.stock_zh_index_daily_em(symbol="0003000")

# 获取某个股票，例如000002的历史行情数据（每日）
df_stock_daily = ak.stock_zh_a_daily(symbol="000002", start_date="20230201", end_date="20230202")
df_stock_daily_em = ak.stock_zh_a_hist_min_em(symbol="000002", start_date="2023-02-01 09:32:00", end_date="2023-02-02 09:32:00", period="5") # 每5min一条数据

# 实时行情数据 
# ak.stock_zh_index_spot() #指数实时行情
# ak.stock_zh_a_spot() #股票实时行情
```

参考代码：
```
# zz1000_pe_df = ak.stock_a_pe(symbol="000852.XSHG").iloc[-1708:]
# zz1000_pe_pct = zz1000_pe_df[['middlePETTM','close']].rank(ascending=True, pct=True)*100
# res = ak.stock_zh_a_spot()
# res = ak.stock_info_a_code_name() # 所有a股代码和名称
# res = ak.stock_zh_a_daily(symbol="000002", start_date="20221212", end_date="21000000") # 某一股票历史数据

# res = ak.stock_zh_a_hist(symbol="000002", start_date="20230101")  # 某一股票历史数据

# res = ak.index_zh_a_hist(symbol="000300", start_date="20230101")
# ak.stock_zh_index_daily()
# res = ak.stock_zh_index_spot()

    # stock_index = ak.stock_zh_index_spot()
    # stock_index_file = "A股指数_" + today + ".csv"
    # save(stock_index, _file=stock_index_file, root_path=base_path)
    #
    # hs300 = ak.index_zh_a_hist(symbol="000300")
    # hs300_file = "沪深300_" + today + ".csv"
    # save(hs300, _file=hs300_file, root_path=base_path)
```
