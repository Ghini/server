from taxonomy.models import Taxon, Rank
from collection.models import Accession, Contact, Verification
from garden.models import Location, Plant
from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList, VerificationList
from garden.views import LocationList, PlantList

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


import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from .searchlex import tokens

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


def p_query_as_serialized(p):
    'serialized : query'
    import collections
    result = collections.OrderedDict()
    for key, qs in p[1].items():
        converted = [{key: getattr(item, key, None)
                      for key in ['inline', 'infobox_url', 'depending']}
                     for item in qs.all()]
        result[key] = converted
    p[0] = result


def p_single_field_query(p):
    'query : domain DOT fieldname operator string'
    result, domain, dot, fieldname, operator, string = p
    queryset = domain.objects.filter(**{'{}__i{}'.format(fieldname, operator): string})
    p[0] = {domain.__class__.__name__: queryset}
    print('field', [i for i in p])


def p_domain_query(p):
    'query : domain operator string'
    result, domain, operator, string = p
    queryset = list_views[domain]().run_query(string).all()  # should use 'operator'
    p[0] = {domain.__name__: queryset}
    print('domain', [i for i in p])

def p_depending_query(p):
    'query : query PIPE DEPEND'
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
    print('most specific', [i for i in p])

def p_word_as_domain(p):
    'domain : WORD'
    p[0] = classes.get(p[1].lower())

def p_word_as_fieldname(p):
    'fieldname : WORD'
    p[0] = p[1].lower()

def p_term_as_expression(p):
    'expression : term'

def p_expression_or_term(p):
    'expression : expression OR term'

def p_factor_as_term(p):
    'term : factor'

def p_term_and_factor(p):
    'term : term AND factor'

def p_expression_to_factor(p):
    'factor : LPAREN expression RPAREN'

def p_field_comparison(p):
    'factor : WORD operator string'

def p_operator_like(p):
    'operator : LIKE'
    p[0] = 'i' + p[1]
    print([i for i in p])

def p_operator_contains(p):
    'operator : CONTAINS'
    p[0] = 'i' + p[1]
    print([i for i in p])

def p_operator_equals(p):
    'operator : EQ'
    p[0] = 'exact'
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
