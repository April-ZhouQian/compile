from lc_demo.transpile import *

res = compile_test(
    r"""
        a = 8;
        y = 0;
        function func1(b)
        {
            x = 1;
            y = b;
            function func1_1()
            {
                a = 9;
                c = 10;
            }
        }
    """
)
print(res.fptr.code)
print()
print(res.fptr.metadata)


