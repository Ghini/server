from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList
from garden.views import LocationList, PlantList

from taxonomy.forms import TaxonForm
from collection.forms import VerificationForm, AccessionForm, ContactForm
from garden.forms import PlantForm, LocationForm

# Create your views here.

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
