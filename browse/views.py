from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response

from taxonomy.forms import TaxonForm
from collection.forms import VerificationForm, AccessionForm, ContactForm
from garden.forms import PlantForm, LocationForm


## implement the __ne  custom lookup, for `!=`
# BEGIN
from django.db.models.fields import Field
from django.db.models import Lookup

@Field.register_lookup
class NotEqualLookup(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params
# END

# Create your views here.


class GetDependingObjects:
    def get(self, request, *args, **kwargs):
        from django.core import serializers
        result = {}
        qs = self.get_queryset()
        o = qs.first()
        for key, values in o.depending_objects().items():
            if not values:
                continue
            converted = [{key: getattr(item, key, None)
                          for key in ['inline', 'infobox_url']}
                         for item in values.all()]
            if converted:
                result[key] = converted
        return Response(result, status=status.HTTP_200_OK)


@login_required
@requires_csrf_token
def index(request):
    verification_form = VerificationForm()
    taxon_form = TaxonForm()
    contact_form = ContactForm()
    plant_form = PlantForm()
    accession_form = AccessionForm()
    location_form = LocationForm()

    return render(request, 'index.html', {'taxon_form': taxon_form,
                                          'contact_form': contact_form,
                                          'plant_form': plant_form,
                                          'accession_form': accession_form,
                                          'location_form': location_form,
                                          'verification_form': verification_form, })

def count_json(request):
    '''this view returns the count of a query'''
    from .searchgrammar import parser
    query_string = request.GET.get('q')
    result = parser.parse(query_string)
    total = 0
    for key, qs in result.items():
        total += qs.count()
    return JsonResponse({'count': total})


def filter_json(request):
    '''this view computes the search query results

    it looks for patterns in the query string and runs the corresponding
    search strategy.

    <DOMAIN>.<field> <op> <TERM>
    <DOMAIN> <op> <TERM>
    <TERMS>
    <DOMAIN> where <COMPLEX-QUERY>

    each can have a trailing '|depending'.

    '''
    from .searchgrammar import parser
    query_string = request.GET.get('q')
    result = parser.parse(query_string)
    for key, qs in result.items():
        converted = [{key: getattr(item, key, None)
                      for key in ['inline', 'infobox_url']}
                     for item in qs.all()]
        result[key] = converted
    return JsonResponse(result)


queued_queries = {}

def get_filter_tokens(request):
    import uuid
    from .searchgrammar import parser
    query_string = request.GET.get('q')
    result = parser.parse(query_string)
    for key, qs in result.items():
        if qs.count():
            uuid = str(uuid.uuid4())
            queued_queries[uuid] = (item for item in qs.all())
        result[key] = uuid
    return JsonResponse(result)


def pay_token(request, token):
    content = []
    result = {'done': False,
              'chunk': content}
    try:
        iqs = queued_queries[token]
        for i in range(50):
            item = next(iqs)
            content.append({key: getattr(item, key, None)
                            for key in ['inline', 'infobox_url']})
    except StopIteration:
        del queued_queries[token]
        result['done'] = True
    except KeyError:
        pass
    return JsonResponse(result)
