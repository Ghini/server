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

    def run_query(self, q):
        return self.get_queryset().filter(epithet__contains=q).order_by('rank', 'epithet')


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
                result['parent'] = ('link', "%s" % obj.parent,
                                    "taxon where epithet={0.epithet} and rank.name={0.rank.name}".format(obj.parent))
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
        result = {'inline': o.inline,}
        return Response(result, status=status.HTTP_200_OK)


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
