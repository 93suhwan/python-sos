from mylexer import tokens
from ast import *


def p_program(p):
    """program : exp"""
    p[0] = p[1]


def p_lambda(p):
    """exp : FUN var ARROW exp"""
    p[0] = Lambda(p[2], p[4])


def p_letin(p):
    """exp : LET var EQ exp IN exp"""
    p[0] = LetIn(p[2], p[4], p[6])


def p_statement(p):
    """exp : IF exp THEN exp ELSE exp
           | WHILE exp DO exp
    """
    if len(p) == 7:
        p[0] = If(p[2], p[4], p[6])
    else:
        p[0] = While(p[2], p[4]) 


def p_block(p):
    """exp : LBRACE exp RBRACE"""
    p[0] = p[2]


def p_exp(p):
    """exp : assign_exp SEMI exp
           | assign_exp
    """
    if len(p) == 4:
        p[0] = Seq(p[1], p[3])
    else:
        p[0] = p[1]


def p_assign_exp(p):
    """assign_exp : equal_exp ASSIGN equal_exp
                  | equal_exp
    """
    if len(p) == 4:
        p[0] = Assign(p[1], p[3])
    else:
        p[0] = p[1]


def p_equal_exp(p):
    """equal_exp : equal_exp EQEQ rel_exp
                 | equal_exp NOTEQ rel_exp
                 | rel_exp
    """
    if len(p) == 4:
        p[0] = BinOp(p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_rel_exp(p):
    """rel_exp : rel_exp GT add_exp
               | rel_exp GE add_exp
               | rel_exp LT add_exp
               | rel_exp LE add_exp
               | add_exp
    """
    if len(p) == 4:
        p[0] = BinOp(p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_add_exp(p):
    """add_exp : add_exp PLUS mult_exp
               | add_exp MINUS mult_exp
               | mult_exp
    """
    if len(p) == 4:
        p[0] = BinOp(p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_mult_exp(p):
    """mult_exp : mult_exp MULT prefix_exp
                | mult_exp DIV prefix_exp
                | prefix_exp
    """
    if len(p) == 4:
        p[0] = BinOp(p[1], p[2], p[3])
    else:
        p[0] = p[1]


def p_prefix_exp(p):
    """prefix_exp : BANG prefix_exp
                  | REF prefix_exp
                  | postfix_exp
    """
    if len(p) == 3:
        if p[1] == 'ref':
            p[0] = Ref(p[2])
        else:
            p[0] = Bang(p[2])
    else:
        p[0] = p[1]


def p_postfix_exp(p):
    """postfix_exp : postfix_exp primary
                   | primary
    """
    if len(p) == 3:
        p[0] = App(p[1], p[2])
    else:
        p[0] = p[1]


def p_primary(p):
    """primary : LPAREN exp RPAREN
               | var
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_number(p):
    """primary : NUM"""
    p[0] = Num(p[1])


def p_bool(p):
    """primary : TRUE
               | FALSE
    """
    if p[1] == 'true':
        p[0] = Bool(True)
    else:
        p[0] = Bool(False)


def p_var(p):
    """var : VAR"""
    p[0] = Var(p[1])


def p_error(p):
    """error"""
    print("syntax error!")
