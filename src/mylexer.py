reserved_keywords = (
    'IF', 'THEN', 'ELSE', 
    'WHILE', 'DO', 'TRUE', 'FALSE',
    'LET', 'IN', 'FUN', 'REF', 
)

tokens = reserved_keywords + (
    'VAR', 'NUM', 'LPAREN', 'RPAREN', 'ARROW',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'ASSIGN',
    'SEMI', 'EQEQ', 'NOTEQ', 'EQ', 'GT', 'GE', 
    'LBRACE', 'RBRACE', 'LT', 'LE', 'BANG',
)

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_BANG = r'!'
t_ARROW = r'->'
t_ASSIGN = r':='
t_SEMI = r';'
t_EQEQ = r'=='
t_NOTEQ = r'!='
t_EQ = r'='
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

reserved_map = {}
for r in reserved_keywords:
    reserved_map[r.lower()] = r


def t_NUM(t):
    r'\-*\d+'
    t.value = int(t.value)
    return t


def t_VAR(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, 'VAR')
    return t


def t_error(t):
    print(("Illegal character '%s'" % t.value[0]))
    t.lexer.skip(1)
