import ply.lex as lex

tokens = (
    'VAR','RETURN','IF','ELSE','FOR','SWITCH','CASE','DEFAULT',
    'ID','NUMBER',
    'ASSIGN','PLUS','MINUS','TIMES','DIVIDE',
    'LT','GT','EQ',
    'LBRACE','RBRACE','COLON'
)

t_ASSIGN = r'='
t_EQ = r'=='
t_LT = r'<'
t_GT = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'

reserved = {
    'var':'VAR',
    'return':'RETURN',
    'if':'IF',
    'else':'ELSE',
    'for':'FOR',
    'switch':'SWITCH',
    'case':'CASE',
    'default':'DEFAULT'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lineno}")

lexer = lex.lex()