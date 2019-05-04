from django.forms import ModelForm
from django import forms
from django_select2 import forms as s2forms
# HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
# ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget, Select2Widget


from taxonomy.models import Taxon
from collection.models import Accession, Contact, Verification
from garden.models import Location, Plant


class TaxonForm(ModelForm):
    class Meta:
        model = Taxon
        fields = ['epithet', 'rank']


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

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class AccessionForm(ModelForm):
    class Meta:
        model = Accession
        fields = '__all__'

class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
