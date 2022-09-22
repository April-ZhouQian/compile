from __future__ import annotations
import typing
from lc_demo.asm import TrFuncPtr, TrObject
import lc_demo.frame as Frame
import lc_demo.traffy as traffy

class TrFunc:
    freevars: list[Frame.Variable]
    globals: dict[TrObject,TrObject]
    fptr: TrFuncPtr
    def __init__(self, freevars, fptr, globals):
        self.freevars = freevars
        self.fptr = fptr
        self.globals = globals
    def __call__(self, *args):
        return self.Execute(args=args, frame=None)
    def Execute(self, args: typing.Sequence[TrObject], frame: Frame.Frame|None) ->TrObject:
        localvars :list[Frame.Variable] =[]
        length = len(self.fptr.metadata.localnames)
        for i in range(length):
            localvars.append(Frame.Variable(None))
        for i in range(len(args)):
            localvars[i].Value = args[i]
        frame = Frame.Frame.make(self, localvars)
        traffy.exec_mir(self.fptr.code, frame)
        return frame.retval

