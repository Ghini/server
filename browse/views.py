from django.db import models
from django.shortcuts import render
from django.http import JsonResponse

from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList
from garden.views import LocationList, PlantList


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def filter_json(request):
    import collections
    result = collections.OrderedDict()
    for klass in [TaxonList, AccessionList, PlantList, LocationList]:
        partial = [{key: getattr(item, key, None)
                    for key in ['inline', 'infobox_url', 'depending']}
                   for item in klass().run_query(request.GET.get('q')).all()]
        result[klass.__name__] = partial
    return JsonResponse(result)
