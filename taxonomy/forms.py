from django import forms
from django.http import JsonResponse

from django_select2 import forms as s2forms

from .models import Taxon


class TaxonForm(forms.ModelForm):
    class Meta:
        model = Taxon
        fields = ['epithet', 'rank', 'authorship', 'year', 'parent', 'accepted']
        widgets = {
            'parent': s2forms.ModelSelect2Widget(model=Taxon,
                                                 search_fields=['epithet__icontains']),
            'accepted': s2forms.ModelSelect2Widget(model=Taxon,
                                                   search_fields=['epithet__icontains']),
            'rank': s2forms.Select2Widget,
        }

    @classmethod
    def as_view(cls):
        def view(request, pk=None):
            if pk is not None:
                obj = Taxon.objects.get(pk=pk)
                return JsonResponse({'form': "%s" % TaxonForm(instance=obj)})
            return JsonResponse({'form': "%s" % TaxonForm()})
        return view
