import ply.lex as lex
import ply.yacc as yacc
from assembly_generator import tac_to_assembly

# -------------------
# Lexer
# -------------------
tokens = (
    'ID', 'NUMBER',
    'ASSIGN', 'PLUS', 'LT',
    'SEMI', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'AGAR', 'WARNA', 'CHHAPO', 'JABTAK'
)

t_ASSIGN = r'='
t_PLUS = r'\+'
t_LT = r'<'
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

reserved = {
    'agar': 'AGAR',
    'warna': 'WARNA',
    'chhapo': 'CHHAPO',
    'jabtak': 'JABTAK'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# -------------------
# Parser
# -------------------
precedence = (
    ('left', 'PLUS'),
    ('left', 'LT'),
)

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_assign(p):
    '''statement : ID ASSIGN expression SEMI'''
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    '''statement : CHHAPO expression SEMI'''
    p[0] = ('print', p[2])

def p_statement_if_else(p):
    '''statement : AGAR LPAREN expression RPAREN statement WARNA statement'''
    p[0] = ('if-else', p[3], p[5], p[7])

def p_statement_while(p):
    '''statement : JABTAK LPAREN expression RPAREN statement'''
    p[0] = ('while', p[3], p[5])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression LT expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = p[1]

def p_statement_block(p):
    '''statement : LBRACE statements RBRACE'''
    p[0] = ('block', p[2])

def p_error(p):
    print(f"Syntax error at {p.value}" if p else "Syntax error at EOF")

parser = yacc.yacc()

# -------------------
# TAC Generation
# -------------------
tac_code = []
temp_count = 0
label_count = 0

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def new_label(prefix="L"):
    global label_count
    l = f"{prefix}{label_count}"
    label_count += 1
    return l

def generate_code(node):
    if isinstance(node, list):
        for stmt in node:
            generate_code(stmt)
    elif isinstance(node, tuple):
        if node[0] == 'assign':
            rhs = generate_code(node[2])
            tac_code.append(f"{node[1]} = {rhs}")
        elif node[0] == 'print':
            tac_code.append(f"chhapo {node[1]}")
        elif node[0] == 'binop':
            left = generate_code(node[2])
            right = generate_code(node[3])
            t = new_temp()
            tac_code.append(f"{t} = {left} {node[1]} {right}")
            return t
        elif node[0] == 'if-else':
            cond = generate_code(node[1])
            else_label = new_label("ELSE")
            end_label = new_label("ENDIF")
            tac_code.append(f"agar {cond}:")
            generate_code(node[2])
            tac_code.append(f"warna:")
            generate_code(node[3])
        elif node[0] == 'while':
            cond = generate_code(node[1])
            tac_code.append(f"jabtak {cond}:")
            generate_code(node[2])
        elif node[0] == 'block':
            generate_code(node[1])
    elif isinstance(node, int) or isinstance(node, str):
        return node

# -------------------
# Test Program
# -------------------
input_data = '''
a = 5;
b = 10;
agar (a < b) chhapo a; warna chhapo b;
jabtak (a < b) a = a + 1;
chhapo a;
'''

lexer.input(input_data)
ast = parser.parse(input_data)

print("\nParsed AST:")
print(ast)

print("\nGenerated Three-Address Code:")
generate_code(ast)
for line in tac_code:
    print(line)

# Generate Assembly
print("\nGenerated Assembly Code:")
asm_code = tac_to_assembly(tac_code)
for line in asm_code:
    print(line)

# -------------------
# Write to output.asm for simulator.py
# -------------------
with open("output.asm", "w") as f:
    for line in asm_code:
        f.write(line + "\n")
