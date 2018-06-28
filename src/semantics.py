from ast import *
from visitor import NodeVisitor
from substitution import Substitution

#import sys
#sys.setrecursionlimit(10000)


class Eval(NodeVisitor):
    """big-step operational semantics"""
    def __init__(self, ast, memory):
        self.ast = ast
        self.memory = memory
        self.loc_count = 0

    def visit_Lambda(self, node):
        return node

    def visit_App(self, node):
        m1 = self.visit(node.left_exp)
        if not isinstance(m1, Lambda):
            raise TypeError
        m2 = self.visit(node.right_exp)
        sub = Substitution(m2, m1.var)
        return self.visit(sub.subst(m1.exp))

    def visit_BinOp(self, node):
        m1 = self.visit(node.left_exp)
        m2 = self.visit(node.right_exp)
        op = node.op
        if not isinstance(m1, Num) or not isinstance(m2, Num):
            raise TypeError
        if op == '+':
            return Num(m1.value + m2.value)
        elif op == '-':
            return Num(m1.value - m2.value)
        elif op == '*':
            return Num(m1.value * m2.value)
        elif op == '/':
            return Num(m1.value / m2.value)
        elif op == '==':
            return Bool(m1.value == m2.value)
        elif op == '!=':
            return Bool(m1.value != m2.value)
        elif op == '>':
            return Bool(m1.value > m2.value)
        elif op == '>=':
            return Bool(m1.value >= m2.value)
        elif op == '<':
            return Bool(m1.value < m2.value)
        elif op == '<=':
            return Bool(m1.value <= m2.value)

    def visit_LetIn(self, node):
        sub = Substitution(self.visit(node.exp), node.var)
        return self.visit(sub.subst(node.body))

    def visit_If(self, node):
        bvalue = self.visit(node.cond)
        if not isinstance(bvalue, Bool):
            raise TypeError
        if bvalue.value:
            return self.visit(node.exp1)
        else:
            return self.visit(node.exp2)

    def visit_While(self, node):
        bvalue = self.visit(node.cond)
        if not isinstance(bvalue, Bool):
            raise TypeError
        if bvalue.value:
            self.visit(node.block)
            self.visit(node)
        return Skip()

    def visit_Ref(self, node):
        value = self.visit(node.exp)
        if not (type(value) == Num):
            raise TypeError
        # location is of the following form: l0, l1, l2, ...
        loc = Loc('l' + str(self.loc_count))
        self.loc_count += 1
        self.memory.insert(loc, value)
        return loc

    def visit_Bang(self, node):
        loc = self.visit(node.exp)
        if not isinstance(loc, Loc):
            raise TypeError
        return self.memory.lookup(loc)

    def visit_Assign(self, node):
        m1 = self.visit(node.left_exp)
        if not isinstance(m1, Loc):
            raise TypeError
        m2 = self.visit(node.right_exp)
        if not (type(m2) == Num):
            raise TypeError
        self.memory.insert(m1, m2)
        return Skip()

    def visit_Seq(self, node):
        if not isinstance(self.visit(node.left_exp), Skip):
            raise TypeError
        return self.visit(node.right_exp)

    def visit_Num(self, node):
        return node

    def visit_Bool(self, node):
        return node

    def visit_Loc(self, node):
        return node

    def visit_Skip(self, node):
        return node

    def eval(self):
        return self.visit(self.ast)


class Stuck(Exception):
    """to represent a state that cannot be further reduced in the small-step semantics"""
    def __init__(self):
        pass


class Step(NodeVisitor):
    """Small-step operational semantics"""
    def __init__(self, ast, memory):
        self.ast = ast
        self.memory = memory
        self.loc_count = 0

    def visit_Lambda(self, node):
        raise Stuck

    def visit_App(self, node):
        m1 = node.left_exp
        m2 = node.right_exp
        try:
            return App(self.visit(m1), m2)
        except Stuck:
            if not isinstance(m1, Lambda):
                raise TypeError
            try:
                return App(m1, self.visit(m2))
            except Stuck:
                sub = Substitution(m2, m1.var)
                return sub.subst(m1.exp)

    def visit_BinOp(self, node):
        m1 = node.left_exp
        m2 = node.right_exp
        op = node.op
        try:
            return BinOp(self.visit(m1), op, m2)
        except Stuck:
            try:
                return BinOp(m1, op, self.visit(m2))
            except Stuck:
                if not isinstance(m1, Num) or not isinstance(m2, Num):
                    raise TypeError
                if op == '+':
                    return Num(m1.value + m2.value)
                elif op == '-':
                    return Num(m1.value - m2.value)
                elif op == '*':
                    return Num(m1.value * m2.value)
                elif op == '/':
                    return Num(m1.value / m2.value)
                elif op == '==':
                    return Bool(m1.value == m2.value)
                elif op == '!=':
                    return Bool(m1.value != m2.value)
                elif op == '>':
                    return Bool(m2.value > m2.value)
                elif op == '>=':
                    return Bool(m1.value >= m2.value)
                elif op == '<':
                    return Bool(m1.value < m2.value)
                elif op == '<=':
                    return Bool(m1.value <= m2.value)

    def visit_LetIn(self, node):
        try:
            return LetIn(node.var, self.visit(node.exp), node.body)
        except Stuck:
            sub = Substitution(node.exp, node.var)
            return sub.subst(node.body)

    def visit_If(self, node):
        try:
            return If(self.visit(node.cond), node.exp1, node.exp2)
        except Stuck:
            bvalue = node.cond
            if not isinstance(bvalue, Bool):
                raise TypeError
            if bvalue.value:
                return self.visit(node.exp1)
            else:
                return self.visit(node.exp2)

    def visit_While(self, node):
        then_block = Seq(node.block, node)
        return If(node.cond, then_block, Skip())

    def visit_Ref(self, node):
        try:
            return Ref(self.visit(node.exp))
        except Stuck:
            if not isinstance(node.exp, Num):
                raise TypeError
            loc = Loc('l' + str(self.loc_count))
            self.loc_count += 1
            self.memory.insert(loc, node.exp)
            return loc

    def visit_Bang(self, node):
        try:
            return Bang(self.visit(node.exp))
        except Stuck:
            if not isinstance(node.exp, Loc):
                raise TypeError
            return self.memory.lookup(node.exp)

    def visit_Assign(self, node):
        m1 = node.left_exp
        m2 = node.right_exp
        try:
            return Assign(self.visit(m1), m2)
        except Stuck:
            if not isinstance(m1, Loc):
                raise TypeError
            try:
                return Assign(m1, self.visit(m2))
            except Stuck:
                if not isinstance(m2, Num):
                    raise TypeError
                self.memory.insert(m1, m2)
                return Skip()

    def visit_Seq(self, node):
        try:
            return Seq(self.visit(node.left_exp), node.right_exp)
        except Stuck:
            if not isinstance(node.left_exp, Skip):
                raise TypeError
            return self.visit(node.right_exp)

    def visit_Num(self, node):
        raise Stuck

    def visit_Bool(self, node):
        raise Stuck

    def visit_Loc(self, node):
        raise Stuck

    def visit_Skip(self, node):
        raise Stuck

    def multi_step(self, node):
        try:
            return self.multi_step(self.visit(node))
        except Stuck:
            return node

    def eval(self):
        return self.multi_step(self.ast)
