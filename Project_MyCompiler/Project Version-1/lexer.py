import ply.lex as lex
import ply.yacc as yacc

# Lexer (Tokens)
tokens = (
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'SEMI',
    'LT', 'GT',
    'AGAR', 'WARNA', 'JABTAK', 'CHHAPO'
)


reserved = {
    'agar': 'AGAR',     # 'if' in Romanized Hindi
    'warna': 'WARNA',  # 'else' in Romanized Hindi
    'jabtak': 'JABTAK', # 'while' in Romanized Hindi
    'chhapo': 'CHHAPO' # 'print' in Romanized Hindi
}

# Regular expressions for tokens
t_EQUALS = r'='
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_GT = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

# Ignore spaces and tabs
t_ignore = ' \t'

# Rule for ID (variable names)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Use Romanized Hindi keywords here
    return t

# Rule for numbers (integers)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Rule for newline characters
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Lexer initialization
lexer = lex.lex()
