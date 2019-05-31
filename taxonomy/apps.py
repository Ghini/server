from django.apps import AppConfig


class TaxonomyConfig(AppConfig):
    name = 'taxonomy'

    def ready(self):
        from .models import Rank
        for r in Rank.objects.all():
            r.save()
