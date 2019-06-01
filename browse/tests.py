from django.test import TestCase

# Create your tests here.

from .searchgrammar import parse

class TestParsingQueries(TestCase):
    def test0_result_is_dictionary(self):
        result = parse('Location where true')
        self.assertTrue(isinstance(result, dict))

    def test1_can_find_all_objects(self):
        from garden.models import Location
        location, _ = Location.objects.get_or_create(name='here')
        location2, _ = Location.objects.get_or_create(name='there')
        result = parse('Location where true')
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 2)
        self.assertTrue(location in result['Location'])
        self.assertTrue(location2 in result['Location'])

    def test1_empty_collections_are_not_skipped(self):
        from garden.models import Location
        location, _ = Location.objects.get_or_create(name='here')
        result = parse('Location where false')
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 0)

    def test1_match_by_field(self):
        from garden.models import Location
        location, _ = Location.objects.get_or_create(name='here')
        location2, _ = Location.objects.get_or_create(name='there')
        result = parse('Location.id = {0.id}'.format(location))
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 1)
        self.assertTrue(location in result['Location'])
        self.assertTrue(location2 not in result['Location'])

    def test1_search_by_term(self):
        from garden.models import Location
        location, _ = Location.objects.get_or_create(name='here')
        location2, _ = Location.objects.get_or_create(name='very much over there')
        result = parse('"very much over there"')
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 1)
        self.assertTrue(location2 in result['Location'])
        self.assertTrue(location not in result['Location'])

    def test1_search_by_term_and_is_default(self):
        from garden.models import Location
        location1, _ = Location.objects.get_or_create(name='questo')
        location2, _ = Location.objects.get_or_create(name='codesto')
        location3, _ = Location.objects.get_or_create(name='quello')
        result = parse('questo codesto')
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 0)

    def test1_search_by_term_or(self):
        from garden.models import Location
        location1, _ = Location.objects.get_or_create(name='questo')
        location2, _ = Location.objects.get_or_create(name='codesto')
        location3, _ = Location.objects.get_or_create(name='quello')
        result = parse('or questo codesto')
        self.assertTrue('Location' in result)
        self.assertEquals(len(result['Location']), 2)
        self.assertTrue(location3 not in result['Location'])
        self.assertTrue(location2 in result['Location'])
        self.assertTrue(location1 in result['Location'])
        
