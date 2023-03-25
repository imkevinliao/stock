from soc import AnalyzeStock, AnalyzeFund

# example
codes = ["000001"]

inst = AnalyzeFund(code=codes[0])
inst.info()
inst.query(compare_price=0.940, plot=True)

inst = AnalyzeStock(code=codes[0])
inst.info()
inst.query(compare_price=12.82, plot=True)
