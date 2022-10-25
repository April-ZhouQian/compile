from lc_demo.transpile import transpile_test
import lc_demo.mfunc as Func
from lc_demo.asm import *
from lc_demo.serialize import serialize
import json
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.matlab import MatlabLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
lc_completer = WordCompleter(
    ["if", "else", "while", "return", "function", "exit"], ignore_case=True
)
def prompt_continuation(width, line_number, is_soft_wrap):
    return "." * width
text = """
a = 3;
function f()
{
    a = 4;
    print(a);
}
f();
print(a);
"""
res = transpile_test(text)
func = Func.MFunc(res.fptr.metadata.freenames, res.fptr,globals={'print': print, 'a':3})
exec_res = func.__call__()
if exec_res:
    print("执行结果为：", exec_res)

dict = serialize(res)

with open("res_json.txt","w") as f:
    json.dump(dict, f)

