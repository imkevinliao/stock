from soc import Analyze, AnalyzeType

# example
inst = Analyze(code="000001", analyze_type=AnalyzeType.STOCK)
inst.info()
inst.query(compare_price=12.82, plot=True)

inst = Analyze(code="000001", analyze_type=AnalyzeType.FUND)
inst.info()
inst.query(compare_price=0.940, plot=True)
