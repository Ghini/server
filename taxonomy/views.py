from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Rank, Taxon
from .serializers import RankSerializer
from .serializers import TaxonSerializer

from browse.views import GetDependingObjects


def organize_by_ranges(id_list):
    '''return singletons and ranges definitions

    this way we can avoid matching 1…500 as 500 elements.
    '''
    import numpy as np
    id_list = np.array(sorted(id_list))
    index = id_list[1:] - id_list[:-1] - 1
    zipped = np.dstack((index, id_list[:-1], id_list[1:]))[0]
    np_todo = zipped[index!=0,:]
    todo = list(np_todo)
    todo.reverse()
    ranges = []
    singletons = []
    bottom = id_list[0]
    while todo:
        _, top, next_bottom = todo.pop()
        if top == bottom:
            singletons.append(top)
        elif top == bottom + 1:
            singletons.append(top)
            singletons.append(bottom)
        else:
            ranges.append((bottom, top))
        bottom = next_bottom
    return (singletons, ranges)


# Create your views here.

def index(request):
    response = "My List of Employees Goes Here"
    return HttpResponse(response)


class RequestLoginOnNonSafeMixin:

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @method_decorator(login_required)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @method_decorator(login_required)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class TaxonList(RequestLoginOnNonSafeMixin, generics.ListCreateAPIView):
    serializer_class = TaxonSerializer
    queryset = Taxon.objects.all()
    class Meta:
        ordering = ['rank', 'epithet']

    def run_query(self, q, order=True):
        result = self.get_queryset().filter(epithet__contains=q)
        if order:
            result = self.order_query(result)
        return result

    def order_query(self, result):
        result = result.order_by('rank', 'epithet')
        return result


class TaxonDetail(RequestLoginOnNonSafeMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaxonSerializer

    def get_queryset(self):
        queryset = Taxon.objects.filter(pk=self.kwargs['pk'])
        return queryset


class TaxonInfobox(TaxonDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = TaxonSerializer(instance=obj)
            result = serializer.data
            result['__class_name__'] = 'Taxon'
            result['__detail_url__'] = reverse('taxon-detail', args=[obj.pk])
            result['__shows_as__'] = "%s" % obj
            for key in ['id', 'epithet', 'authorship']:
                try:
                    del result[key]
                except:
                    pass
            if obj.parent:
                if obj.parent.rank.id < Rank.family_id:
                    result['parent'] = ('link', "%s" % obj.parent,
                                        "taxon where epithet={0.epithet} and rank.name={0.rank.name}".format(obj.parent))
                else:
                    del result['parent']
                    parent = obj.parent
                    while parent and parent.rank.id >= Rank.family_id:
                        result[parent.rank.name] = ('link', "%s" % parent,
                                                    "taxon where epithet={0.epithet} and rank.name={0.rank.name}".format(parent))
                        parent = parent.parent
            if obj.accepted:
                result['accepted'] = ('link', "%s" % obj.accepted,
                                      "taxon where epithet={0.epithet} and rank.name={0.rank.name}".format(obj.accepted))
            if obj.synonyms:
                result['synonyms+'] = ", ".join("%s" % i for i in obj.synonyms.all())
            result['rank'] = "%s" % obj.rank
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)


class TaxonMarkup(TaxonDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        o = qs.first()
        result = {'inline': o.inline,
                  'twolines': o.twolines}
        return Response(result, status=status.HTTP_200_OK)


class TaxonRAC(TaxonDetail):
    def get(self, request, *args, **kwargs):
        import time
        from django.db.models import Count, Sum
        qs = self.get_queryset()
        o = qs.first()
        accession_id_list = []
        import collections
        counts = collections.OrderedDict([('__epithet__', o.epithet),
                                          ('__timer__', -time.time()),
                                          ('accessions', 0),
                                          ('plant groups', 0),
                                          ('living plants', 0)])
        done = set()
        todo = [o]
        while todo:
            o = todo.pop()
            if o.id in done:
                continue
            done.add(o.id)
            if o.accessions:
                for a in o.accessions.all():
                    accession_id_list.append(str(a.id))
                    counts['accessions'] += 1
                    plants_this_accession = a.plants.aggregate(Count('id'), Sum('quantity'))
                    counts['plant groups'] += plants_this_accession['id__count']
                    counts['living plants'] += plants_this_accession['quantity__sum'] or 0
            todo.extend([i for i in o.subtaxa and o.subtaxa.all() or []])
            if o.accepted:
                todo.append(o.accepted)

        if accession_id_list:
            counts['accessions'] = ('link',
                                    counts['accessions'],
                                    'accession where id in [{}]'.format(' '.join(accession_id_list)))

        counts['__timer__'] += time.time()
        return Response(counts, status=status.HTTP_200_OK)
        

class TaxonDepending(GetDependingObjects, TaxonDetail):
    pass


class RankList(RequestLoginOnNonSafeMixin, generics.ListCreateAPIView):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()


class RankDetail(RequestLoginOnNonSafeMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RankSerializer
    def get_queryset(self):
        queryset = Rank.objects.filter(code=self.kwargs['pk'])
        return queryset


class RankInfobox(RankDetail):
    pass
