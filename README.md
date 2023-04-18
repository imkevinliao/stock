# SOC
通过简单的代码就可以得到你想知道的股票的信息，让代码变得非常简单

享受技术带来的快来，拿起数据的武器，分析某一只股票的过去，然后预测它的将来，不一定正确，但旅途的本身就是一件很快乐的事情，旅行者，不是吗？提瓦特大陆不只有马斯克礁。

```
soc_demo.py:
from soc import Analyze, CodeType
def demo():
    inst = Analyze(code="000002", codetype=CodeType.STOCK)
    inst.basic_info()
    inst.query(compare_price=None)
    inst.plot()
if __name__ == '__main__':
    demo()

generate.py:
生成json文件，目前用于绘图时候增加股票代码中文信息，以及分析指数自动带上标识符，json文件已经生成

soc_down.py:
生成行业历史资金流
```
# 要求
1. 安装 Python （Python版本需要大于3.6）
2. 安装依赖的库 pip install -r requirements.txt

# 致谢
感谢Akshare提供的数据接口

# 实用小工具 
[计算本金利率收益](./tool/calc.py)

[计算个人所得税](./tool/tax.py)

[计算每月工时及下班时间](./tool/worktime.py)
