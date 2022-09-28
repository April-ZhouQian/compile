from lc_demo.transpile import transpile_test
import lc_demo.mfunc as Func
from lc_demo.asm import *
from lc_demo.serialize import serialize
import json
res = transpile_test(
    r"""
        c = 2 + 6;
        print(c);
        return c;
    """
)

func = Func.MFunc(res.fptr.metadata.freenames, res.fptr,globals={'print': print, 'm': 3})
exec_res = func.__call__()


dict = serialize(res)

with open("res_json.txt","w") as f:
    json.dump(dict, f)


