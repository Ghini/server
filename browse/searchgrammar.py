import ply.yacc as yacc

from taxonomy.models import Taxon, Rank
from collection.models import Accession, Contact, Verification
from garden.models import Location, Plant
from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList, VerificationList
from garden.views import LocationList, PlantList

# Get the token map from the lexer.  This is required.
from .searchlex import tokens

# a reminder
''' <DOMAIN>.<field> <op> <TERM>
    <DOMAIN> <op> <TERM>
    <TERMS>
    <DOMAIN> where <COMPLEX-QUERY>
'''


classes = {'taxon': Taxon,
           'rank': Rank,
           'accession': Accession,
           'contact': Contact,
           'verification': Verification,
           'location': Location,
           'plant': Plant
}

list_views = {Taxon: TaxonList,
              Rank: RankList,
              Accession: AccessionList,
              Contact: ContactList,
              Verification: VerificationList,
              Location: LocationList,
              Plant: PlantList,
}

search_domain = None


def p_single_field_query(p):
    'query : domain DOT fieldname operator value'
    result, domain, dot, fieldname, operator, value = p
    queryset = domain.objects.filter(**{'{}__{}'.format(fieldname, operator): value})
    p[0] = {domain.__class__.__name__: queryset}
    print('field', [i for i in p])


def p_domain_query(p):
    'query : domain operator value'
    result, domain, operator, value = p
    queryset = list_views[domain]().run_query(value).all()  # should use 'operator'
    p[0] = {domain.__name__: queryset}
    print('domain', [i for i in p])

def p_depending_query(p):
    'query : query PIPE DEPEND'
    result = {}
    for key, qs in p[1].items():
        for item in qs.all():
            result.update(item.depending_objects())
    p[0] = result
    print([i for i in p])

def p_terms_query(p):
    'query : terms'
    import collections
    result = collections.OrderedDict()
    for domain in [Taxon, Accession, Plant, Location, Contact]:
        partial = list_views[domain]().run_query(p[1][0])  # should use all terms
        result[domain.__name__] = partial
    p[0] = result
    print('most generic', [i for i in p])

def p_sqlike_query(p):
    'query : domain WHERE expression'
    result, domain, _, query_set = p
    p[0] = {domain.__name__: query_set}
    print('most specific', [i for i in p])

def p_domain_word(p):
    'domain : WORD'
    print('seen domain {0}'.format(p[1]))
    global search_domain
    search_domain = classes.get(p[1].lower())
    p[0] = search_domain

def p_fieldname_word(p):
    'fieldname : WORD'
    p[0] = p[1].lower()

def p_expression_bterm(p):
    'expression : bterm'
    p[0] = p[1]

def p_expression_or_bterm(p):
    'expression : expression OR bterm'
    p[0] = p[1].union(p[3])

def p_bterm_bfactor(p):
    'bterm : bfactor'
    p[0] = p[1]

def p_bterm_and_bfactor(p):
    'bterm : bterm AND bfactor'
    p[0] = p[1].intersection(p[3])

def p_bfactor_not_factor(p):
    'bfactor : NOT bfactor'
    p[0] = search_domain.objects.difference(p[2])

def p_bfactor_expression(p):
    'bfactor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_bfactor_comparison(p):
    'bfactor : field operator value'
    result, field, operator, value = p
    p[0] = search_domain.objects.filter(**{'{}__{}'.format(field, operator): value})
    print([i for i in p])

def p_bfactor_between(p):
    'bfactor : field BETWEEN value AND value'
    result, field, _, min_value, _, max_value = p
    p[0] = search_domain.objects.filter(**{'{}__lte'.format(field): max_value,
                                           '{}__gte'.format(field): min_value})
    print([i for i in p])

def p_field_fieldname(p):
    'field : fieldname'
    p[0] = p[1]
    print('fieldname {} is used as field starter'.format(p[1]))

def p_field_dot_fieldname(p):
    'field : field DOT fieldname'
    p[0] = '{}__{}'.format(p[1], p[3])
    print('composing field {}'.format(p[0]))

def p_operator_like(p):
    'operator : LIKE'
    p[0] = 'iexact'
    print([i for i in p])

def p_operator_contains(p):
    'operator : CONTAINS'
    p[0] = 'icontains'
    print([i for i in p])

def p_operator_equals(p):
    'operator : EQ'
    p[0] = 'exact'
    print([i for i in p])

def p_operator_not_equals(p):
    'operator : NE'
    p[0] = 'ne'
    print([i for i in p])

def p_operator_less_than(p):
    'operator : LT'
    p[0] = 'lt'
    print([i for i in p])

def p_operator_less_equals(p):
    'operator : LE'
    p[0] = 'lte'
    print([i for i in p])

def p_operator_greater_than(p):
    'operator : GT'
    p[0] = 'gt'
    print([i for i in p])

def p_operator_greater_equals(p):
    'operator : GE'
    p[0] = 'gte'
    print([i for i in p])

def p_terms_value(p):
    'terms : value'
    p[0] = [p[1]]
    print([i for i in p])

def p_terms_terms_value(p):
    'terms : terms value'
    p[0] = p[1]
    p[0].append(p[2])
    print([i for i in p])

def p_value_number(p):
    'value : INTEGER'
    p[0] = p[1]
    print([i for i in p])

def p_value_word(p):
    'value : WORD'
    p[0] = p[1]
    print([i for i in p])

def p_value_quoted(p):
    'value : QUOTED'
    p[0] = p[1]
    print([i for i in p])

def p_value_reserved_and(p):
    'value : AND'
    p[0] = p[1]
    print([i for i in p])

def p_value_reserved_or(p):
    'value : OR'
    p[0] = p[1]
    print([i for i in p])

def p_value_reserved_not(p):
    'value : NOT'
    p[0] = p[1]
    print([i for i in p])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input on token {0.type}, {0.value}".format(p))

# Build the parser
parser = yacc.yacc()
