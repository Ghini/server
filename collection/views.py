from django.shortcuts import render
from rest_framework import generics, viewsets, views

from .models import Accession, Contact
from .serializers import AccessionSerializer, ContactSerializer

# Create your views here.

class AccessionList(generics.ListCreateAPIView):
    lookup_field = 'code'
    queryset = Accession.objects.all()
    serializer_class = AccessionSerializer

class AccessionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    queryset = Accession.objects.all()
    serializer_class = AccessionSerializer

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
