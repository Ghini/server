from django.shortcuts import render
from rest_framework import generics, viewsets, views

from .models import Plant
from .serializers import PlantSerializer

# Create your views here.

class Plants(generics.ListCreateAPIView):
    def get_queryset(self):
        print(self.kwargs)
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession:
            queryset = Plant.objects.filter(accession__code=self.kwargs['accession_code'])
        else:
            queryset = Plant.objects.filter(accession__code=self.kwargs['accession_code'])
        return queryset

    serializer_class = PlantSerializer

