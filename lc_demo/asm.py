from dataclasses import dataclass
from enum import IntEnum
from numbers import Number
import typing

if not typing.TYPE_CHECKING:
    class MIR:
        pass
    class MLHS:
        pass
else:
    from .asm import StoreFree, StoreLocal, StoreGlobal
    MLHS = (StoreLocal | StoreFree | StoreGlobal) # type: ignore
    from .asm import Constant, MBlock, MAssign, MIf, MWhile, MReturn, MCall, MBinOp, MUnaryOp, FreeVar, LocalVar, GlobalVar, MLogicalAnd, MLogicalOr, MLogicalNot, MFuncDef
    MIR = Constant | MBlock | MAssign | MIf | MWhile | MReturn | MCall | MBinOp | MUnaryOp | FreeVar | LocalVar | GlobalVar | MLogicalAnd | MLogicalOr | MLogicalNot | MFuncDef # type: ignore


@dataclass
class MNumber(object):
    value: Number

@dataclass
class MStr(object):
    value: str

@dataclass
class MBool(object):
    value: bool

if typing.TYPE_CHECKING:
    from .mfunc import MFunc
    MObject = Number| str | bool | None | MFunc  # type: ignore
else:
    MObject = object

@dataclass
class Constant:
    obj: MObject

@dataclass
class MBlock:
    suite: list[MIR]

@dataclass
class MAssign:
    lhs: MLHS
    rhs: MIR

@dataclass
class MIf:
    cond: MIR
    body: MIR
    else_body: MIR

@dataclass
class MWhile:
    cond: MIR
    body: MIR

@dataclass
class MReturn:
    value: MIR

@dataclass
class MCall:
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
    Mod = 10
@dataclass
class MBinOp:
    left: MIR
    right: MIR
    op: OpBin

@dataclass
class MUnaryOp:
    operand: MIR
    op: OpUnary

@dataclass
class FreeVar:
    slot: int

@dataclass
class LocalVar:
    slot: int

@dataclass
class GlobalVar:
    name: MObject

@dataclass
class StoreLocal:
    slot: int

@dataclass
class StoreFree:
    slot: int

@dataclass
class StoreGlobal:
    name: MObject

@dataclass
class MLogicalAnd:
    left: MIR
    right: MIR

@dataclass
class MLogicalOr:
    left: MIR
    right: MIR

@dataclass
class MLogicalNot:
    operand: MIR

@dataclass
class Metadata(object):
    localnames: list[str]
    freenames: list[str]
    codename: str
    sourceCode: None

@dataclass
class MFuncPtr(object):
    code: MIR
    metadata: Metadata

@dataclass
class MFuncDef:
    fptr: MFuncPtr
    freeslots: list[int]

@dataclass(frozen=True)
class ModuleSpec:
    sourceCode: str
    fptr: MFuncPtr

def return_globals():
    return globals()