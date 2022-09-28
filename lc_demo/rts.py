from __future__ import annotations
from lc_demo.asm import MObject
from typing_extensions import Protocol

class UnaryOperator(Protocol):
    def __call__(self, __arg: MObject) -> MObject:
        ...
class BinaryOperator(Protocol):
    def __call__(self, __arg1: MObject, __arg2: MObject) -> MObject:
        ...
class RTS:
    object_none = None
    OOFuncs : list[UnaryOperator] = []
    OOOFuncs: list [BinaryOperator]= []

    @classmethod
    def gen_OOFuncs(cls):
        OOFuncs = cls.OOFuncs
        OOFuncs.append(cls.object_inv)
        OOFuncs.append(cls.object_not)
        OOFuncs.append(cls.object_neg)
        OOFuncs.append(cls.object_pos)
        return OOFuncs

    @classmethod
    def gen_OOOFuncs(cls):
        OOOFuncs = cls.OOOFuncs
        OOOFuncs.append(cls.object_add)
        OOOFuncs.append(cls.object_sub)
        OOOFuncs.append(cls.object_mul)
        OOOFuncs.append(cls.object_div)
        OOOFuncs.append(cls.object_eq)
        OOOFuncs.append(cls.object_noteq)
        OOOFuncs.append(cls.object_lt)
        OOOFuncs.append(cls.object_gt)
        OOOFuncs.append(cls.object_le)
        OOOFuncs.append(cls.object_ge)
        OOOFuncs.append(cls.object_mod)
        return OOOFuncs

    @staticmethod
    def object_bool(MObject:MObject) ->bool:
        return bool(MObject)
    @staticmethod
    def object_call_ex(rt_func: MObject, rt_args:list):
        return rt_func(*rt_args)  # type: ignore
   ###一元运算
    @staticmethod
    def object_inv(arg: MObject):
        return ~arg # type: ignore
    @staticmethod
    def object_not(arg: MObject):
        return not arg
    @staticmethod
    def object_neg(arg: MObject):
        return - arg #type: ignore
    @staticmethod
    def object_pos(arg: MObject):
        return + arg #type: ignore
    #二元运算
    @staticmethod
    def object_add(arg1: MObject, arg2: MObject):
        return arg1 + arg2 #type: ignore
    @staticmethod
    def object_sub(arg1: MObject, arg2: MObject):
        return arg1 - arg2 #type: ignore
    @staticmethod
    def object_mul(arg1: MObject, arg2: MObject):
        return arg1 * arg2  #type: ignore
    @staticmethod
    def object_div(arg1: MObject, arg2: MObject):
        return arg1 / arg2  #type: ignore
    @staticmethod
    def object_eq(arg1: MObject, arg2: MObject):
        return arg1 == arg2
    @staticmethod
    def object_noteq(arg1: MObject, arg2: MObject):
        return arg1 != arg2
    @staticmethod
    def object_gt(arg1: MObject, arg2: MObject):
        return arg1 > arg2  #type: ignore
    @staticmethod
    def object_lt(arg1: MObject, arg2: MObject):
        return arg1 < arg2 #type: ignore
    @staticmethod
    def object_ge(arg1: MObject, arg2: MObject):
        return arg1 >= arg2 #type: ignore
    @staticmethod
    def object_le(arg1: MObject, arg2: MObject):
        return arg1 <= arg2  #type: ignore
    @staticmethod
    def object_mod(arg1: MObject, arg2: MObject):
        return arg1 % arg2 #type: ignore


RTS.gen_OOFuncs()
RTS.gen_OOOFuncs()