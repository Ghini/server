from django.db import models
from django.urls import reverse

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
    def twolines(self):
        return {'item': self.inline,
                'side': '{0} alive in {1} plant groups'.format(self.plants.count(), sum(p.quantity for p in self.plants.all())),
                'sub': '(Location)'}

    @property
    def infobox_url(self):
        return reverse('location-infobox', args=[self.code])

    def depending_objects(self):
        return {'Plant': self.plants}


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
    def twolines(self):
        return {'item': '{}.{}'.format(self.accession.code, self.code),
                'side': '{0.quantity} alive in {0.location.inline}'.format(self),
                'sub': format(self.accession.taxon.show())}

    @property
    def infobox_url(self):
        return reverse('plant-infobox', args=[self.accession.code, self.code])

    def depending_objects(self):
        return {}


class LocationPlanner(models.Model):
    accession = models.ForeignKey(Accession, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_done = models.DateField(blank=True)
    plant = models.ForeignKey(Plant, null=True, blank=True, on_delete=models.SET_NULL)
