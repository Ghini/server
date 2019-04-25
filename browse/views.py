from django.db import models
from django.shortcuts import render
from django.http import JsonResponse

from taxonomy.models import Taxon, Rank
from collection.models import Accession, Contact
from garden.models import Location, Plant


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def filter_json(request):
    # TODO: how to represent filter criteria
    result = {}
    for klass in [Accession, Taxon, Plant]:
        partial = [{key: getattr(item, key, None)
                    for key in ['inline', 'infobox_url', 'depending']}
                   for item in klass.objects.all()]
        result[klass.__name__] = partial
    return JsonResponse(result)
