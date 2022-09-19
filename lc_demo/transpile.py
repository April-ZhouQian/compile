from __future__ import annotations
from lc_demo.lc_ast import *
from lc_demo import asm as ir
import typing
from lc_demo.scoper import scope, compute_scope
from lc_demo.Collections import OrderedSet
from lc_demo.lc import parser

class Transpiler:
    def __init__(self, source_code: str | None, parent_scope: scope | None):
        self.souce_code = source_code
        self.parent_scope = parent_scope

    def create_fptr_builder(self, code: ir.MIR, name: str):
        metadata = ir.Metadata(
            localnames=list(self.scope.local_vars),
            freenames=list(self.scope.free_vars),
            codename=name,
            sourceCode=None,
        )
        return ir.TrFuncPtr(code=code, metadata=metadata)

    def before_visit(self, x, args):
        self.scope = compute_scope(
            x,
            scope(
                parent=self.parent_scope,
                local_vars=OrderedSet(),
                free_vars=OrderedSet(),
            ),
            args,
        )

    # 判断当前层的free来自上层的free还是local
    def load_derefence(self, id: str):
        if id in self.scope.local_vars:
            i = self.scope.local_vars.order(id)
            return i
        elif id in self.scope.free_vars:
            i = self.scope.free_vars.order(id)
            return -i - 1
        else:
            raise NameError(f"{id} is not a local/free variable")

    def store_name_(self, id: str) -> ir.MLHS:
        if id in self.scope.local_vars:
            i = self.scope.local_vars.order(id)
            return ir.StoreLocal(slot=i)
        # elif id in self.scope.free_vars:
        else:
            i = self.scope.free_vars.order(id)
            return ir.StoreFree(slot=i)
    def load_name_(self, id: str):
        if id in self.scope.local_vars:
            i = self.scope.local_vars.order(id)
            return ir.LocalVar(slot=i)
        # elif id in self.scope.free_vars:
        else:
            i = self.scope.free_vars.order(id)
            return ir.FreeVar(slot=i)

    def transpile(self, x: LC):
        if isinstance(x, NumberVal) | isinstance(x, StringVal) | isinstance(x, BoolVal):
            v = const_to_variant(x)
            return ir.Constant(v)
        # 此处左值只可能是变量，因此可以直接调用store_name
        elif isinstance(x, AssignVal):
            value = self.transpile(x.value)
            lhs = self.store_name_(x.var)
            return ir.TrAssign(lhs, value)
        elif isinstance(x, UnaryOp):
            op = unaryop_indices[x.op]
            operand = self.transpile(x.right)
            return ir.TrUnaryOp(operand=operand, op=op)
        elif isinstance(x, Return):
            value = self.transpile(x.body)
            return ir.TrReturn(value)
        elif isinstance(x, Block):
            xs = []
            for item in x.body:
                xs.append(self.transpile(item))
            return ir.TrBlock(suite=xs)
        elif isinstance(x, WhileBlock):
            cond = self.transpile(x.cond)
            body = []
            for item in x.body.body:
                body.append(self.transpile(item))
            body_block = ir.TrBlock(body)
            return ir.TrWhile(cond=cond, body=body_block)
        elif isinstance(x, IfBlock):
            cond = self.transpile(x.cond)
            body = []
            else_body = []
            for item in x.body.body:
                body.append(self.transpile(item))
            body_block = ir.TrBlock(body)
            for item in x.else_body.body:
                else_body.append(self.transpile(item))
            else_block = ir.TrBlock(else_body)
            return ir.TrIf(cond=cond, body=body_block, else_body=else_block)
        elif isinstance(x, CallFunc):
            func = self.transpile(x.func)
            args = []
            # CallFunc的参数为实参: list[LC] 要派发
            for item in x.args:
                arg = self.transpile(item)
                args.append(arg)
            return ir.TrCall(func=func, args=args)
        # ★函数定义：创建新的transpiler对象对function内部进行一一转换
        # 1. 创建新的transpiler并将当前scope作为其parent scope
        # 2. 调用before_visit函数，获取当前func的scope
        # 3. 对于函数体中的每条语句进行转换
        # 4. 创建fptr用于记录函数的信息
        # 5. 利用load_deference判断当前func内部的free来自上层的free还是local并记录其位置
        # 6. 利用4、5得到的信息，得到转换的TrFuncDef
        # 7. 将funcName作为左值进行存储，并完成赋值操作，右值为6得到的TrFuncDef
        elif isinstance(x, NamedFunc):
            transpiler = Transpiler(self.souce_code, self.scope)
            transpiler.before_visit(x.body, x.arg)
            xs = []
            for item in x.body.body:
                xs.append(transpiler.transpile(item))
            block = ir.TrBlock(xs)
            fptr = transpiler.create_fptr_builder(block, x.name)
            freelots = []
            for item in transpiler.scope.free_vars:
                freelots.append(self.load_derefence(item))
            func_body = ir.TrFuncDef(fptr=fptr, freeslots=freelots)
            lhs = self.store_name_(x.name)
            return ir.TrAssign(lhs=lhs, rhs=func_body)
        elif isinstance(x, LogicalAnd):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            return ir.TrLogicalAnd(left=l, right=r)
        elif isinstance(x, LogicalOr):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            return ir.TrLogicalOr(left=l, right=r)
        elif isinstance(x, LogicalNot):
            return ir.TrLogicalNot(x.right)
        elif isinstance(x, BinOp):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            if isinstance(x.op, Var):
                binop = x.op.name
                op = binop_indices[binop]
                return ir.TrBinOp(left=l, right=r, op=op)
            else:
                return
        elif isinstance(x, Var):
            return self.load_name_(x.name)
        else:
            return visit(self.transpile, x)


def visit(f, x: LC):
    if isinstance(x, AssignVal):
        return f(x.value)
    elif isinstance(x, Block):
        res = []
        for elt in x.body:
            res.append(f(elt))
        return res
    elif isinstance(x, IfBlock):
        res = []
        res.append(f(x.cond))
        for elt in x.body.body:
            res.append(f(elt))
        for elt in x.else_body.body:
            res.append(f(elt))
        return res
    elif isinstance(x, WhileBlock):
        res = []
        res.append(f(x.cond))
        for elt in x.body.body:
            res.append(f(elt))
        return res
    elif isinstance(x, Return):
        return f(x.body)
    elif isinstance(x, NamedFunc):
        return f(x.body)
    elif isinstance(x, CallFunc):
        res = []
        res.append(f(x.func))
        for elt in x.args:
            res.append(f(elt))
        return res
    elif isinstance(x, BinOp):
        res = []
        res.append(f(x.left))
        res.append(f(x.op))
        res.append(f(x.right))
    elif isinstance(x, UnaryOp):
        return f(x.right)
    elif isinstance(x, LogicalOr):
        res = []
        res.append(f(x.left))
        res.append(f(x.right))
    elif isinstance(x, LogicalAnd):
        res = []
        res.append(f(x.left))
        res.append(f(x.right))
    elif isinstance(x, LogicalNot):
        return f(x.right)
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


binop_indices: dict[str, ir.OpBin] = {
    "add": ir.OpBin.ADD,
    "sub": ir.OpBin.SUB,
    "mul": ir.OpBin.MUL,
    "div": ir.OpBin.DIV,
    "eq": ir.OpBin.Eq,
    "noteq": ir.OpBin.NotEq,
    "gt": ir.OpBin.Gt,
    "lt": ir.OpBin.Lt,
    "ge": ir.OpBin.Ge,
    "le": ir.OpBin.Le,
}

unaryop_indices: dict[str, ir.OpUnary] = {
    "inv": ir.OpUnary.INV,
    "not": ir.OpUnary.NOT,
    "neg": ir.OpUnary.NEG,
    "pos": ir.OpUnary.POS,
}


def const_to_variant(x: LC) -> ir.TrObject:
    if isinstance(x, BoolVal):
        return x.value
    elif isinstance(x, NumberVal):
        return x.value
    elif isinstance(x, StringVal):
        return x.value
    else:
        raise TypeError(x)


def compile_test(src: str):
    x = parser.parse(src)
    top = Transpiler(src, None)
    top.before_visit(x, [])
    block = visit(top.transpile, x)
    fptr = top.create_fptr_builder(block, "top")
    return ir.ModuleSpec(src, fptr)

