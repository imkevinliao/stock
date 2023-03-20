from soc import Analyze, Download

# 个股成分信息 个股信息查询
# data = ak.index_stock_hist()
# data = ak.stock_individual_info_em()

# inst = Download(fold=r"D:\github\save")

import akshare as ak

# data = ak.fund_etf_hist_em(symbol="510310")
ak.fund_etf_fund_info_em()
ak.fund_etf_hist_sina()

