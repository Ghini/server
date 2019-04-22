from django.shortcuts import render
from rest_framework import viewsets
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

