from rest_framework import serializers

from .models import Plant, Location
from taxonomy.models import Taxon
from collection.models import Accession

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

