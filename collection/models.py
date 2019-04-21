from django.db import models

_ = lambda x: x

from taxonomy.models import Taxon

QUALIFIERS = (
    ('aff.', 'aff.'),
    ('cf.', 'cf.'),
    ('forsan', 'forsan'),
    ('near', 'near'),
    ('?', '?',),
    (None, ''),
)
recvd_type_values = (
    ('ALAY', _('Air layer')),
    ('BBPL', _('Balled & burlapped plant')),
    ('BRPL', _('Bare root plant')),
    ('BUDC', _('Bud cutting')),
    ('BUDD', _('Budded')),
    ('BULB', _('Bulb')),
    ('CLUM', _('Clump')),
    ('CORM', _('Corm')),
    ('DIVI', _('Division')),
    ('GRAF', _('Graft')),
    ('LAYE', _('Layer')),
    ('PLNT', _('Planting')),
    ('PSBU', _('Pseudobulb')),
    ('RCUT', _('Rooted cutting')),
    ('RHIZ', _('Rhizome')),
    ('ROOC', _('Root cutting')),
    ('ROOT', _('Root')),
    ('SCIO', _('Scion')),
    ('SEDL', _('Seedling')),
    ('SEED', _('Seed')),
    ('SPOR', _('Spore')),
    ('SPRL', _('Sporeling')),
    ('TUBE', _('Tuber')),
    ('UNKN', _('Unknown')),
    ('URCU', _('Unrooted cutting')),
    ('BBIL', _('Bulbil')),
    ('VEGS', _('Vegetative spreading')),
    ('SCKR', _('Root sucker')),
    (None, ''),
    )

# Create your models here.

class Accession(models.Model):
    taxon = models.ForeignKey(Taxon, related_name='accessions', on_delete=models.PROTECT)
    qualifier = models.CharField(blank=True, null=True, max_length=8, choices=QUALIFIERS)

    accessioned_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    received_quantity = models.IntegerField(blank=False, default=1)
    received_type = models.CharField(blank=True, null=True, max_length=4, choices=recvd_type_values)
    intended_locations = models.ManyToManyField('garden.Location', through='garden.LocationPlanner', related_name='planned_accessions')

    pass


class Contact(models.Model):
    pass

