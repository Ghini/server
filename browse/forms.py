from django.forms import ModelForm

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)

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
        fields = '__all__'

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
