from django.forms import ModelForm
from django import forms
from django_select2 import forms as s2forms

from django.http import JsonResponse

# HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
# ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget, Select2Widget


from taxonomy.models import Taxon
from collection.models import Accession, Contact, Verification
from garden.models import Location, Plant


class TaxonForm(ModelForm):
    class Meta:
        model = Taxon
        fields = ['epithet', 'rank']

    @classmethod
    def as_view(cls):
        def view(request, pk=None):
            if pk is not None:
                obj = Taxon.objects.get(pk=pk)
                return JsonResponse({'form': "%s" % TaxonForm(instance=obj)})
            return JsonResponse({'form': "%s" % TaxonForm()})
        return view


class VerificationForm(ModelForm):
    class Meta:
        model = Verification
        fields = ['level', 'accession', 'taxon', 'qualifier', 'contact', 'date']
        widgets = {
            'accession': s2forms.ModelSelect2Widget(model=Accession,
                                                    search_fields=['code__icontains'],
                                                    max_results=120,
            ),
            'taxon': s2forms.ModelSelect2Widget(model=Taxon,
                                                search_fields=['epithet__icontains'],
                                                minimum_input_length=3,
                                                max_results=120,
            ),
            'contact': s2forms.ModelSelect2Widget(model=Contact,
                                                  search_fields=['name__icontains'],
            ),
            'qualifier': s2forms.Select2Widget,
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


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

    @classmethod
    def as_view(cls):
        def view(request, code=None):
            if code is not None:
                obj = Location.objects.get(code=code)
                return JsonResponse({'form': "%s" % LocationForm(instance=obj)})
            return JsonResponse({'form': "%s" % LocationForm()})
        return view


class AccessionForm(ModelForm):
    class Meta:
        model = Accession
        fields = '__all__'

    @classmethod
    def as_view(cls):
        def view(request, code=None):
            if code is not None:
                obj = Accession.objects.get(code=code)
                return JsonResponse({'form': "%s" % AccessionForm(instance=obj)})
            return JsonResponse({'form': "%s" % AccessionForm()})
        return view


class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'

    @classmethod
    def as_view(cls):
        def view(request, accession_code, code=None):
            if code is not None:
                obj = Plant.objects.get(accession__code=accession_code, code=code)
                return JsonResponse({'form': "%s" % PlantForm(instance=obj)})
            acc = Accession.objects.get(code=accession_code)
            obj = Plant(accession=acc)
            return JsonResponse({'form': "%s" % PlantForm()})
        return view


class ContactForm(ModelForm):
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

