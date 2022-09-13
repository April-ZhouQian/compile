from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from numbers import Number
import typing
import typing_extensions


if typing.TYPE_CHECKING:
    import typing_extensions

    class TraffyIR(typing_extensions.Protocol):
        pass

    class TraffyLHS(typing_extensions.Protocol):
        pass

else:
    TraffyIR = object
    TraffyLHS = object
@dataclass
class TrNumber:
    value: Number

@dataclass
class TrStr:
    value: str

@dataclass
class TrBool:
    value: bool

if typing.TYPE_CHECKING:
    TrObject = TrNumber | TrStr | TrBool  # type: ignore
else:
    TrObject =(TrNumber, TrStr, TrBool)

@dataclass
class Constant:
    obj: TrObject

@dataclass
class TrBlock:
    suite: list[TraffyIR]

@dataclass
class TrAssign:
    lhs: TraffyLHS
    rhs: TraffyIR

@dataclass
class NamedFunc:
    name: str
    arg: list[str]
    suite: list[TraffyIR]

@dataclass
class TrIf:
    cond: TraffyIR
    body: TraffyIR
    else_body: TraffyIR

@dataclass
class TrWhile:
    cond: TraffyIR
    body: TraffyIR

@dataclass
class TrReturn:
    value: TraffyIR

@dataclass
class TrCall:
    func: TraffyIR
    args: list[TraffyIR]

class OpUnary(IntEnum):
    INV = 0
    NOT = 1
    NEG = 2
    POS = 3

class OpBin(IntEnum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    Eq = 4
    NotEq = 5
    Lt = 6
    Gt = 7
    Le = 8
    Ge = 9
@dataclass
class TrBinOp:
    left: TraffyIR
    right: TraffyIR
    op: OpBin

@dataclass
class TrUnaryOp:
    right: TraffyIR
    op: OpUnary

@dataclass
class FreeVar(TraffyIR):
    slot: int

@dataclass
class LocalVar(TraffyIR):
    slot: int


@dataclass
class StoreLocal(TraffyLHS):
    slot: int

@dataclass
class StoreFree(TraffyLHS):
    slot: int

@dataclass
class TrLogicalAnd:
    left: TraffyIR
    right: TraffyIR

@dataclass
class TrLogicalOr:
    left: TraffyIR
    right: TraffyIR

@dataclass
class TrLogicalNot:
    operand: TraffyIR
#todo
@dataclass
class Metadata(object):
    localnames: list[str]
    freenames: list[str]
    codename: str
    sourceCode: None


@dataclass
class TrFuncPtr(object):
    code: TraffyIR
    metadata: Metadata

@dataclass
class TrFuncDef(TraffyIR):
    fptr: TrFuncPtr
    freeslots: list[int]


@dataclass
class ModuleSpec:
    sourceCode: str
    fptr: TrFuncPtr