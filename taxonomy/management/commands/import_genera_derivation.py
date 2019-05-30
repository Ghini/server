from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from taxonomy.models import Taxon, Rank

class Command(BaseCommand):
    help = 'import full genera derivation'

    def next_id(self):
        return next(self._next_id())

    def _next_id(self):
        while True:
            self.max_id += 1
            yield self.max_id

    def handle(self, *args, **kwargs):
        # We can import the model directly
        rank = {name: Rank.objects.get(name=name)
                for name in ['genus', 'subtribus', 'tribus', 'subfamilia', 'familia']}
        with open('taxonomy/management/data/one-step-derivation.txt') as f:
            doing = 'familia'
            self.bulk_update = []
            self.bulk_create = []
            counting = 0
            from django.db.models import Max
            self.max_id = Taxon.objects.aggregate(Max('id'))['id__max'] + 300
            while True:  # first loop: link to parent
                line = next(f).strip()
                counting += 1
                if not line:
                    self.flush_bulk(0)
                    break  # let's now do genus synonyms
                prank, pepithet, crank, cepithet = line.split(',')
                try:
                    parent = Taxon.objects.get(epithet=pepithet, rank=rank[prank])
                except Taxon.DoesNotExist:
                    parent = Taxon.objects.create(epithet=pepithet, rank=rank[prank], id=self.next_id())
                    parent.save()
                try:
                    child = Taxon.objects.get(epithet=cepithet, rank=rank[crank])
                    if child.parent != parent:
                        child.parent = parent
                        self.bulk_update.append(child)
                except Taxon.DoesNotExist:
                    child = Taxon(epithet=cepithet, rank=rank[crank], parent=parent, id=self.next_id())
                    self.bulk_create.append(child)
                self.flush_bulk()
                self.stdout.write("\r{:>5} {}".format(counting, line), ending=" ")
            while True:  # second loop: accepted
                line = next(f).strip()
                counting += 1
                if not line:
                    self.flush_bulk(0)
                    break  # we're finished
                this, that = line.split(',')
                that = Taxon.objects.get(epithet=that, rank=rank['genus'])
                try:
                    this = Taxon.objects.get(epithet=this, rank=rank['genus'])
                    this.parent = that.parent
                    this.accepted = that
                    self.bulk_update.append(this)
                except Taxon.DoesNotExist:
                    this = Taxon(epithet=this, rank=rank['genus'], id=self.next_id(), parent=that.parent, accepted=that)
                    self.bulk_create.append(this)
                self.flush_bulk()
                self.stdout.write("\r{:>5} {}".format(counting, line), ending=" ")
        self.stdout.write("\rdone")

    def flush_bulk(self, threshold=375):
        if len(self.bulk_update) > threshold:
            self.stdout.write("\r{}".format('... updating ...'), ending=" ")
            Taxon.objects.bulk_update(self.bulk_update, ['parent', 'accepted'])
            self.bulk_update.clear()
        if len(self.bulk_create) > threshold:
            self.stdout.write("\r{}".format('... creating ...'), ending=" ")
            Taxon.objects.bulk_create(self.bulk_create)
            self.bulk_create.clear()
        
