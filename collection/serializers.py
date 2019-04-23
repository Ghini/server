from rest_framework import serializers

from .models import Accession, Contact

class AccessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accession
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

