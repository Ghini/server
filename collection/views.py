from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .models import Accession, Contact, Verification
from .serializers import AccessionSerializer, ContactSerializer, VerificationSerializer
from taxonomy.views import RequestLoginOnNonSafeMixin
from browse.views import GetDependingObjects

# Create your views here.

class AccessionList(RequestLoginOnNonSafeMixin, generics.ListCreateAPIView):
    lookup_field = 'code'
    queryset = Accession.objects.all()
    serializer_class = AccessionSerializer

    def run_query(self, q):
        return self.get_queryset().filter(code__contains=q).order_by('code')


class AccessionDetail(RequestLoginOnNonSafeMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'code'
    serializer_class = AccessionSerializer

    def get_queryset(self):
        queryset = Accession.objects.filter(code=self.kwargs['code'])
        return queryset


class AccessionMarkup(AccessionDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        o = qs.first()
        result = {'inline': o.inline,}
        return Response(result, status=status.HTTP_200_OK)


class AccessionDepending(GetDependingObjects, AccessionDetail):
    pass


class AccessionInfobox(AccessionDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        obj = qs.first()
        if obj:
            serializer = AccessionSerializer(instance=obj)
            import collections
            result = collections.OrderedDict()
            result['__class_name__'] = 'Accession'
            result['__detail_url__'] = reverse('accession-detail', args=[obj.code])
            result['__shows_as__'] = "%s" % obj
            result['code'] = obj.code
            result['taxa'] = ('link',
                              ", ".join(["{} ({})".format(i.show(), i.family) for i in obj.taxa.all()]),
                              ", ".join([i.epithet for i in obj.taxa.all()]), )
            result['received_quantity'] = obj.received_quantity
            if obj.source is not None:
                result['source'] = "%s" % obj.source
            if obj.received_type:
                result['received_type'] = obj.get_received_type_display()
            result['plant groups'] = obj.plants.count()
            result['living plants'] = sum(p.quantity for p in obj.plants.all())
            for key, value in serializer.data.items():
                if key == 'id':
                    continue
                result.setdefault(key, value)

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_204_NO_CONTENT)


class ContactList(RequestLoginOnNonSafeMixin, generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def run_query(self, q):
        return self.get_queryset().filter(name__icontains=q).order_by('name')


class ContactDetail(RequestLoginOnNonSafeMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactInfobox(ContactDetail):
    pass


class ContactDepending(GetDependingObjects, ContactDetail):
    pass


class ContactMarkup(ContactDetail):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        o = qs.first()
        result = {'inline': o.inline, }
        return Response(result, status=status.HTTP_200_OK)


class VerificationList(generics.ListCreateAPIView):
    @method_decorator(login_required)
    def post(self, request, accession_code):
        from collection.models import Accession
        accession = Accession.objects.filter(code=accession_code).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['accession'] = accession.pk
        if 'seq' not in data:
            from django.db import models
            max_seq = (Verification.objects
                       .filter(accession=accession)
                       .aggregate(max_seq=models.Max('seq')))['max_seq']
            data['seq'] = (max_seq or 0) + 1
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


class VerificationDetail(RequestLoginOnNonSafeMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'seq'

    def get_queryset(self):
        from collection.models import Accession
        accession = Accession.objects.filter(code=self.kwargs['accession_code']).first()
        if accession is None:
            return Response({'code': self.kwargs['accession_code'],
                             "detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        queryset = Verification.objects.filter(accession=accession)
        return queryset

    serializer_class = VerificationSerializer
