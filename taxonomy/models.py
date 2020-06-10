from django.urls import reverse
from django.db import models
from .utils import make_phonetic

# Create your models here.

class Rank(models.Model):
    _id_of = {}
    #id,name,short,show_as
    #0,"regnum","",".epithet sp.",False
    name = models.CharField(max_length=16)
    short = models.CharField(max_length=8, blank=True)
    show_as = models.CharField(max_length=48, default='<i>.epithet</i> sp.')

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        Rank._id_of[self.name] = self.id
        return result

    def __str__(self):
        return self.name

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return reverse('rank-infobox', args=[self.pk])

    @classmethod
    def id_of(cls, name, default=99999):
        return cls._id_of.get(name, default)


class Taxon(models.Model):
    class Meta:
        verbose_name_plural = "taxa"

    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    epithet = models.CharField(max_length=40)  # published epithet
    epithet_phonetic = models.CharField(max_length=40)  # phonetic equivalent
    authorship = models.CharField(blank=True, max_length=120)  # publication authorship
    year = models.IntegerField(blank=True, null=True)  # publication year
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subtaxa', on_delete=models.CASCADE)
    accepted = models.ForeignKey('self', blank=True, null=True, related_name='synonyms', on_delete=models.SET_NULL)

    # these are automatically computed on save
    genus = models.CharField(max_length=40, blank=True, null=True)
    family = models.CharField(max_length=40, blank=True, null=True)

    @property
    def geometries(self):
        try:
            result = [p.geometry for p in a.all() for a in self.accessions.all()]
        except:
            result = []
        return result

    def save(self, *args, **kwargs):
        if not self.genus: self.genus = self.get_genus()
        if not self.family: self.family = self.get_family()
        self.epithet_phonetic = make_phonetic(self.epithet)
        return super().save(*args, **kwargs)

    def show(self, authorship=False):
        result = self.identify().replace(' sp.', '')
        if authorship and self.authorship:
            result += ' ' + self.authorship
        return result

    def identify(self, qualifier=None):
        def convert(match):
            item = match.group(0)
            field = item[1:]
            return getattr(self, field)
        import re
        result = re.sub(r'\.\w+', convert, self.rank.show_as)
        return result.strip()

    @property
    def derivation_up_to_order(self):
        result = []
        step = self
        while step.rank.id >= Rank.id_of('familia'):
            step = step.parent
            if step is None:
                break
            result.append(step.epithet)
        return result

    def get_family(self):
        if self.rank.id < Rank.id_of('familia'):
            return
        step = self
        while step and step.rank.id > Rank.id_of('familia'):
            step = step.parent
        return step and step.epithet

    def get_genus(self):
        if self.rank.id < Rank.id_of('genus'):
            return
        step = self
        while step and step.rank.id > Rank.id_of('genus'):
            step = step.parent
        return step and step.epithet

    @property
    def scientific(self):
        if self.rank.name == 'cultivar':
            step = self.parent
        else:
            step = self
        return step.identify()

    @property
    def binomial(self):
        step = self
        while step and step.rank.id > Rank.id_of('species'):
            step = step.parent
        return step and step.identify() or ''

    def __str__(self):
        return self.show(True)

    def __repr__(self):
        return self.__str__()

    @property
    def inline(self):
        return "%s" % self

    @property
    def twolines(self):
        family = self.family
        if not family and self.accepted:
            family = self.accepted.family
        family = family and (family + ' - ') or ''
        return {'item': self.show(authorship=True),
                'side': '',
                'sub': '{2}{0} verifications; {1} subtaxa'.format(len(self.verifications.all()), len(self.subtaxa.all()), family)}

    @property
    def infobox_url(self):
        return reverse('taxon-infobox', args=[self.pk])

    def depending_objects(self):
        return {'Accession': self.accessions.order_by('code'),
                'Taxon': self.subtaxa.order_by('rank_id', 'epithet', 'authorship')}


class Vernacular(models.Model):
    class Meta:
        verbose_name_plural = "Vernacular"

