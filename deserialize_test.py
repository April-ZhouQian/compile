import json
import lc_demo.mfunc as Func
import typing
from lc_demo.deserialize import *
from lc_demo.asm import return_globals, ModuleSpec

globals = return_globals()
with open("res_json.txt") as f:
    res = json.load(f)
json_ir = typing.cast(ModuleSpec, deserialize(res, globals))

func = Func.MFunc(json_ir.fptr.metadata.freenames, json_ir.fptr,globals={'print': print, 'm': 3})
exec_res = func.__call__()
if exec_res:
    print("结果为：",exec_res)
