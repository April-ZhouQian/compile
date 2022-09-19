from lc_demo.transpile import compile_test
from lc_demo.traffy import exec_mir
from lc_demo.lc_rts.frame import Frame, STATUS
res = compile_test(
    r"""
        a = 8;
        y = 0;
    """
)
print(res.fptr.code)
print()
print(res.fptr.metadata)
localvars = res.fptr.metadata.localnames
freevars = res.fptr.metadata.freenames
exec_res = exec_mir(res.fptr.code, Frame(STATUS(0), localvars=[], freevars= [], retval=bool(False)))
print(exec_res)

