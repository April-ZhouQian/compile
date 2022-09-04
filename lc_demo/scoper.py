from __future__ import annotations
from dataclasses import dataclass, field
from lc_demo.lc_ast import *
from lc_demo.lc import parser

@dataclass
class _scope:
    local_vars: set
    free_vars: set

@dataclass(repr=False)
class scope:
    local_vars: set = field(default_factory=set)
    free_vars: set = field(default_factory=set)
    parent: scope | None = None

    def find_var(self: scope, x: str):
        if x in self.local_vars or x in self.free_vars:
            return True
        if self.parent:
            if self.parent.find_var(x):
                self.free_vars.add(x)
                return True
        return False
    def __repr__(self) -> str:
        return repr(_scope(self.local_vars, self.free_vars))

is_write = bool
def scan(self: scope, x: str):
    if self.find_var(x):
        return True
    return False


def visit(f: typing.Callable[[LC], typing.Any], x: LC):
    if isinstance(x, AssignVal):
        f(x.value)
    elif isinstance(x, Block):
        for elt in x.body:
            f(elt)
    elif isinstance(x, IfBlock):
        f(x.cond)
        for elt in x.body.body:
            f(elt)
        for elt in x.else_body.body:
            f(elt)
    elif isinstance(x, WhileBlock):
        f(x.cond)
        for elt in x.body.body:
            f(elt)
    elif isinstance(x, Return):
        f(x.body)
    elif isinstance(x, NamedFunc):
        f(x.body)
    elif isinstance(x, CallFunc):
        f(x.func)
        for elt in x.arg:
            f(elt)
    elif isinstance(x, BinOp):
        f(x.left)
        f(x.op)
        f(x.right)
    elif isinstance(x, UnaryOp):
        f(x.right)
    elif isinstance(x, LogicalOr):
        f(x.left)
        f(x.right)
    elif isinstance(x, LogicalAnd):
        f(x.left)
        f(x.right)
    elif isinstance(x, LogicalNot):
        f(x.right)
    elif isinstance(x, Var):
        pass
    elif isinstance(x, BoolVal):
        pass
    elif isinstance(x, StringVal):
        pass
    elif isinstance(x, NumberVal):
        pass
    else:
        if typing.TYPE_CHECKING:
            typing_extensions.assert_never(x)
        else:
            assert False, x


S = scope()
S.parent = scope(local_vars = {"a", "c"})

def test(x: LC, S:scope, res: list):
    nested_funcs: list[NamedFunc] = []
    enteredvars:dict[str, is_write] = {}
    def scan_variable(x: LC):
        if isinstance(x, Var):
            enteredvars.setdefault(x.name, False)
        elif isinstance(x, AssignVal):
            enteredvars[x.var] = True
            scan_variable(x.value)
        elif isinstance(x, NamedFunc):
            if x.name:
                enteredvars[x.name] = True
            nested_funcs.append(x)
        else:
            visit(scan_variable, x)
    scan_variable(x)
    for enter, is_write in enteredvars.items():
        if not S.find_var(enter):
            if is_write:
                S.local_vars.add(enter)
    for func in nested_funcs:
        local_vars = set()
        for arg in func.arg:
            local_vars.add(arg)
        sub_res = []
        res.append(
            (
                func.name,
                test(func.body, scope(local_vars=local_vars, parent = S), sub_res),
                sub_res
            ))
    return S


res_list = []
res = test(
    parser.parse(r"""
        a = 10;
        b = true;
        c = 1;
        d = c;
        function func1(m, n)
        {
            a = m;
            x = c;
            function func1_1(n)
            {
                a = m;
            }
        }
        function func2(m)
        {
            b = m;
            x = c;
        }
    """),
    S,
    res_list
)

for e in res_list:
    print(e)
