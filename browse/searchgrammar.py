import ply.yacc as yacc

from taxonomy.models import Taxon, Rank
from collection.models import Accession, Contact, Verification
from garden.models import Location, Plant
from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList, VerificationList
from garden.views import LocationList, PlantList

from django.db.models import F  # used where forcing field for intersection

# Get the token map from the lexer.  This is required.
from .searchlex import tokens

import logging
logger = logging.getLogger(__name__)

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


def p_single_field_query(p):
    'query : domain DOT fieldname operator value'
    result, domain, dot, fieldname, operator, value = p
    queryset = domain.objects.filter(**{'{}__{}'.format(fieldname, operator): value})
    p[0] = {domain.__name__: queryset}
    logger.debug('field: %s' % [i for i in p])


def p_domain_query(p):
    'query : domain EQ value'
    # TODO: should accept and use 'operator', not just EQ
    result, domain, operator, value = p
    queryset = list_views[domain]().run_query(value).all()
    p[0] = {domain.__name__: queryset}
    logger.debug('domain: %s' % [i for i in p])

def p_depending_query(p):
    'query : query PIPE DEPEND'
    result = {}
    for key, qs in p[1].items():
        for item in qs.all():
            result.update(item.depending_objects())
    p[0] = result

def p_terms_and_query(p):
    'query : terms'
    import collections
    result = collections.OrderedDict()
    for domain in [Taxon, Accession, Plant, Location, Contact]:
        partials = [list_views[domain]().run_query(i, order=(len(p[1])==1)) for i in p[1]]
        partial = partials.pop()
        while partials:
            partial = partial.intersection(partials.pop())
        result[domain.__name__] = partial
    p[0] = result
    logger.debug('most generic: %s' % [i for i in p])

def p_terms_or_query(p):
    'query : OR terms'
    import collections
    result = collections.OrderedDict()
    for domain in [Taxon, Accession, Plant, Location, Contact]:
        partials = [list_views[domain]().run_query(i, order=(len(p[1])==1)) for i in p[2]]
        partial = partials.pop()
        while partials:
            partial = partial.union(partials.pop())
        result[domain.__name__] = partial
    p[0] = result
    logger.debug('most generic: %s' % [i for i in p])

def p_sqlike_query(p):
    'query : domain WHERE expression'
    result, domain, _, query_set = p
    p[0] = {domain.__name__: query_set.distinct()}
    logger.debug('most specific: %s' % [i for i in p])

def p_domain_word(p):
    'domain : WORD'
    logger.debug('seen domain {0}'.format(p[1]))
    p.parser.search_domain = classes.get(p[1].lower())
    p[0] = p.parser.search_domain

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
    p[0] = p.parser.search_domain.objects.difference(p[2])

def p_bfactor_expression(p):
    'bfactor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_bfactor_false(p):
    'bfactor : FALSE'
    p[0] = p.parser.search_domain.objects.none()

def p_bfactor_true(p):
    'bfactor : TRUE'
    p[0] = p.parser.search_domain.objects.all()

def p_bfactor_is_not_null(p):
    'bfactor : field NE NULL'
    result, field, operator, value = p
    p[0] = p.parser.search_domain.objects.filter(**{'{}__isnull'.format(field): False})

def p_bfactor_is_null(p):
    'bfactor : field EQ NULL'
    result, field, operator, value = p
    p[0] = p.parser.search_domain.objects.filter(**{'{}__isnull'.format(field): True})

def p_bfactor_comparison(p):
    'bfactor : field operator value'
    result, field, operator, value = p
    p[0] = p.parser.search_domain.objects.filter(**{'{}__{}'.format(field, operator): value})

def p_bfactor_aggregate_comparison(p):
    'bfactor : aggregate LPAREN field RPAREN operator value'
    from django.db.models import Count, Sum, Value  # adding field to qs
    result, aggregate, _, field, _, operator, value = p
    f = {'count': Count, 'sum': Sum}[aggregate]
    q = p.parser.search_domain.objects.annotate(temp_field=f(field) or Value(0))
    q = q.filter(**{'temp_field__{}'.format(operator): value})
    q = q.only('id', field, 'temp_field')
    matching = set(i['id'] for i in q.values('id'))
    p[0] = p.parser.search_domain.objects.filter(id__in=matching)

def p_valuelist_value(p):
    'valuelist : value'
    p[0] = [p[1]]

def p_valuelist_valuelist_value(p):
    'valuelist : valuelist value'
    p[0] = p[1]
    p[0].append(p[2])

def p_bfactor_list_comprehension(p):
    'bfactor : field IN LBRACKET valuelist RBRACKET'
    result, field, _, _, value, _ = p
    p[0] = p.parser.search_domain.objects.filter(**{'{}__in'.format(field): value})

def p_bfactor_not_list_comprehension(p):
    'bfactor : field NOT IN LBRACKET valuelist RBRACKET'
    result, field, _, _, _, value, _ = p
    p[0] = p.parser.search_domain.objects.exclude(**{'{}__in'.format(field): value})

def p_bfactor_between(p):
    'bfactor : field BETWEEN value AND value'
    result, field, _, min_value, _, max_value = p
    p[0] = p.parser.search_domain.objects.filter(**{'{}__range'.format(field): (min_value, max_value)})

def p_field_fieldname(p):
    'field : fieldname'
    p[0] = p[1]
    logger.debug('fieldname {} is used as field starter'.format(p[1]))

def p_field_dot_fieldname(p):
    'field : field DOT fieldname'
    p[0] = '{}__{}'.format(p[1], p[3])
    logger.debug('composing field {}'.format(p[0]))

def p_aggregate_count(p):
    'aggregate : COUNT'
    p[0] = 'count'

def p_aggregate_sum(p):
    'aggregate : SUM'
    p[0] = 'sum'

def p_operator_like(p):
    'operator : LIKE'
    p[0] = 'iexact'

def p_operator_contains(p):
    'operator : CONTAINS'
    p[0] = 'icontains'

def p_operator_equals(p):
    'operator : EQ'
    p[0] = 'exact'

def p_operator_not_equals(p):
    'operator : NE'
    p[0] = 'ne'

def p_operator_less_than(p):
    'operator : LT'
    p[0] = 'lt'

def p_operator_less_equals(p):
    'operator : LE'
    p[0] = 'lte'

def p_operator_greater_than(p):
    'operator : GT'
    p[0] = 'gt'

def p_operator_greater_equals(p):
    'operator : GE'
    p[0] = 'gte'

def p_terms_value(p):
    'terms : value'
    p[0] = [p[1]]

def p_terms_terms_value(p):
    'terms : terms value'
    p[0] = p[1]
    p[0].append(p[2])

def p_value_number(p):
    'value : INTEGER'
    p[0] = p[1]

def p_value_word(p):
    'value : WORD'
    p[0] = p[1]

def p_value_quoted(p):
    'value : QUOTED'
    p[0] = p[1]

def p_value_squoted(p):
    'value : SQUOTED'
    p[0] = p[1]

def p_value_reserved_and(p):
    'value : AND'
    p[0] = p[1]

def p_value_reserved_or(p):
    'value : OR'
    p[0] = p[1]

def p_value_reserved_not(p):
    'value : NOT'
    p[0] = p[1]

def p_value_reserved_sum(p):
    'value : SUM'
    p[0] = p[1]

def p_value_reserved_count(p):
    'value : COUNT'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(token):
    if token is not None:
        print("Line %s, illegal token %s" % (token.lineno, token.value))
    else:
        print('Unexpected end of input')

# Build the parser

def parse(string):
    from .searchlex import get_lexer
    parser = yacc.yacc()
    lexer = get_lexer()
    return parser.parse(string, lexer=lexer)
