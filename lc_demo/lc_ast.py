from __future__ import annotations
from dataclasses import dataclass
from numbers import Number
import typing
import typing_extensions


@dataclass(frozen=True)
class NamedFunc:
    name: str
    arg: list[str]
    body: Block


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class BoolVal:
    value: bool


@dataclass(frozen=True)
class NumberVal:
    value: Number


@dataclass(frozen=True)
class StringVal:
    value: str


@dataclass(frozen=True)
class AssignVal:
    var: str
    value: LC


@dataclass(frozen=True)
class Block:
    body: list[LC]


@dataclass(frozen=True)
class IfBlock:
    cond: LC
    body: Block
    else_body: Block


@dataclass(frozen=True)
class WhileBlock:
    cond: LC
    body: Block


@dataclass(frozen=True)
class Return:
    body: LC


@dataclass(frozen=True)
class CallFunc:
    func: LC
    arg: list[LC]


@dataclass(frozen=True)
class BinOp:
    left: LC
    right: LC
    op: LC


@dataclass(frozen=True)
class UnaryOp:
    right: LC
    op: typing.Literal["neg", "pos", "not"]


@dataclass(frozen=True)
class LogicalOr:
    left: LC
    right: LC

@dataclass(frozen=True)
class LogicalAnd:
    left: LC
    right: LC


@dataclass(frozen=True)
class LogicalNot:
    right: LC


if typing.TYPE_CHECKING:
    LC = Var | NumberVal | BoolVal | StringVal | AssignVal | Block | NamedFunc | IfBlock | WhileBlock | Return | CallFunc | BinOp | UnaryOp | LogicalOr | LogicalAnd | LogicalNot  # type: ignore
else:
    LC = (
        Var,
        NumberVal,
        BoolVal,
        StringVal,
        AssignVal,
        Block,
        NamedFunc,
        IfBlock,
        WhileBlock,
        Return,
        CallFunc,
        BinOp,
        UnaryOp,
        LogicalOr,
        LogicalAnd,
        LogicalNot,
    )


@dataclass
class State:
    scope: typing.Dict[str, typing.Any]
    is_returning: bool


def eval_lc(S: State, syntactic_structure: LC) -> tuple[typing.Any, State]:
    if isinstance(syntactic_structure, Var):
        return S.scope[syntactic_structure.name], S
    elif isinstance(syntactic_structure, BoolVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, StringVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, NumberVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, NamedFunc):

        def rf(S_star: State, r_star):
            arg = syntactic_structure.arg
            S1 = State({**S.scope}, S.is_returning)
            r1 = None
            gap = len(r_star) - len(arg)
            if gap > 0:
                raise Exception(
                    "Error in parameter list: "
                    + str(gap)
                    + " more parameters were transmitted"
                )
            elif gap < 0:
                raise Exception(
                    "Error in parameter list: Missing " + str(-gap) + " parameters"
                )
            else:
                for index in range(len(arg)):
                    S1 = State({**S1.scope, arg[index]: r_star[index]}, S1.is_returning)
                r1, S1 = eval_lc(S1, syntactic_structure.body)
                return r1, S_star

        name = syntactic_structure.name
        if name != "":
            S = State({**S.scope, name: rf}, S.is_returning)
        return rf, S
    elif isinstance(syntactic_structure, AssignVal):
        value = eval_lc(S, syntactic_structure.value)[0]
        S_New = State({**S.scope, syntactic_structure.var: value}, S.is_returning)
        return value, S_New
    elif isinstance(syntactic_structure, Block):
        r = None
        for item in syntactic_structure.body:
            if S.is_returning == False:
                r, S = eval_lc(S, item)
            else:
                break
        return r, S
    elif isinstance(syntactic_structure, IfBlock):
        r, S = eval_lc(S, syntactic_structure.cond)
        r1 = None
        if r:
            r1, S = eval_lc(S, syntactic_structure.body)
        else:
            r1, S = eval_lc(S, syntactic_structure.else_body)
        return r1, S
    elif isinstance(syntactic_structure, WhileBlock):
        r1 = None
        r, S = eval_lc(S, syntactic_structure.cond)
        while r:
            r1, S = eval_lc(S, syntactic_structure.body)
            r, S = eval_lc(S, syntactic_structure.cond)
        return r1, S
    elif isinstance(syntactic_structure, Return):
        r, S = eval_lc(S, syntactic_structure.body)
        S_New = State({**S.scope}, True)
        return r, S_New
    elif isinstance(syntactic_structure, CallFunc):
        rf, S1 = eval_lc(S, syntactic_structure.func)
        arg = syntactic_structure.arg
        r = []
        S2 = State({**S1.scope}, S1.is_returning)
        for index in range(len(arg)):
            r1, S2 = eval_lc(S1, arg[index])
            r.append(r1)
        r2, S3 = rf(S2, r)
        return r2, S3
    elif isinstance(syntactic_structure, BinOp):
        arg = []
        left, S = eval_lc(S, syntactic_structure.left)
        arg.append(left)
        right, S = eval_lc(S, syntactic_structure.right)
        arg.append(right)
        rf, S1 = eval_lc(S, syntactic_structure.op)
        r, S2 = rf(S1, arg)
        return r, S2
    elif isinstance(syntactic_structure, UnaryOp):
        right, S = eval_lc(S, syntactic_structure.right)
        if syntactic_structure.op == "pos":
            return right, S
        elif syntactic_structure.op == "neg":
            return -right, S
        elif syntactic_structure.op == "not":
            return not right, S
        typing_extensions.assert_never(syntactic_structure.op)
    elif isinstance(syntactic_structure, LogicalOr):
        left, S = eval_lc(S, syntactic_structure.left)
        if left:
            return True, S
        right, S = eval_lc(S, syntactic_structure.right)
        return right, S
    elif isinstance(syntactic_structure, LogicalAnd):
        left, S = eval_lc(S, syntactic_structure.left)
        if not left:
            return False, S
        right, S = eval_lc(S, syntactic_structure.right)
        return right, S
    elif isinstance(syntactic_structure, LogicalNot):
        right, S = eval_lc(S, syntactic_structure.right)
        return not right, S
    if typing.TYPE_CHECKING:
        typing_extensions.assert_never(syntactic_structure)
    else:
        raise TypeError(syntactic_structure)
