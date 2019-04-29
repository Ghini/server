from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList
from garden.views import LocationList, PlantList


# Create your views here.

@requires_csrf_token
def index(request):
    return render(request, 'index.html', {})

def filter_json(request):
    import collections
    result = collections.OrderedDict()
    query_string = request.GET.get('q')
    if query_string:
        # attempt domain strategy
        try:
            domain, query = query_string.split('=', 1)
        except:
            # default strategy:
            domain = None
            query = query_string
        for klass in [TaxonList, AccessionList, PlantList, LocationList]:
            if domain is not None and not klass.__name__.lower().startswith(domain):
                continue
            partial = [{key: getattr(item, key, None)
                        for key in ['inline', 'infobox_url', 'depending']}
                       for item in klass().run_query(query).all()]
            result[klass.__name__] = partial
    return JsonResponse(result)
