from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required

from taxonomy.views import TaxonList, RankList
from collection.views import AccessionList, ContactList
from garden.views import LocationList, PlantList

from taxonomy.forms import TaxonForm
from collection.forms import VerificationForm, AccessionForm, ContactForm
from garden.forms import PlantForm, LocationForm

# Create your views here.

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
    import collections
    result = collections.OrderedDict()
    query_string = request.GET.get('q')
    if query_string:
        # attempt domain strategy
        try:
            domain, query = [i.strip() for i in query_string.split('=', 1)]
        except:
            # default strategy:
            domain = None
            query = query_string
        for klass in [TaxonList, AccessionList, PlantList, LocationList, ContactList]:
            if domain is not None and not klass.__name__.lower().startswith(domain):
                continue
            partial = [{key: getattr(item, key, None)
                        for key in ['inline', 'infobox_url', 'depending']}
                       for item in klass().run_query(query).all()]
            result[klass.__name__.replace('List', '')] = partial
    return JsonResponse(result)
