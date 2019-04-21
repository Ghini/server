from django.db import models

from taxonomy.models import Taxon
from collection.models import Accession

# Create your models here.

class Location(models.Model):
    code = models.CharField(null=False, max_length=8)
    name = models.CharField(null=True, max_length=64)
    description = models.TextField(null=True)

class Plant(models.Model):
    accession = models.ForeignKey(Accession, related_name="plants", on_delete=models.PROTECT)

class LocationPlanner(models.Model):
    accession = models.ForeignKey(Accession, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_done = models.DateField()
    plant = models.ForeignKey(Plant, null=True, on_delete=models.SET_NULL)
