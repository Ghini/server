from django import forms
from django.http import JsonResponse

from django_select2 import forms as s2forms

from .models import Taxon


class TaxonForm(forms.ModelForm):
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
