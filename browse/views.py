from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response

import uuid

from taxonomy.forms import TaxonForm
from collection.forms import VerificationForm, AccessionForm, ContactForm
from collection.models import Institution
from garden.forms import PlantForm, LocationForm

import threading

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

queued_queries = {}

def update_expected(token, qs):
    if token in queued_queries:
        print("updating token {} count to {}".format(token, qs.count()))
        queued_queries[token][1] = qs.count()
    else:
        print("can't update token {}".format(token))


# Create your views here.

class GetDependingObjects:
    def get(self, request, *args, **kwargs):
        result = {}
        qs = self.get_queryset()
        o = qs.first()
        for key, qs in o.depending_objects().items():
            if qs.count():
                token = str(uuid.uuid4())
                print("adding token {}".format(token))
                queued_queries[token] = [(item for item in qs.all()), 100000]
                threading.Thread(target=update_expected, args=(token, qs)).start()
                result[key] = token
        return Response(result, status=status.HTTP_200_OK)


class ImagesCarousel:
    def get(self, request, *args, **kwargs):
        result = {}
        qs = self.get_queryset()
        o = qs.first()
        try:
            d = {'object_name': '{}'.format(o),
                 'images': o.images.all(), }
        except:
            d = {'object_name': 'not defining',
                 'images': []}
        return render(request, 'carousel.html', d)


@login_required
@requires_csrf_token
def index(request):
    verification_form = VerificationForm()
    taxon_form = TaxonForm()
    contact_form = ContactForm()
    plant_form = PlantForm()
    accession_form = AccessionForm()
    location_form = LocationForm()
    institution = Institution.objects.first()

    return render(request, 'index.html', {'institution': institution,
                                          'taxon_form': taxon_form,
                                          'contact_form': contact_form,
                                          'plant_form': plant_form,
                                          'accession_form': accession_form,
                                          'location_form': location_form,
                                          'verification_form': verification_form, })

def count_json(request):
    '''this view returns the count of a query'''
    from .searchgrammar import parse
    query_string = request.GET.get('q')
    rectangle = request.GET.get('r')
    geometry = None
    if rectangle:
        try:
            import struct, base64
            xi, yi, xf, yf = struct.unpack('<ffff', base64.b64decode(rectangle))
            from django.contrib.gis.geos import Polygon
            geometry = Polygon(((xi, yi), (xi, yf), (xf, yf), (xf, yi), (xi, yi)))
        except Exception as e:
            print(type(e).__name__, e)
    candidates = parse(query_string, geometry) or {}
    result = {}
    total = 0
    for key, qs in candidates.items():
        this = qs.count()
        total += this
        result[key] = this
    result['__total__'] = total
    return JsonResponse(result)


def filter_json(request):
    '''this view computes the search query results    '''
    from .searchgrammar import parse
    query_string = request.GET.get('q')
    rectangle = request.GET.get('r')
    geometry = None
    if rectangle:
        try:
            import struct, base64
            xi, yi, xf, yf = struct.unpack('<ffff', base64.b64decode(rectangle))
            from django.contrib.gis.geos import Polygon
            geometry = Polygon(((xi, yi), (xi, yf), (xf, yf), (xf, yi), (xi, yi)))
        except Exception as e:
            print(type(e).__name__, e)
    candidates = parse(query_string, geometry) or {}
    result = {}
    for key, qs in candidates.items():
        converted = [{key: getattr(item, key, None)
                      for key in ['inline', 'twolines', 'infobox_url']}
                     for item in qs.all()]
        result[key] = converted
    return JsonResponse(result)


def get_filter_tokens(request):
    from .searchgrammar import parse
    query_string = request.GET.get('q')
    rectangle = request.GET.get('r')
    geometry = None
    if rectangle:
        try:
            import struct, base64
            xi, yi, xf, yf = struct.unpack('<ffff', base64.b64decode(rectangle))
            from django.contrib.gis.geos import Polygon
            geometry = Polygon(((xi, yi), (xi, yf), (xf, yf), (xf, yi), (xi, yi)))
        except Exception as e:
            print(type(e).__name__, e)
    result = {}
    candidates = parse(query_string, geometry) or {}
    for key, qs in candidates.items():
        if qs.count():
            token = str(uuid.uuid4())
            queued_queries[token] = [(item for item in qs.all()), 100000]
            threading.Thread(target=update_expected, args=(token, qs)).start()
            result[key] = token
    return JsonResponse(result)


def serialize(p):
    try:
        return p.coords
    except:
        pass
    try:
        return [i.coords for i in p]
    except:
        pass
    return p


def cash_token(request, token):
    print("cashing token {}, found in {} queue? {}".format(token, len(queued_queries), token in queued_queries))
    content = []
    result = {'done': False,
              'expect': 0,
              'chunk': content}
    try:
        iqs, result['expect'] = queued_queries[token]
        for i in range(20):
            item = next(iqs)
            content.append({key: serialize(getattr(item, key, None))
                            for key in ['inline', 'twolines', 'infobox_url', 'geometries']})
    except StopIteration:
        del queued_queries[token]
        result['done'] = True
    except KeyError:
        pass
    except RuntimeError as e:
        print(type(e).__name__, e)
    return JsonResponse(result)


def drop_token(request, token):
    print("dropping token {}, found in {} queue? {}".format(token, len(queued_queries), token in queued_queries))
    try:
        if token == '__all__':
            print("not dropping anything")
            # queued_queries.clear()
            pass
        else:
            del queued_queries[token]
    except KeyError:
        pass
    return JsonResponse({})
