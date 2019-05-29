from django.urls import reverse
from django.db import models

import computed_property as computed_models

# Create your models here.

class Rank(models.Model):
    species_id = 17
    family_id = 9
    #id,name,short,show_as
    #0,"regnum","",".epithet sp.",False
    name = models.CharField(max_length=16)
    short = models.CharField(max_length=8, blank=True)
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

    phonetic = computed_models.ComputedCharField(max_length=40, compute_from='compute_phonetic_epithet', default='')

    # I'm in doubt about the following properties, if they should be
    # computed attributes, held in the database.

    @property
    def family(self):
        step = self
        while step and step.rank.name != 'familia':
            step = step.parent
        return step and step.epithet or ''

    @property
    def genus(self):
        step = self
        while step and step.rank.name != 'genus':
            step = step.parent
        return step and step.epithet

    # properly methods and properties

    def compute_phonetic_epithet(self):
        import re
        x = self.epithet.lower()
        x = re.sub(r'c([ie])', r'z\1', x)  # palatal c sounds like z
        x = re.sub(r'g([ie])', r'j\1', x)  # palatal g sounds like j
        x = x.replace('ph', 'f')  # ph sounds like f
        x = x.replace('v', 'f')  # v sounds like f // fricative (voiced or not)

        x = x.replace('h', '')  # h sounds like nothing
        x = re.sub(r'[gcq]', r'k', x)  # g, c, q sound like k // guttural
        x = re.sub(r'[xz]', r's', x)  # x, z sound like s
        x = x.replace('ae', 'e')  # ae sounds like e
        x = re.sub('[ye]', 'i', x)  # y, e sound like i
        x = re.sub('[ou]', 'u', x)  # o, u sound like u // so we only have a, i, u
        x = re.sub(r'(.)\1', r'\1', x)  # doubled letters sound like single
        x = x.replace('-', '')
        return x

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
        while step.rank.id >= Rank.family_id:
            step = step.parent
            if step is None:
                break
            result.append(step.epithet)
        return result

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
        while step.rank.id > Rank.species_id:
            step = step.parent
        return step.identify()

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
        if family:
            family = family + ' - '
        return {'item': self.show(authorship=True),
                'side': '',
                'sub': '{2}{0} verifications; {1} subtaxa'.format(len(self.verifications.all()), len(self.subtaxa.all()), family)}

    @property
    def infobox_url(self):
        return reverse('taxon-infobox', args=[self.pk])

    def depending_objects(self):
        return {'Accession': self.accessions.order_by('code'),
                'Taxon': self.subtaxa.order_by('rank_id', 'epithet', 'authorship')}
