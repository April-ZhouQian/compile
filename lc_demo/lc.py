# Generated from lark-action.


from lc_demo.lc_ast import *
def append(lst, element):
    lst.append(element)
    return lst

if '_get_location' not in globals(): 
    def _get_location(token):
        return (token.line, token.column)

if '_get_value' not in globals(): 
    def _get_value(token):
        return token.value


from lc_demo.lc_raw import Transformer, Lark_StandAlone, Tree
class lc_Transformer(Transformer):

    def start_0(self, __args):
        return  Block(__args[1-1])
    def lc_0(self, __args):
        return  __args[1-1]
    def lc_1(self, __args):
        return AssignVal(__args[1-1].value, __args[3-1])
    def lc_2(self, __args):
        return  NamedFunc("", __args[3-1], Block(__args[6-1]))
    def lc_3(self, __args):
        return  NamedFunc("", [], Block(__args[5-1]))
    def lc_4(self, __args):
        return  IfBlock(__args[3-1], Block(__args[6-1]), Block([]))
    def lc_5(self, __args):
        return  IfBlock(__args[3-1], Block(__args[6-1]), Block(__args[10-1]))
    def lc_6(self, __args):
        return  WhileBlock(__args[3-1], Block(__args[6-1]))
    def lc_7(self, __args):
        return  Return(__args[2-1])
    def lc_8(self, __args):
        return  NamedFunc(__args[2-1].value, __args[4-1], Block(__args[7-1]))
    def lc_9(self, __args):
        return  NamedFunc(__args[2-1].value, [], Block(__args[6-1]))
    def stmts_0(self, __args):
        return  [__args[1-1]]
    def stmts_1(self, __args):
        return  append(__args[1-1], __args[2-1])
    def call_0(self, __args):
        return  CallFunc(__args[1-1], __args[3-1])
    def call_1(self, __args):
        return  CallFunc(__args[1-1], "")
    def name_0(self, __args):
        return  __args[1-1].value
    def args_0(self, __args):
        return  [__args[1-1]]
    def args_1(self, __args):
        return  append(__args[1-1], __args[3-1])
    def actual_params_0(self, __args):
        return  [__args[1-1]]
    def actual_params_1(self, __args):
        return  append(__args[1-1], __args[3-1])
    def or_0(self, __args):
        return  __args[1-1]
    def or_1(self, __args):
        return  LogicalOr(__args[1-1], __args[3-1])
    def and_0(self, __args):
        return  __args[1-1]
    def and_1(self, __args):
        return  LogicalAnd(__args[1-1], __args[3-1])
    def not_0(self, __args):
        return  __args[1-1]
    def not_1(self, __args):
        return  LogicalNot(__args[2-1])
    def relation_0(self, __args):
        return  __args[1-1]
    def relation_1(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("gt"))
    def relation_2(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("lt"))
    def relation_3(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("ge"))
    def relation_4(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("le"))
    def relation_5(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("eq"))
    def addsub_0(self, __args):
        return  __args[1-1]
    def addsub_1(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("add"))
    def addsub_2(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("sub"))
    def muldiv_0(self, __args):
        return  __args[1-1]
    def muldiv_1(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("mul"))
    def muldiv_2(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("div"))
    def muldiv_3(self, __args):
        return  BinOp(__args[1-1], __args[3-1], Var("mod"))
    def unary_0(self, __args):
        return  __args[1-1]
    def unary_1(self, __args):
        return  UnaryOp(__args[2-1], "pos")
    def unary_2(self, __args):
        return  UnaryOp(__args[2-1], "neg")
    def atom_0(self, __args):
        return  Var(__args[1-1].value)
    def atom_1(self, __args):
        return  NumberVal(eval(__args[1-1].value))
    def atom_2(self, __args):
        return  BoolVal(True)
    def atom_3(self, __args):
        return  BoolVal(False)
    def atom_4(self, __args):
        return  StringVal(eval(__args[1-1].value))
    def atom_5(self, __args):
        return  __args[2-1]
    def atom_6(self, __args):
        return  Block(__args[2-1])
    def atom_7(self, __args):
        return  CallFunc(__args[1-1], __args[3-1])
    def atom_8(self, __args):
        return  CallFunc(__args[1-1], "")


parser = Lark_StandAlone(transformer=lc_Transformer())
