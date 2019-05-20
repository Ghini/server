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
            del result['id']
            if obj.parent:
                print(obj, obj.parent)
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
                result['synonyms'] = ", ".join("%s" % i for i in obj.synonyms.all())
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
        import collections
        counts = collections.OrderedDict([('__epithet__', o.epithet),
                                          ('__timer__', -time.time()),
                                          ('accessions', 0),
                                          ('plant groups', 0),
                                          ('plants', 0)])
        done = set()
        todo = [o]
        while todo:
            o = todo.pop()
            if o.id in done:
                continue
            done.add(o.id)
            if o.accessions:
                all_accessions = (o.accessions
                                  .annotate(num_plant_groups=Count('plants'),
                                            num_plants=Sum('plants__quantity'))
                                  .aggregate(Count('id'), Sum('num_plant_groups'), Sum('num_plants')))
                counts['accessions'] += all_accessions['id__count']
                counts['plant groups'] += all_accessions['num_plant_groups__sum'] or 0
                counts['plants'] += all_accessions['num_plants__sum'] or 0
            todo.extend([i for i in o.subtaxa and o.subtaxa.all() or []])
            if o.accepted:
                todo.append(o.accepted)

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
