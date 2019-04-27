from django.db import models

from taxonomy.models import Taxon
from collection.models import Accession

# Create your models here.

class Location(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(blank=True, null=True, max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return '{} ({})'.format(self.code, self.name)
        return self.code

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return "/garden/locations/%s/infobox/" % (self.code)


class Plant(models.Model):
    accession = models.ForeignKey(Accession, related_name="plants", blank=False, on_delete=models.PROTECT)
    code = models.CharField(max_length=8, default='1')
    location = models.ForeignKey(Location, related_name="plants", blank=False, on_delete=models.PROTECT)
    quantity = models.IntegerField(blank=False, default=1)

    class Meta:
        unique_together = (('accession', 'code'),
        )

    def __str__(self):
        return '{}.{}'.format(self.accession.code, self.code)

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return "/garden/accessions/%s/plants/%s/infobox/" % (self.accession.code, self.code)


class LocationPlanner(models.Model):
    accession = models.ForeignKey(Accession, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_done = models.DateField(blank=True)
    plant = models.ForeignKey(Plant, null=True, blank=True, on_delete=models.SET_NULL)
