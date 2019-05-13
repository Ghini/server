import ply.lex as lex

''' <DOMAIN>.<field> <op> <TERM>
    <DOMAIN> <op> <TERM>
    <TERMS>
    <DOMAIN> where <COMPLEX-QUERY>
'''

reserved = {
    'like' : 'LIKE',
    'where' : 'WHERE',
    'contains': 'CONTAINS',
    'depending': 'DEPEND',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'between': 'BETWEEN',
}

tokens = [
    'PIPE',
    'INTEGER', 'QUOTED', 'WORD',
    'DOT',
    'LPAREN', 'RPAREN',
    'LE', 'LT', 'GE', 'GT', 'EQ', 'NE',
] + list(reserved.values())

def t_WORD(t):  # covers WORD and reserved word tokens
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.lower() in reserved:
        # alter type if meeting a reserved word
        t.value = t.value.lower()
        t.type = reserved[t.value]
    return t

t_EQ       = r'='
t_NE       = r'!='
t_LT       = r'<'
t_LE       = r'<='
t_GT       = r'>'
t_GE       = r'>='

t_DOT      = r'\.'
t_PIPE     = r'\|'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_QUOTED(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

## other optional or needed elements ##

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
