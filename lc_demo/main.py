from lc_demo.lc_ast import *
import wisepy2
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.matlab import MatlabLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from lc_demo.transpile import transpile_test
from lc_demo.mfunc import MFunc
from lc_demo.deserialize import deserialize
from lc_demo.serialize import serialize
from lc_demo.asm import return_globals, ModuleSpec
import json

lc_completer = WordCompleter(
    ["if", "else", "while", "return", "function", "exit"], ignore_case=True
)
globals = return_globals()
global_vars ={'print': print, 'exit': exit}
@wisepy2.wise
def mc(fin: str, fout: str):
    with open(fin, "r", encoding="utf-8") as f:
        source_code = f.read()
    res = transpile_test(source_code)
    dict = serialize(res)
    with open(fout,"w") as f:
        json.dump(dict, f)

@wisepy2.wise
def mci(*filenames: str):
    if not filenames:
        repl()
        return
    with open(filenames[0]) as f:
        res = json.load(f)
    json_ir = typing.cast(ModuleSpec, deserialize(res, globals))
    func = MFunc(json_ir.fptr.metadata.freenames, json_ir.fptr,globals=global_vars)
    exec_res = func.__call__()
    if(exec_res):
        print("执行结果为：", exec_res)

def prompt_continuation(width, line_number, is_soft_wrap):
    return "." * width


def repl():
    session = PromptSession(lexer=PygmentsLexer(MatlabLexer), completer=lc_completer)
    text = ""
    while True:
        text = session.prompt(
            "mi> ",
            multiline=True,
            prompt_continuation=prompt_continuation,
            auto_suggest=AutoSuggestFromHistory(),
        )
        res = transpile_test(text)
        func = MFunc(res.fptr.metadata.freenames, res.fptr,globals=global_vars)
        exec_res = func.__call__()
        if exec_res:
            print("执行结果为：", exec_res)
