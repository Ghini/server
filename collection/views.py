from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .models import Accession, Contact, Verification
from .serializers import AccessionSerializer, ContactSerializer, VerificationSerializer

# Create your views here.

class AccessionList(generics.ListCreateAPIView):
    lookup_field = 'code'
    queryset = Accession.objects.all()
    serializer_class = AccessionSerializer

    def run_query(self, q):
        return self.get_queryset().filter(code__contains=q).order_by('code')

class AccessionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    serializer_class = AccessionSerializer

    def get_queryset(self):
        queryset = Accession.objects.filter(code=self.kwargs['code'])
        return queryset


class AccessionInfobox(AccessionDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = AccessionSerializer(instance=obj)
            import collections
            result = collections.OrderedDict()
            result['__class_name__'] = 'Accession'
            result['__detail_url__'] = reverse('accession', kwargs={'code': obj.code})
            result['__shows_as__'] = "%s" % obj
            result.update(serializer.data)
            del result['id']
            result['taxa'] = ('link',
                              ", ".join(["%s" % i for i in obj.taxa.all()]),
                              ", ".join([i.epithet for i in obj.taxa.all()]), )
            result['plant groups'] = sum(p.quantity for p in obj.plants.all())
            result['living plants'] = sum(p.quantity for p in obj.plants.all())
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def run_query(self, q):
        return self.get_queryset().filter(name__contains=q).order_by('name')

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactInfobox(ContactDetail):
    pass

class VerificationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'

    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Verification.objects.filter(accession=accession)
        return queryset

    serializer_class = VerificationSerializer

class VerificationList(generics.ListCreateAPIView):
    def post(self, request, accession_code):
        from collection.models import Accession
        accession = Accession.objects.filter(code=accession_code).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['accession'] = accession.pk
        if 'code' not in data:
            from django.db import models
            max_code = (Verification.objects
                        .filter(accession=accession)
                        .aggregate(max_code=models.Max('code')))['max_code']
            data['code'] = (max_code or 0) + 1
        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            verification = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'ser': serializer.errors, 'dat': data}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Verification.objects.filter(accession=accession)
        return queryset

    serializer_class = VerificationSerializer
