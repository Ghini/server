from django.shortcuts import render
from rest_framework import generics, viewsets, views

from .models import Plant
from .serializers import PlantSerializer

# Create your views here.

class Plants(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Plant.objects.filter(accession__id=self.kwargs['accession_pk'])
        return queryset

    serializer_class = PlantSerializer

