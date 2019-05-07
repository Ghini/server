from django.urls import reverse
from django.db import models

# Create your models here.

class Rank(models.Model):
    #id,name,short,show_as
    #0,"regnum","",".epithet sp.",False
    name = models.CharField(max_length=16)
    short = models.CharField(max_length=8)
    show_as = models.CharField(max_length=48, default='<i>.epithet</i> sp.')

    def __str__(self):
        return self.name

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return reverse('rank-infobox', args=[self.pk])


class Taxon(models.Model):
    class Meta:
        verbose_name_plural = "taxa"

    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    epithet = models.CharField(max_length=40)  # published epithet
    authorship = models.CharField(blank=True, max_length=120)  # publication authorship
    year = models.IntegerField(blank=True, null=True)  # publication year
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subtaxa', on_delete=models.CASCADE)
    accepted = models.ForeignKey('self', blank=True, null=True, related_name='synonyms', on_delete=models.SET_NULL)

    def show(self, authorship=False):
        def convert(match):
            item = match.group(0)
            field = item[1:]
            if field == 'epithet':
                return getattr(self, field)
            else:
                return getattr(self.parent, field)
        import re
        return re.sub(r'\.\w+', convert, self.rank.show_as)

    @property
    def genus(self):
        step = self
        while step and step.rank.name != 'genus':
            step = step.parent
        return step and step.epithet

    @property
    def binomial(self):
        step = self
        while step and step.rank.name != 'species':
            step = step.parent
        return step and '{} {}'.format(step.genus, step.epithet)

    @property
    def identify(self):
        return self.show()

    def __str__(self):
        return "{} {}".format(self.epithet, self.authorship).strip()

    def __repr__(self):
        return self.__str__()

    @property
    def inline(self):
        return "%s" % self

    @property
    def infobox_url(self):
        return reverse('taxon-infobox', args=[self.pk])
