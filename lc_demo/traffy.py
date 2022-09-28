from __future__ import annotations
from lc_demo.asm import *
import lc_demo.rts as rts
from lc_demo.frame import Frame, STATUS
import lc_demo.mfunc as Func
import typing_extensions

def exec_mlhs(x: MLHS, frame: Frame, value: MObject):
    if isinstance(x, StoreLocal):
        frame.store_local(x.slot, value)
    elif isinstance(x, StoreFree):
        frame.store_free(x.slot, value)
    elif isinstance(x, StoreGlobal):
        frame.store_global(x.name, value)
    else:
        if typing.TYPE_CHECKING:
            typing_extensions.assert_never(x)
        else:
            assert False, x

def exec_mir(x: MIR, frame: Frame) ->MObject :
    if isinstance(x, MBlock):
        for item in x.suite:
            exec_mir(item, frame)
            if frame.CONT != STATUS.NORMAL:
                break
        return rts.RTS.object_none
    elif isinstance(x, MReturn):
        rt_value = exec_mir(x.value, frame)
        frame.CONT = STATUS.RETURN
        frame.retval = rt_value
        return rts.RTS.object_none
    elif isinstance(x, MWhile):
        rt_value = rts.RTS.object_none
        while(rts.RTS.object_bool(exec_mir(x.cond, frame))):
            rt_value = exec_mir(x.body, frame)
            if frame.CONT == STATUS.NORMAL:
                continue
            break
        return rt_value
    elif isinstance(x, MIf):
        if(rts.RTS.object_bool(exec_mir(x.cond, frame))):
            exec_mir(x.body, frame)
        else:
            if x.else_body:
                exec_mir(x.else_body, frame)
        return rts.RTS.object_none
    elif isinstance(x, Constant):
        return x.obj
    elif isinstance(x, MLogicalAnd):
        rt_res = exec_mir(x.left, frame)
        if not rts.RTS.object_bool(rt_res):
            return rt_res
        return exec_mir(x.right, frame)
    elif isinstance(x, MLogicalOr):
        rt_res = exec_mir(x.left, frame)
        if rts.RTS.object_bool(rt_res):
            return rt_res
        return exec_mir(x.right, frame)
    elif isinstance(x, MLogicalNot):
        value = exec_mir(x.operand, frame)
        rt_value = not value
        return rt_value
    elif isinstance(x, MBinOp):
        rt_1 = exec_mir(x.left, frame)
        rt_2 = exec_mir(x.right, frame)
        opfunc = rts.RTS.OOOFuncs[x.op]
        rt_res = opfunc(rt_1, rt_2)
        return rt_res
    elif isinstance(x, MUnaryOp):
        rt_operand = exec_mir(x.operand, frame)
        opfunc = rts.RTS.OOFuncs[x.op]
        rt_res = opfunc(rt_operand)
        return rt_res
    elif isinstance(x, MCall):
        rt_args = []
        for arg in x.args:
            rt_args.append(exec_mir(arg, frame))
        rt_func = exec_mir(x.func, frame)
        rt_res = rts.RTS.object_call_ex(rt_func, rt_args)
        return rt_res
    elif isinstance(x, FreeVar):
        freeval = frame.load_free(x.slot)
        return freeval
    elif isinstance(x, LocalVar):
        localval = frame.load_local(x.slot)
        return localval
    elif isinstance(x, GlobalVar):
        globalvar = frame.load_global(x.name)
        return globalvar
    elif isinstance(x, MAssign):
        rt_res = exec_mir(x.rhs, frame)
        exec_mlhs(x.lhs, frame, rt_res)
        return rt_res
    elif isinstance(x, MFuncDef):
        freevars: list= []
        if len(x.freeslots) != 0:
            for var in x.freeslots:
                freevars.append(frame.load_reference(var))
        return Func.MFunc(freevars, x.fptr, globals=frame.func.globals)
    else:
        if typing.TYPE_CHECKING:
            typing_extensions.assert_never(x)
        else:
            assert False, x
