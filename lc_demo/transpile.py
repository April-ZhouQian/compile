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

    def create_fptr_builder(self, code: ir.MIR, name: str) ->ir.MFuncPtr:
        metadata = ir.Metadata(
            localnames=list(self.scope.local_vars),
            freenames=list(self.scope.free_vars),
            codename=name,
            sourceCode=None,
        )
        return ir.MFuncPtr(code=code, metadata=metadata)

    def before_transpile(self, x: LC, args: list[str]):
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
    def load_derefence(self, id: str) -> int:
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
        elif id in self.scope.free_vars:
            i = self.scope.free_vars.order(id)
            return ir.StoreFree(slot=i)
        else:
            return ir.StoreGlobal(name=id)
    def load_name_(self, id: str) ->ir.MIR:
        if id in self.scope.local_vars:
            i = self.scope.local_vars.order(id)
            return ir.LocalVar(slot=i)
        elif id in self.scope.free_vars:
            i = self.scope.free_vars.order(id)
            return ir.FreeVar(slot=i)
        else:
            return ir.GlobalVar(name=id)

    def transpile(self, x: LC):
        if isinstance(x, NumberVal) or isinstance(x, StringVal) or isinstance(x, BoolVal):
            return ir.Constant(x.value)
        # 此处左值只可能是变量，因此可以直接调用store_name
        elif isinstance(x, AssignVal):
            value = self.transpile(x.value)
            lhs = self.store_name_(x.var)
            return ir.MAssign(lhs, value)
        elif isinstance(x, UnaryOp):
            op = unaryop_indices[x.op]
            operand = self.transpile(x.right)
            return ir.MUnaryOp(operand=operand, op=op)
        elif isinstance(x, Return):
            value = self.transpile(x.body)
            return ir.MReturn(value)
        elif isinstance(x, Block):
            xs : list[ir.MIR] = []
            for item in x.body:
                xs.append(self.transpile(item))
            return ir.MBlock(suite=xs)
        elif isinstance(x, WhileBlock):
            cond = self.transpile(x.cond)
            body = []
            for item in x.body.body:
                body.append(self.transpile(item))
            body_block = ir.MBlock(body)
            return ir.MWhile(cond=cond, body=body_block)
        elif isinstance(x, IfBlock):
            cond = self.transpile(x.cond)
            body = []
            else_body = []
            for item in x.body.body:
                body.append(self.transpile(item))
            body_block = ir.MBlock(body)
            for item in x.else_body.body:
                else_body.append(self.transpile(item))
            else_block = ir.MBlock(else_body)
            return ir.MIf(cond=cond, body=body_block, else_body=else_block)
        elif isinstance(x, CallFunc):
            func = self.transpile(x.func)
            args = []
            # CallFunc的参数为实参: list[LC] 要继续转换
            for item in x.args:
                arg = self.transpile(item)
                args.append(arg)
            return ir.MCall(func=func, args=args)
        # ★函数定义：创建新的transpiler对象对function内部进行一一转换
        # 1. 创建新的transpiler并将当前scope作为其parent scope
        # 2. 调用before_transpile函数，获取当前func的scope
        # 3. 对于函数体中的每条语句进行转换
        # 4. 创建fptr用于记录函数的信息
        # 5. 利用load_deference判断当前func内部的free来自上层的free还是local并记录其位置
        # 6. 利用4、5得到的信息，得到转换的TrFuncDef
        # 7. 将funcName作为左值进行存储，并完成赋值操作，右值为6得到的TrFuncDef
        elif isinstance(x, NamedFunc):
            transpiler = Transpiler(self.souce_code, self.scope)
            transpiler.before_transpile(x.body, x.arg)
            xs = []
            for item in x.body.body:
                xs.append(transpiler.transpile(item))
            block = ir.MBlock(xs)
            fptr = transpiler.create_fptr_builder(block, x.name)
            freelots = []
            for item in transpiler.scope.free_vars:
                freelots.append(self.load_derefence(item))
            func_body = ir.MFuncDef(fptr=fptr, freeslots=freelots)
            lhs = self.store_name_(x.name)
            return ir.MAssign(lhs=lhs, rhs=func_body)
        elif isinstance(x, LogicalAnd):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            return ir.MLogicalAnd(left=l, right=r)
        elif isinstance(x, LogicalOr):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            return ir.MLogicalOr(left=l, right=r)
        elif isinstance(x, LogicalNot):
            return ir.MLogicalNot(self.transpile(x.right))
        elif isinstance(x, BinOp):
            l = self.transpile(x.left)
            r = self.transpile(x.right)
            if isinstance(x.op, Var):
                binop = x.op.name
                op = binop_indices[binop]
                return ir.MBinOp(left=l, right=r, op=op)
            else:
                raise Exception
        elif isinstance(x, Var):
            return self.load_name_(x.name)
        elif isinstance(x, Local):
            return ir.Constant(0) #type:ignore
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
    "ne": ir.OpBin.NotEq,
    "gt": ir.OpBin.Gt,
    "lt": ir.OpBin.Lt,
    "ge": ir.OpBin.Ge,
    "le": ir.OpBin.Le,
    "mod": ir.OpBin.Mod
}

unaryop_indices: dict[str, ir.OpUnary] = {
    "inv": ir.OpUnary.INV,
    "not": ir.OpUnary.NOT,
    "neg": ir.OpUnary.NEG,
    "pos": ir.OpUnary.POS,
}


def transpile_test(src: str) -> ir.ModuleSpec:
    x = parser.parse(src)
    x = Return(x)
    top = Transpiler(src, None)
    top.before_transpile(x, [])
    block = top.transpile(x)
    fptr = top.create_fptr_builder(code=block, name="top")
    return ir.ModuleSpec(src, fptr)

