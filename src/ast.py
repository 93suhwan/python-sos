class AST:
    pass


class Lambda(AST):
    """lambda abstraction
    syntax: fun var -> exp
    """
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp


class App(AST):
    """lambda application
    syntax: left_exp right_exp
    """
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class BinOp(AST):
    """binary operation
    left_exp (iop | bop) right_exp
    """
    def __init__(self, left_exp, op, right_exp):
        self.left_exp = left_exp
        self.op = op
        self.right_exp = right_exp


class LetIn(AST):
    """local variable declaration
    let var = exp in body
    """
    def __init__(self, var, exp, body):
        self.var = var
        self.exp = exp
        self.body = body


class If(AST):
    """conditional expression
    if cond then exp1 else exp2
    """
    def __init__(self, cond, exp1, exp2):
        self.cond = cond
        self.exp1 = exp1
        self.exp2 = exp2


class While(AST):
    """while loop
    while cond do block
    """
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class Ref(AST):
    """memory allocation
    ref exp
    """
    def __init__(self, exp):
        self.exp = exp


class Bang(AST):
    """memory dereference
    ! exp
    """
    def __init__(self, exp):
        self.exp = exp


class Assign(AST):
    """assignment expression
    left_exp := right_exp
    """
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class Seq(AST):
    """sequence expression
    left_exp ; right_exp
    """
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class Num(AST):
    """integer expression"""
    def __init__(self, num):
        self.value = num


class Bool(AST):
    """boolean expression"""
    def __init__(self, bvalue):
        self.value = bvalue


class Loc(AST):
    """location"""
    def __init__(self, loc):
        self.value = loc


class Skip(AST):
    """skip"""
    pass


class Var(AST):
    """variable"""
    def __init__(self, var_name):
        self.name = var_name
