from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from lc_demo.asm import TrObject
import lc_demo.trfunc as trfunc
import lc_demo.rts as rts


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
    retval: TrObject | None
    func: trfunc.TrFunc

    def load_free(self, operand: int) -> TrObject:
        v = self.freevars[operand].Value
        ##判断是否v==null
        return v

    def load_local(self, operand: int) -> TrObject:
        v = self.localvars[operand].Value
        return v

    def load_global(self, var: TrObject) -> TrObject:
        v = self.func.globals[var]
        return v
    def load_reference(self, operand: int) -> Variable:
        if operand < 0:
            return self.func.freevars[-operand - 1]
        return self.localvars[operand]

    def store_free(self, slot: int, value: TrObject):
        self.freevars[slot].Value = value

    def store_local(self, slot: int, value: TrObject):
        self.localvars[slot].Value = value
    def store_global(self, v:TrObject, value: TrObject):
        self.func.globals[v] = value
    @staticmethod
    def make(func: trfunc.TrFunc, localvars: list[Variable]) -> Frame:
        return Frame(
            CONT=STATUS(0),
            func=func,
            localvars=localvars,
            freevars=func.freevars,
            retval=rts.RTS.object_none,
        )
