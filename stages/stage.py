
import core.op as op
import core.recongnize_process as rp
from core.recongnize_process import ImgOperation


class Stage :
    def __init__(self,cycle):
        self.cycle = cycle
    #cycle 是一个循环下，各个图片路径和所需操作
    #cycle 由ImgOperation 组成
    cycle = [ImgOperation]


    def operate(self):
        for pic in self.cycle:
            res = pic.operate()
            if res == "CUTTING":
                return "CUTTING"


