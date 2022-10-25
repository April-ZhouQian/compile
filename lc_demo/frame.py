from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from lc_demo.asm import MObject
import lc_demo.mfunc as mfunc
import lc_demo.rts as rts


class Variable:
    Value: MObject

    def __init__(self, value: MObject) -> None:
        self.Value = value


class STATUS(IntEnum):
    NORMAL = 0
    RETURN = 1


@dataclass
class Frame:
    CONT: STATUS
    localvars: list[Variable]
    freevars: list[Variable]
    retval: MObject | None
    func: mfunc.MFunc

    def load_free(self, operand: int) -> MObject:
        v = self.freevars[operand].Value
        if v == None:
            name = self.func.fptr.metadata.freenames[operand]
            raise NameError("undefined free variable {name}".format(name = name))
        return v

    def load_local(self, operand: int) -> MObject:
        v = self.localvars[operand].Value
        if v == None:
            name = self.func.fptr.metadata.localnames[operand]
            raise NameError("undefined local variable {name}".format(name = name))
        return v

    def load_global(self, var: MObject) -> MObject:
        if var in self.func.globals:
            v = self.func.globals[var]
            if v == None:
                raise NameError("undefined global variable {name}".format(name = var))
            return v
        else:
            raise NameError("no global variable {name}".format(name = var))
    def load_reference(self, operand: int) -> Variable:
        if operand < 0:
            return self.func.freevars[-operand - 1]
        return self.localvars[operand]

    def store_free(self, slot: int, value: MObject):
        self.freevars[slot].Value = value

    def store_local(self, slot: int, value: MObject):
        self.localvars[slot].Value = value
    def store_global(self, v:MObject, value: MObject):
        self.func.globals[v] = value
    @staticmethod
    def make(func: mfunc.MFunc, localvars: list[Variable]) -> Frame:
        return Frame(
            CONT=STATUS(0),
            func=func,
            localvars=localvars,
            freevars=func.freevars,
            retval=rts.RTS.object_none,
        )
