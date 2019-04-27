from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Rank, Taxon
from .serializers import RankSerializer
from .serializers import TaxonSerializer

# Create your views here.

def index(request):
    response = "My List of Employees Goes Here"
    return HttpResponse(response)

class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer

class TaxonViewSet(viewsets.ModelViewSet):
    queryset = Taxon.objects.all()
    serializer_class = TaxonSerializer


class TaxonInfobox(generics.RetrieveAPIView):
    serializer_class = TaxonSerializer

    def get_queryset(self):
        queryset = Taxon.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = TaxonSerializer(instance=obj)
            result = serializer.data
            del result['id']
            result['parent'] = "%s" % obj.parent
            if obj.accepted:
                result['accepted'] = "%s" % obj.accepted
            if obj.synonyms:
                result['synonyms'] = ", ".join("%s" % i for i in obj.synonyms.all())
            result['rank'] = "%s" % obj.rank
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)
