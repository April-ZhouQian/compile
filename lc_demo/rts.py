from __future__ import annotations
from lc_demo.asm import TrObject
from typing_extensions import Protocol

class UnaryOperator(Protocol):
    def __call__(self, __arg: TrObject) -> TrObject:
        ...
class BinaryOperator(Protocol):
    def __call__(self, __arg1: TrObject, __arg2: TrObject) -> TrObject:
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
    def object_bool(trobject:TrObject) ->bool:
        return bool(trobject)
    @staticmethod
    def object_call_ex(rt_func: TrObject, rt_args:list):
        return rt_func(*rt_args)  # type: ignore
   ###一元运算
    @staticmethod
    def object_inv(arg: TrObject):
        return ~arg # type: ignore
    @staticmethod
    def object_not(arg: TrObject):
        return not arg
    @staticmethod
    def object_neg(arg: TrObject):
        return - arg #type: ignore
    @staticmethod
    def object_pos(arg: TrObject):
        return + arg #type: ignore
    #二元运算
    @staticmethod
    def object_add(arg1: TrObject, arg2: TrObject):
        return arg1 + arg2 #type: ignore
    @staticmethod
    def object_sub(arg1: TrObject, arg2: TrObject):
        return arg1 - arg2 #type: ignore
    @staticmethod
    def object_mul(arg1: TrObject, arg2: TrObject):
        return arg1 * arg2  #type: ignore
    @staticmethod
    def object_div(arg1: TrObject, arg2: TrObject):
        return arg1 / arg2  #type: ignore
    @staticmethod
    def object_eq(arg1: TrObject, arg2: TrObject):
        return arg1 == arg2
    @staticmethod
    def object_noteq(arg1: TrObject, arg2: TrObject):
        return arg1 != arg2
    @staticmethod
    def object_gt(arg1: TrObject, arg2: TrObject):
        return arg1 > arg2  #type: ignore
    @staticmethod
    def object_lt(arg1: TrObject, arg2: TrObject):
        return arg1 < arg2 #type: ignore
    @staticmethod
    def object_ge(arg1: TrObject, arg2: TrObject):
        return arg1 >= arg2 #type: ignore
    @staticmethod
    def object_le(arg1: TrObject, arg2: TrObject):
        return arg1 <= arg2  #type: ignore
    @staticmethod
    def object_mod(arg1: TrObject, arg2: TrObject):
        return arg1 % arg2 #type: ignore


RTS.gen_OOFuncs()
RTS.gen_OOOFuncs()