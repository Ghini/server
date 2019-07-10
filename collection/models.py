from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.fullname

    @property
    def inline(self):
        return "%s" % self

    @property
    def twolines(self):
        return {'item': self.inline, 'side': '', 'sub': ''}

    @property
    def infobox_url(self):
        return reverse('contact-infobox', args=[self.pk])

    def depending_objects(self):
        return {'Accession': self.verifications.accession}


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
    def images(self):
        from garden.models import PlantImage
        result = PlantImage.objects.none()
        try:
            plants_generator = (p for p in self.plants.all())
            while True:
                qs = next(plants_generator).images
                result |= qs
        except:
            pass
        return result

    @property
    def taxon(self):
        'best verification, and most recent'
        if self.verifications.count() == 0:
            return None
        return self.verifications.order_by('-level', '-date')[0].taxon

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
            return "{} ({})".format(self.code, best_verification.taxon.identify())
        else:
            return self.code

    @property
    def inline(self):
        return "%s" % self

    @property
    def twolines(self):
        str_locations = "{0} locations".format(len({p.location for p in self.plants.all()}))
        if str_locations == "{0} locations".format(1):  # this is thinking of translations
            str_locations = self.plants.first().location.inline
        if self.taxon:
            best_identification = self.taxon.identify()
        else:
            best_identification = '---'
        return {'item': self.code,
                'side': '{0} plant groups in {1}'.format(self.plants.count(), str_locations),
                'sub': best_identification}

    @property
    def infobox_url(self):
        return reverse('accession-infobox', args=[self.code])

    def depending_objects(self):
        return {'Plant': self.plants}


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
    seq = models.IntegerField()  # allows for composed conceptual primary key accession-seq
    level = models.CharField(blank=False, null=False, max_length=1, choices=VERIFICATION_LEVELS, default='0')
    contact = models.ForeignKey(Contact, blank=False, related_name='verifications', on_delete=models.PROTECT)
    date = models.DateField(blank=False, null=False)

    def __str__(self):
        return "{0.contact.fullname} says {0.accession.code} is a {1} - level {0.level}".format(self, self.taxon.identify())

    class Meta:
        unique_together = (('accession', 'seq'),
        )

    @property
    def inline(self):
        return "%s" % self
