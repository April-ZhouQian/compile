from __future__ import annotations
import typing
from lc_demo.asm import MFuncPtr, MObject
import lc_demo.frame as Frame
import lc_demo.intp as intp

class MFunc:
    freevars: list[Frame.Variable]
    globals: dict[MObject,MObject]
    fptr: MFuncPtr
    def __init__(self, freevars, fptr, globals):
        self.freevars = freevars
        self.fptr = fptr
        self.globals = globals
    def __call__(self, *args):
        return self.Execute(args=args, frame=None)
    def Execute(self, args: typing.Sequence[MObject], frame: Frame.Frame|None) ->MObject:
        localvars :list[Frame.Variable] =[]
        length = len(self.fptr.metadata.localnames)
        for i in range(length):
            localvars.append(Frame.Variable(None))
        for i in range(len(args)):
            localvars[i].Value = args[i]
        frame = Frame.Frame.make(self, localvars)
        intp.exec_mir(self.fptr.code, frame)
        return frame.retval

