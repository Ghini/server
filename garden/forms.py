from django import forms
from django.http import JsonResponse
from django_select2 import forms as s2forms
from leaflet.forms.widgets import LeafletWidget

from collection.models import Accession
from .models import Location, Plant


class LocationForm(forms.ModelForm):
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


class PlantForm(forms.ModelForm):

    class Meta:
        model = Plant
        fields = '__all__'
        widgets = {
            'location': s2forms.ModelSelect2Widget(model=Location,
                                                   search_fields=['name__icontains', 'code__icontains']),
            'accession': s2forms.ModelSelect2Widget(model=Accession,
                                                    search_fields=['code__icontains']),
            'geometry': LeafletWidget(attrs={'loadevent': ''}),
        }

    @classmethod
    def as_view(cls):
        def view(request, accession_code, code=None):
            if code is not None:
                obj = Plant.objects.get(accession__code=accession_code, code=code)
            else:
                acc = Accession.objects.get(code=accession_code)
                obj = Plant(accession=acc)
            form = PlantForm(instance=obj)
            return JsonResponse({'form': form.as_table()})
        return view
