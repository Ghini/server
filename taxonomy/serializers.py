from rest_framework import serializers
from .models import Taxon, Rank

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'

class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = '__all__'
