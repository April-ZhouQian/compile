from __future__ import annotations
from dataclasses import dataclass
from lc_demo.lc_ast import *
from lc_demo.Collections import OrderedSet

@dataclass
class _scope:
    local_vars: OrderedSet[str]
    free_vars: OrderedSet[str]

@dataclass(repr=False)
class scope:
    local_vars: OrderedSet[str]
    free_vars: OrderedSet[str]
    parent: scope | None = None
    @classmethod
    def new(cls, parent: scope | None):
        return cls(OrderedSet(), OrderedSet(), parent)
    def find_var(self: scope, x: str):
        ###判断是否出现在上层
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
        for elt in x.args:
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

def compute_scope(x: LC, S:scope, args: list[str]):
    if args:
        for arg in args:
            S.local_vars.add(arg)
    enteredvars:dict[str, is_write] = {}
    explicit_globalvars:set[str]=set()
    def scan_variable(x: LC):
        if isinstance(x, Var):
            enteredvars.setdefault(x.name, False)
        elif isinstance(x, AssignVal):
            enteredvars[x.var] = True
            scan_variable(x.value)
        elif isinstance(x, NamedFunc):
            if x.name:
                enteredvars[x.name] = True
        else:
            visit(scan_variable, x)
    scan_variable(x)
    for enter, is_write in enteredvars.items():
        if enter in explicit_globalvars:
            continue
        if not S.find_var(enter):
            if is_write:
                S.local_vars.add(enter)
    return S
