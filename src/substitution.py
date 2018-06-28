from ast import *
from visitor import SubVisitor


class Substitution(SubVisitor):
    def __init__(self, value, var):
        self.value = value
        self.var_name = var.name

    def subst_Lambda(self, node):
        if node.var.name == self.var_name:
            return node
        else:
            exp = self.subst(node.exp)
            return Lambda(node.var, exp)

    def subst_App(self, node):
        left_exp = self.subst(node.left_exp)
        right_exp = self.subst(node.right_exp)
        return App(left_exp, right_exp)

    def subst_BinOp(self, node):
        left_exp = self.subst(node.left_exp)
        op = node.op
        right_exp = self.subst(node.right_exp)
        return BinOp(left_exp, op, right_exp)

    def subst_LetIn(self, node):
        var = node.var
        exp = self.subst(node.exp)
        body = self.subst(node.body)
        return LetIn(var, exp, body)

    def subst_If(self, node):
        cond = self.subst(node.cond)
        exp1 = self.subst(node.exp1)
        exp2 = self.subst(node.exp2)
        return If(cond, exp1, exp2)

    def subst_While(self, node):
        cond = self.subst(node.cond)
        block = self.subst(node.block)
        return While(cond, block)

    def subst_Ref(self, node):
        exp = self.subst(node.exp)
        return Ref(exp)

    def subst_Bang(self, node):
        exp = self.subst(node.exp)
        return Bang(exp)

    def subst_Assign(self, node):
        left_exp = self.subst(node.left_exp)
        right_exp = self.subst(node.right_exp)
        return Assign(left_exp, right_exp)

    def subst_Seq(self, node):
        left_exp = self.subst(node.left_exp)
        right_exp = self.subst(node.right_exp)
        return Seq(left_exp, right_exp)

    def subst_Num(self, node):
        return node

    def subst_Bool(self, node):
        return node

    def subst_Loc(self, node):
        return node

    def subst_Skip(self, node):
        return node

    def subst_Var(self, node):
        if node.name == self.var_name:
            return self.value
        else:
            return node
