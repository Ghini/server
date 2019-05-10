#!/bin/env python

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from searchlex import tokens

# a reminder
''' <DOMAIN>.<field> <op> <TERM>
    <DOMAIN> <op> <TERM>
    <TERMS>
    <DOMAIN> where <COMPLEX-QUERY>

tokens = (
    'INTEGER',
    'WORD',
    'QUOTED',
    'DOT',
    'EQUALS',
    'LIKE',
    'CONTAINS',
    'WHERE',
    'PIPE',
    'DEPEND',
)
'''

def p_single_field_query(p):
    'query : WORD DOT WORD operator string'
    print('single-field', [i for i in p])

def p_domain_query(p):
    'query : WORD operator string'
    print('any field', [i for i in p])

def p_terms_query(p):
    'query : terms'
    print('most generic', [i for i in p])

def p_sqlike_query(p):
    'query : WORD WHERE expression'
    print('most generic', [i for i in p])

def p_depending_query(p):
    'query : query PIPE DEPEND'
    print([i for i in p])

def p_expression_term(p):
    'expression : term'
    
def p_expression_or_term(p):
    'expression : expression OR term'

def p_term_factor(p):
    'term : factor'
    
def p_term_and_factor(p):
    'term : term AND factor'

def p_expression_to_factor(p):
    'factor : LPAREN expression RPAREN'

def p_field_comparison(p):
    'factor : WORD operator string'
    
def p_operator_like(p):
    'operator : LIKE'
    p[0] = p[1]
    print([i for i in p])

def p_operator_contains(p):
    'operator : CONTAINS'
    p[0] = p[1]
    print([i for i in p])

def p_operator_equals(p):
    'operator : EQ'
    p[0] = p[1]
    print([i for i in p])

def p_operator_not_equals(p):
    'operator : NE'
    p[0] = p[1]
    print([i for i in p])

def p_operator_less_than(p):
    'operator : LT'
    p[0] = p[1]
    print([i for i in p])

def p_operator_less_equals(p):
    'operator : LE'
    p[0] = p[1]
    print([i for i in p])

def p_operator_greater_than(p):
    'operator : GT'
    p[0] = p[1]
    print([i for i in p])

def p_operator_greater_equals(p):
    'operator : GE'
    p[0] = p[1]
    print([i for i in p])

def p_terms_single(p):
    'terms : string'
    print([i for i in p])
    p[0] = [p[1]]

def p_terms_queue(p):
    'terms : terms string'
    p[0] = p[1]
    p[0].append(p[2])
    print([i for i in p])

def p_term_number(p):
    'string : INTEGER'
    p[0] = p[1]
    print([i for i in p])

def p_term_word(p):
    'string : WORD'
    p[0] = p[1]
    print([i for i in p])

def p_term_quoted(p):
    'string : QUOTED'
    p[0] = p[1]
    print([i for i in p])
    
# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s:
       continue
   result = parser.parse(s)
   print(result)
