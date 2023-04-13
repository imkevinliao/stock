# SOC
通过简单的代码就可以得到你想知道的股票的信息，让代码变得非常简单
```
from config import *
from soc import CodeType, Analyze

stock = ["000002"]
fund = ["000001", "000003"]
index = ["000300", "000905", "000016"]
"""
指数也可以写为 000300，由于指数需要带市场标识，但是考虑到代码的统一性，
不需要输入时候给定市场标识，会从json文件中读取然后将 000300 改为 sh000300 用户无需关心
"""
for i in stock:
    inst = Analyze(code=i, codetype=CodeType.STOCK)
    inst.basic_info()
    inst.query()
    inst.plot()
for i in fund:
    inst = Analyze(code=i, codetype=CodeType.FUND)
    inst.basic_info()
    inst.query()
    inst.plot()
for i in index:
    inst = Analyze(code=i, codetype=CodeType.INDEX)
    inst.basic_info()
    inst.query()
    inst.plot()
```
享受技术带来的快来，拿起数据的武器，分析某一只股票的过去，然后预测它的将来，不一定正确，但旅途的本身就是一件很快乐的事情，旅行者，不是吗？提瓦特大陆不只有马斯克礁。

**如何使用**
1. 安装 Python （Python版本需要大于3.6）
2. 安装依赖的库 pip install -r requirements.txt

# 更新信息
2023.04.12 --更新了新版的soc.py代码，旧版本代码被废弃更名为soc_old.py

2023.04.13 --更新结构，从文件中读取股票指数，方便分析股票指数

# QA
Q:为什么命名为soc.py?

A:因为芯片是一个系统的核心：System-On-a-Chip(SoC)，我想表达的是它是核心文件，当然我可以用Core命名，但是SoC听起来更酷

Q:代码中存在一定的冗余，后续是否会考虑进行优化?

A:少量的冗余是任何代码都无法避免的（咳咳，实际是没有时间进行处理）

Q:枚举类型通常不使用其枚举值，但代码中似乎用到了，为什么?

A:代码必须服务于人，如果从使用者角度看，需要其枚举值，那么便不必拘泥于形式。当然是不推荐的做法。

# 致谢
感谢Akshare提供的数据接口

# 实用小工具 
[计算本金利率收益](./tool/calc.py)

[计算个人所得税](./tool/tax.py)

[计算每月工时及下班时间](./tool/worktime.py)
