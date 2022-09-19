from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from multiprocessing.sharedctypes import Value
from lc_demo.asm import TrObject
from utils.stack import stack
class Variable:
    Value: TrObject
    def __init__(self, value: TrObject) -> None:
        self.Value = value

class STATUS(IntEnum):
    NORMAL = 0
    RETURN = 1

@dataclass
class Frame:
    CONT: STATUS
    localvars: list[Variable]
    freevars: list[Variable]
    retval: TrObject
    # traceback: stack
    # func: TrFunc

    def load_free(self, operand: int) -> TrObject:
        v = self.freevars[operand].Value
        ##判断是否v==null
        return v
    def load_local(self, operand: int) -> TrObject:
        v = self.localvars[operand].Value
        return v
    def load_reference(self, operand: int) -> Variable:
        if operand < 0:
            return self.func.freevars[-operand - 1]
        return self.func.localvars[operand]
