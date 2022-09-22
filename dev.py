from lc_demo.transpile import compile_test
import lc_demo.trfunc as Func


res = compile_test(
    r"""
        a = 2;
        function f(x)
        {
            c = x + m;
            function g(y)
            {
                d = a + y;
                return d;
            }
            return c + g(1);
        }
        return f(1)
    """
)

func = Func.TrFunc(res.fptr.metadata.freenames, res.fptr,globals={'print': print, 'm': 3})
exec_res = func.__call__()
print(exec_res)


