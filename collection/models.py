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


class Contact(models.Model):
    name = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.name

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return "/collection/contacts/%s" % self.pk


class Accession(models.Model):
    taxa = models.ManyToManyField(Taxon, through='Verification', related_name='accessions')

    code = models.CharField(max_length=12, unique=True)

    accessioned_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    received_quantity = models.IntegerField(blank=False, default=1)
    received_type = models.CharField(blank=True, null=True, max_length=4, choices=recvd_type_values)
    intended_locations = models.ManyToManyField('garden.Location', through='garden.LocationPlanner',
                                                related_name='planned_accessions')

    source = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def taxon(self):
        if len(self.verifications.all()) == 1:
            return self.taxa[0]
        elif len(self.verifications.all()) == 0:
            None
        else:
            return []

    @property
    def qualifier(self):
        if len(self.verifications.all()) == 1:
            return self.verifications[0].qualifier
        elif len(self.verifications.all()) == 0:
            None
        else:
            return []

    @property
    def best_verification(self):
        if self.verifications.all():
            return self.verifications.order_by('-level').all()[0]
        else:
            return None

    def __str__(self):
        if self.verifications.all():
            best_verification = self.verifications.order_by('-level').all()[0]
            return "{} ({})".format(self.code, best_verification.taxon.show())
        else:
            return self.code

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return "/collection/accessions/%s" % self.code


VERIFICATION_LEVELS = (
    ('0', 'The name of the record has not been checked by any authority.'),
    ('1', 'The name of the record determined by comparison with other named plants.'),
    ('2', 'The name of the record determined by a taxonomist or by other competent persons using herbarium and/or library and/or documented living material.'),
    ('3', 'The name of the plant determined by taxonomist engaged in systematic revision of the group.'),
    ('4', 'The record is part of type gathering or propagated from type material by asexual methods'),
    )


class Verification(models.Model):
    accession = models.ForeignKey(Accession, blank=False, related_name='verifications', on_delete=models.CASCADE)
    taxon = models.ForeignKey(Taxon, blank=False, related_name='verifications', on_delete=models.PROTECT)
    qualifier = models.CharField(blank=True, null=True, max_length=8, choices=QUALIFIERS)
    code = models.IntegerField()
    level = models.CharField(blank=False, null=False, max_length=1, choices=VERIFICATION_LEVELS, default='0')
    contact = models.ForeignKey(Contact, blank=False, related_name='verifications', on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)

    def __str__(self):
        return "{} says {} is a {} - level {}".format(self.contact.name, self.accession.code, self.taxon.show(), self.level)
        
    class Meta:
        unique_together = (('accession', 'code'),
        )

    @property
    def inline(self):
        return "%s" % self
