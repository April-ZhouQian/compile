from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from numbers import Number
import typing
import typing_extensions

if not typing.TYPE_CHECKING:
    class MIR:
        pass
    class MLHS:
        pass
else:
    from .asm import StoreFree, StoreLocal
    MLHS = (StoreLocal| StoreFree) # type: ignore
    from .asm import Constant, TrBlock, TrAssign, NamedFunc, TrIf, TrWhile, TrReturn, TrCall, TrBinOp, TrUnaryOp, FreeVar, LocalVar, TrLogicalAnd, TrLogicalOr, TrLogicalNot, TrFuncDef
    MIR = (Constant | TrBlock | TrAssign | NamedFunc | TrIf | TrWhile | TrReturn | TrCall | TrBinOp | TrUnaryOp | FreeVar | LocalVar | TrLogicalAnd | TrLogicalOr | TrLogicalNot | TrFuncDef) # type: ignore


@dataclass
class TrNumber(object):
    value: Number

@dataclass
class TrStr(object):
    value: str

@dataclass
class TrBool(object):
    value: bool

if typing.TYPE_CHECKING:
    TrObject = Number| str | bool # type: ignore
else:
    TrObject = (Number, str, bool)

@dataclass
class Constant:
    obj: TrObject

@dataclass
class TrBlock:
    suite: list[MIR]

@dataclass
class TrAssign:
    lhs: MLHS
    rhs: MIR

# @dataclass
# class NamedFunc:
#     name: str
#     arg: list[str]
#     suite: list[MIR]

@dataclass
class TrIf:
    cond: MIR
    body: MIR
    else_body: MIR

@dataclass
class TrWhile:
    cond: MIR
    body: MIR

@dataclass
class TrReturn:
    value: MIR

@dataclass
class TrCall:
    func: MIR
    args: list[MIR]

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
    left: MIR
    right: MIR
    op: OpBin

@dataclass
class TrUnaryOp:
    operand: MIR
    op: OpUnary

@dataclass
class FreeVar:
    slot: int

@dataclass
class LocalVar:
    slot: int


@dataclass
class StoreLocal:
    slot: int

@dataclass
class StoreFree:
    slot: int

@dataclass
class TrLogicalAnd:
    left: MIR
    right: MIR

@dataclass
class TrLogicalOr:
    left: MIR
    right: MIR

@dataclass
class TrLogicalNot:
    operand: MIR
#todo
@dataclass
class Metadata(object):
    localnames: list[str]
    freenames: list[str]
    codename: str
    sourceCode: None


@dataclass
class TrFuncPtr(object):
    code: MIR
    metadata: Metadata

@dataclass
class TrFuncDef:
    fptr: TrFuncPtr
    freeslots: list[int]


@dataclass
class ModuleSpec:
    sourceCode: str
    fptr: TrFuncPtr

