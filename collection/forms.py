from django import forms
from django.http import JsonResponse

from django_select2 import forms as s2forms

from taxonomy.models import Taxon
from .models import Verification, Accession, Contact


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = ['level', 'accession', 'taxon', 'qualifier', 'contact', 'date']
        widgets = {
            'accession': s2forms.ModelSelect2Widget(model=Accession,
                                                    search_fields=['code__icontains'],
                                                    max_results=120),
            'taxon': s2forms.ModelSelect2Widget(model=Taxon,
                                                search_fields=['epithet__icontains'],
                                                minimum_input_length=3,
                                                max_results=120),
            'contact': s2forms.ModelSelect2Widget(model=Contact,
                                                  search_fields=['name__icontains']),
            'qualifier': s2forms.Select2Widget,
            'level': s2forms.Select2Widget,
        }

    @classmethod
    def as_view(cls):
        def view(request, accession_code, seq=None):
            if seq is not None:
                obj = Verification.objects.get(accession__code=accession_code, seq=seq)
                return JsonResponse({'form': "%s" % VerificationForm(instance=obj)})
            acc = Accession.objects.get(code=accession_code)
            obj = Verification(accession=acc)
            return JsonResponse({'form': "%s" % VerificationForm(instance=obj)})
        return view


class AccessionForm(forms.ModelForm):
    class Meta:
        model = Accession
        fields = ['code', 'received_quantity', 'received_type', 'source', 'accessioned_date', 'received_date', ]
        widgets = {
            'source': s2forms.ModelSelect2Widget(model=Contact,
                                                 search_fields=['name__icontains']),
            'received_type': s2forms.Select2Widget,
        }

    @classmethod
    def as_view(cls):
        def view(request, code=None):
            if code is not None:
                obj = Accession.objects.get(code=code)
                return JsonResponse({'form': "%s" % AccessionForm(instance=obj)})
            return JsonResponse({'form': "%s" % AccessionForm()})
        return view


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    @classmethod
    def as_view(cls):
        def view(request, pk=None):
            if pk is not None:
                obj = Contact.objects.get(pk=pk)
                return JsonResponse({'form': "%s" % ContactForm(instance=obj)})
            return JsonResponse({'form': "%s" % ContactForm()})
        return view
