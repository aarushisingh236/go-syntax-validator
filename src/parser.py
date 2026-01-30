import ply.yacc as yacc
from lexer import tokens
from ast_nodes import ASTNode

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
)

def p_program(p):
    'program : statement_list'
    p[0] = ASTNode("Program", children=p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_statement(p):
    '''statement : var_declaration
                 | assignment
                 | ifelse
                 | forloop
                 | switch_stmt
                 | return_stmt'''
    p[0] = p[1]

def p_var_declaration(p):
    'var_declaration : VAR ID ASSIGN expression'
    p[0] = ASTNode("VarDecl", p[2], [p[4]])

def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = ASTNode("Assign", p[1], [p[3]])

def p_ifelse(p):
    '''ifelse : IF condition block
              | IF condition block ELSE block'''
    if len(p) == 4:
        p[0] = ASTNode("If", children=[p[2], p[3]])
    else:
        p[0] = ASTNode("IfElse", children=[p[2], p[3], p[5]])

def p_forloop(p):
    'forloop : FOR condition block'
    p[0] = ASTNode("ForLoop", children=[p[2], p[3]])

# -------- SWITCH FIX --------
def p_switch_stmt(p):
    'switch_stmt : SWITCH expression LBRACE case_list RBRACE'
    p[0] = ASTNode("Switch", children=[
        p[2],
        ASTNode("Cases", children=p[4])
    ])

def p_case_list(p):
    '''case_list : case_stmt
                 | case_stmt case_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_case_stmt(p):
    '''case_stmt : CASE expression COLON block
                 | DEFAULT COLON block'''
    if p[1] == 'default':
        p[0] = ASTNode("DefaultCase", children=[p[3]])
    else:
        p[0] = ASTNode("Case", children=[p[2], p[4]])
# ----------------------------

def p_return_stmt(p):
    'return_stmt : RETURN expression'
    p[0] = ASTNode("Return", children=[p[2]])

def p_condition(p):
    '''condition : expression LT expression
                 | expression GT expression
                 | expression EQ expression'''
    p[0] = ASTNode("BinaryOp", p[2], [p[1], p[3]])

def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = ASTNode("Block", children=p[2])

def p_expression(p):
    '''expression : NUMBER
                  | ID
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if len(p) == 2:
        p[0] = ASTNode("Literal", p[1])
    else:
        p[0] = ASTNode("BinaryOp", p[2], [p[1], p[3]])

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' line {p.lineno}")
    else:
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()

def parse_code(code):
    return parser.parse(code)