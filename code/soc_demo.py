import os.path

from soc import Analyze, CodeType

os.environ['no_proxy'] = '*'


def demo():
    inst = Analyze(code="000002", codetype=CodeType.STOCK)
    inst.basic_info()
    # inst.query()
    # inst.plot()


if __name__ == '__main__':
    demo()
