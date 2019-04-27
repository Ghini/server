from django.shortcuts import render
from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .models import Plant, Location
from .serializers import PlantSerializer, LocationSerializer

# Create your views here.

class PlantList(generics.ListCreateAPIView):
    def post(self, request, accession_code):
        from collection.models import Accession
        accession = Accession.objects.filter(code=accession_code).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['accession'] = accession.pk
        serializer = PlantSerializer(data=data)
        if serializer.is_valid():
            plant = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Plant.objects.filter(accession=accession)
        return queryset

    serializer_class = PlantSerializer

class PlantDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Plant.objects.filter(accession=accession, code=self.kwargs['code'])
        return queryset

    serializer_class = PlantSerializer

class PlantInfobox(PlantDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = PlantSerializer(instance=obj)
            result = serializer.data
            del result['id']
            result['accession'] = "%s" % obj.accession
            result['location'] = "%s" % obj.location
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)

class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    serializer_class = LocationSerializer
    def get_queryset(self):
        queryset = Location.objects.filter(code=self.kwargs['code'])
        return queryset
class LocationInfobox(LocationDetail):
    pass
