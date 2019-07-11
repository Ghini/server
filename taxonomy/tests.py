from django.test import TestCase

# Create your tests here.
from taxonomy.models import Taxon, Rank

from unittest import SkipTest


class TaxonTestCase(TestCase):
    def setUp(self):
        self.r_reg, _ = Rank.objects.get_or_create(name="regnum", show_as=".epithet sp.")
        self.r_ord, _ = Rank.objects.get_or_create(name="ordo", show_as=".epithet sp.")
        self.r_fam, _ = Rank.objects.get_or_create(name="familia", show_as=".epithet sp.")
        self.r_gen, _ = Rank.objects.get_or_create(name="genus", show_as=".epithet sp.")
        self.r_sec, _ = Rank.objects.get_or_create(name="sectio", show_as=".genus sec. .epithet sp.")
        self.r_spe, _ = Rank.objects.get_or_create(name="species", show_as=".genus .epithet")
        self.r_var, _ = Rank.objects.get_or_create(name="varietas", show_as=".binomial var. .epithet")
        self.r_for, _ = Rank.objects.get_or_create(name="forma", show_as=".binomial f. .epithet")
        self.r_cul, _ = Rank.objects.get_or_create(name="cultivar", show_as=".scientific '.epithet'")

        self.plantae, _ = Taxon.objects.get_or_create(rank=self.r_reg, epithet='Plantae')
        [i.save() for i in Rank.objects.all()]

    def test3_shows_as_subspecies(self):
        cucurbitales, _ = Taxon.objects.get_or_create(rank=self.r_ord, parent=self.plantae, epithet='Cucurbitales')
        cucurbitaceae, _ = Taxon.objects.get_or_create(rank=self.r_fam, parent=cucurbitales, epithet='Cucurbitaceae')
        cucurbita, _ = Taxon.objects.get_or_create(rank=self.r_gen, parent=cucurbitaceae, epithet='Cucurbita')
        pepo, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=cucurbita, epithet='pepo')
        cylindrica, _ = Taxon.objects.get_or_create(rank=self.r_var, parent=pepo, epithet='cylindrica')
        self.assertEquals(cylindrica.show(), 'Cucurbita pepo var. cylindrica')
        
    def test4_shows_cultivar(self):
        cucurbitales, _ = Taxon.objects.get_or_create(rank=self.r_ord, parent=self.plantae, epithet='Cucurbitales')
        cucurbitaceae, _ = Taxon.objects.get_or_create(rank=self.r_fam, parent=cucurbitales, epithet='Cucurbitaceae')
        cucurbita, _ = Taxon.objects.get_or_create(rank=self.r_gen, parent=cucurbitaceae, epithet='Cucurbita')
        pepo, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=cucurbita, epithet='pepo')
        cylindrica, _ = Taxon.objects.get_or_create(rank=self.r_var, parent=pepo, epithet='cylindrica')

        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=cylindrica, epithet='Lekker Bek')
        self.assertEquals(cv.show(), "Cucurbita pepo var. cylindrica 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=pepo, epithet='Lekker Bek')
        self.assertEquals(cv.show(), "Cucurbita pepo 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=cucurbita, epithet='Lekker Bek')
        self.assertEquals(cv.show(), "Cucurbita 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=self.plantae, epithet='Lekker Bek')
        self.assertEquals(cv.show(), "Plantae 'Lekker Bek'")

        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=cylindrica, epithet='Lekker Bek')
        self.assertEquals(cv.identify(), "Cucurbita pepo var. cylindrica 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=pepo, epithet='Lekker Bek')
        self.assertEquals(cv.identify(), "Cucurbita pepo 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=cucurbita, epithet='Lekker Bek')
        self.assertEquals(cv.identify(), "Cucurbita sp. 'Lekker Bek'")
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=self.plantae, epithet='Lekker Bek')
        self.assertEquals(cv.identify(), "Plantae sp. 'Lekker Bek'")

    def test5_shows_speciem_novam(self):
        raise SkipTest()
        cucurbitales, _ = Taxon.objects.get_or_create(rank=self.r_ord, parent=self.plantae, epithet='Cucurbitales')
        cucurbitaceae, _ = Taxon.objects.get_or_create(rank=self.r_fam, parent=cucurbitales, epithet='Cucurbitaceae')
        cucurbita, _ = Taxon.objects.get_or_create(rank=self.r_gen, parent=cucurbitaceae, epithet='Cucurbita')
        sp_nov, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=cucurbita, nov_code='IGC1033')
        self.assertEquals(sp_nov.identify(), 'Cucurbita sp. (IGC1033)')
        sp_nov, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=cucurbitaceae, nov_code='IGC1034')
        self.assertEquals(sp_nov.identify(), 'Cucurbitaceae sp. (IGC1034)')
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=sp_nov, epithet='Lekker Bek')
        self.assertEquals(cv.identify(), "Cucurbitaceae sp. (IGC1034) 'Lekker Bek'")
        sp_nov, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=self.plantae, nov_code='IGC1035')
        self.assertEquals(sp_nov.identify(), 'Plantae sp. (IGC1035)')

    def test6_shows_australian_new(self):
        raise SkipTest()
        asterales, _ = Taxon.objects.get_or_create(rank=self.r_ord, parent=self.plantae, epithet='Asterales')
        asteraceae, _ = Taxon.objects.get_or_create(rank=self.r_fam, parent=asterales, epithet='Asteraceae')
        gen_nov, _ = Taxon.objects.get_or_create(rank=self.r_gen, parent=asteraceae, nov_code='Aq520454')
        sp_nov, _ = Taxon.objects.get_or_create(rank=self.r_spe, parent=gen_nov, nov_code='D.A.Halford Q811', nov_name='Shute Harbour')
        cv, _ = Taxon.objects.get_or_create(rank=self.r_cul, parent=sp_nov, epithet='Due di Denari')
        self.assertEquals(sp_nov.identify(), 'Gen. (Aq520454) sp. Shute Harbour (D.A.Halford Q811)')
        self.assertEquals(gen_nov.identify(), 'Gen. (Aq520454) sp.')
        self.assertEquals(cv.identify(), "Gen. (Aq520454) sp. Shute Harbour (D.A.Halford Q811) 'Due di Denari'")
        

class OrganizeByRangesTestCase(TestCase):
    def test_sequence(self):
        from .views import organize_by_ranges
        ids = list(range(1, 20))
        self.assertEquals(organize_by_ranges(ids, 5), ([], [(1, 19)]))
    def test_short_sequence(self):
        from .views import organize_by_ranges
        ids = list(range(1, 20))
        self.assertEquals(organize_by_ranges(ids, 500), (ids, []))
    def test_implicit_short_sequence(self):
        from .views import organize_by_ranges
        ids = list(range(1, 20))
        self.assertEquals(organize_by_ranges(ids), (ids, []))
    def test_singletons(self):
        from .views import organize_by_ranges
        ids = [1,3,5,7,9]
        self.assertEquals(organize_by_ranges(ids, 5), (ids, []))
    def test_singletons_plus_short_sequence(self):
        from .views import organize_by_ranges
        ids = [1,3,5,7,8,9]
        self.assertEquals(organize_by_ranges(ids, 5), (ids, []))
    def test_singletons_plus_short_sequence2(self):
        from .views import organize_by_ranges
        ids = [1,3,5,7,8,9]
        self.assertEquals(organize_by_ranges(ids, 3), ([1,3,5], [(7,9)]))
    def test_singletons_plus_sequence(self):
        from .views import organize_by_ranges
        ids = [1,3,5,6,7,8,9]
        self.assertEquals(organize_by_ranges(ids, 5), ([1,3], [(5,9)]))
    def test_singletons_plus_sequence(self):
        from .views import organize_by_ranges
        ids = [1,3,5,6,7,8,9]
        self.assertEquals(organize_by_ranges(ids, 6), (ids, []))
