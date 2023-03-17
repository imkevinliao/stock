from soc import AnalyzeStock

inst = AnalyzeStock(csvfile="")
inst.basic_info()
inst.query_compare(compare_price=0.407, plot=True, start_time="20220316")
