from __future__ import annotations
from lc_demo.asm import TrObject


class RTS:
    object_none: TrObject
    OOFuncs :list
    OOOFuncs: list

    def __init__(self) -> None:
        self.OOFuncs = self.gen_OOFuncs()
        self.OOOFuncs = self.gen_OOOFuncs()

    def gen_OOFuncs(self):
        OOFuncs = []
        OOFuncs.append(self.object_inv)
        OOFuncs.append(self.object_not)
        OOFuncs.append(self.object_neg)
        OOFuncs.append(self.object_neg)
        return OOFuncs

    def gen_OOOFuncs(self):
        OOOFuncs = []
        OOOFuncs.append(self.object_add)
        OOOFuncs.append(self.object_sub)
        OOOFuncs.append(self.object_mul)
        OOOFuncs.append(self.object_div)
        OOOFuncs.append(self.object_eq)
        OOOFuncs.append(self.object_noteq)
        OOOFuncs.append(self.object_gt)
        OOOFuncs.append(self.object_lt)
        OOOFuncs.append(self.object_ge)
        OOOFuncs.append(self.object_le)
        return OOOFuncs

    @staticmethod
    def object_bool(trobject:TrObject) ->bool:
        return bool(trobject)
    @staticmethod
    def object_call_ex(rt_func, rt_args):
        if rt_args:
            return rt_func(rt_args)
        else:
            return rt_func()
   ###一元运算
    @staticmethod
    def object_inv(arg):
        return ~ arg
    @staticmethod
    def object_not(arg):
        return not arg
    @staticmethod
    def object_neg(arg):
        return - arg
    @staticmethod
    def object_pos(arg):
        return + arg
    #二元运算
    @staticmethod
    def object_add(arg1, arg2):
        return arg1 + arg2
    @staticmethod
    def object_sub(arg1, arg2):
        return arg1 - arg2
    @staticmethod
    def object_mul(arg1, arg2):
        return arg1 - arg2
    @staticmethod
    def object_div(arg1, arg2):
        return arg1 / arg2
    @staticmethod
    def object_eq(arg1, arg2):
        return arg1 == arg2
    @staticmethod
    def object_noteq(arg1, arg2):
        return arg1 != arg2
    @staticmethod
    def object_gt(arg1, arg2):
        return arg1 > arg2
    @staticmethod
    def object_lt(arg1, arg2):
        return arg1 < arg2
    @staticmethod
    def object_ge(arg1, arg2):
        return arg1 >= arg2
    @staticmethod
    def object_le(arg1, arg2):
        return arg1 <= arg2