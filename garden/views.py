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

    def run_query(self, q):
        return Plant.objects.filter(accession__code__contains=q).all()

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
            result['accession'] = ('link', "%s" % obj.accession, obj.accession.code)
            result['location'] = ('link', "%s" % obj.location, 'location=%s' % obj.location.code)
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)


class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def run_query(self, q):
        return self.get_queryset().filter(name__contains=q).all()


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    serializer_class = LocationSerializer
    def get_queryset(self):
        queryset = Location.objects.filter(code=self.kwargs['code'])
        return queryset


class LocationInfobox(LocationDetail):
    pass
