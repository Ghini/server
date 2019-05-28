from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'import full genera derivation'

    def add_arguments(self, parser):
        parser.add_argument('--filter-genera', type=str, default=None,
                            help='location of genus.txt from ghini.desktop csv export')

    def handle(self, *args, **kwargs):
        genus_txt = kwargs['filter_genera']
        accept_genera = set()
        if genus_txt:
            with open(genus_txt) as f:
                for line in f.readlines():
                    genus, _ = line.split(',', 1)
                    accept_genera.add(genus)
        # We can import the model directly
        from taxonomy.models import Taxon, Rank
        rank = {name: Rank.objects.get(name=name)
                for name in ['genus', 'subtribus', 'tribus', 'subfamilia', 'familia']}
        with open('taxonomy/management/data/genus-to-family.txt') as f:
            while True:
                orig_epithet = next(f).strip()
                if not orig_epithet:
                    break
                lines = []
                while True:
                    line = next(f).strip()
                    if not line:
                        break
                    lines.append(line.split(':'))
                if accept_genera and orig_epithet not in accept_genera:
                    continue
                orig, _ = Taxon.objects.get_or_create(epithet=orig_epithet, rank=rank['genus'])
                for_sake_of_logging = [orig.epithet]
                acc_rank, acc_epithet = lines.pop()
                if acc_epithet != orig_epithet:
                    accepted, _ = Taxon.objects.get_or_create(epithet=acc_epithet, rank=rank[acc_rank])
                    orig.accepted = accepted
                    orig.save()
                    orig = accepted
                    for_sake_of_logging.append("-->{}".format(orig.epithet))
                while lines:
                    parent_rank, parent_epithet = lines.pop()
                    parent, is_new_parent = Taxon.objects.get_or_create(epithet=parent_epithet, rank=rank[parent_rank])
                    if orig.parent != parent:
                        orig.parent = parent
                        orig.save()
                    orig = parent
                    for_sake_of_logging.append(orig.epithet)
                    if not is_new_parent:
                        break
                self.stdout.write("\r{}".format(", ".join(for_sake_of_logging)), ending=" ")
        self.stdout.write("\rdone")
