from django.db import models

# Create your models here.

class Taxon(models.Model):
    GENUS_RANK = 13
    SPECIES_RANK = 19
    TAXON_RANKS = (
        (1, 'regnum'),
        (2, 'subregnum'),
        (3, 'divisio'),
        (4, 'subdivisio'),
        (5, 'classis'),
        (6, 'subclassis'),
        (7, 'ordo'),
        (8, 'subordo'),
        (9, 'familia'),
        (10, 'subfamilia'),
        (11, 'tribus'),
        (12, 'subtribus'),
        (13, 'genus'),
        (14, 'subgenus'),
        (15, 'sectio'),
        (16, 'subsectio'),
        (17, 'series'),
        (18, 'subseries'),
        (19, 'species'),
        (20, 'subspecies'),
        (21, 'varietas'),
        (22, 'subvarietas'),
        (23, 'forma'),
        (24, 'subforma'),
    )

    rank = models.IntegerField(choices=TAXON_RANKS)
    epithet = models.CharField(max_length=40)  # published epithet
    authorship = models.CharField(max_length=120)  # publication authorship
    year = models.IntegerField(null=True)  # publication year
    parent = models.ForeignKey('self', null=True, related_name='subtaxa', on_delete=models.CASCADE)
    accepted = models.ForeignKey('self', null=True, related_name='synonyms', on_delete=models.SET_NULL)

    @property
    def genus(self):
        genus = self
        while genus and genus.rank > self.GENUS_RANK:
            genus = genus.parent
        if genus and genus.rank == self.GENUS_RANK:
            return genus
        else:
            return None

    @property
    def species(self):
        species = self
        while species and species.rank > self.SPECIES_RANK:
            species = species.parent
        if species and species.rank == self.SPECIES_RANK:
            return species
        else:
            return None

    def __str__(self):
        if self.rank == self.SPECIES_RANK:
            return "<Taxon: {} {} {}>".format(self.genus.epithet, self.epithet, self.authorship)
        if self.rank > self.SPECIES_RANK:
            return "<Taxon: {} {} {} {}>".format(self.genus.epithet, self.species.epithet, self.epithet, self.authorship)
        return "<Taxon: {} {}>".format(self.epithet, self.authorship)

    def __repr__(self):
        return self.__str__()
