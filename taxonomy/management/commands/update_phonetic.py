from django.core.management.base import BaseCommand
from taxonomy.utils import make_phonetic

class Command(BaseCommand):
    help='update all `_phonetic` fields'
    def handle(self, *args, **kwargs):
        bulk = []
        threshold = 375
        from taxonomy.models import Taxon
        for taxon in Taxon.objects.all():
            phonetic = make_phonetic(taxon.epithet)
            if taxon.epithet_phonetic != phonetic:
                taxon.epithet_phonetic = phonetic
                bulk.append(taxon)
                if len(bulk) > threshold:
                    Taxon.objects.bulk_update(bulk, ['epithet_phonetic'])
                    bulk = []
        Taxon.objects.bulk_update(bulk, ['epithet_phonetic'])
