import os

from soc import Analyze, CodeType

index = ["sh000922"]

for i in index:
    inst = Analyze(code=i, codetype=CodeType.INDEX)
    inst.basic_info()
    inst.query()
    inst.plot()