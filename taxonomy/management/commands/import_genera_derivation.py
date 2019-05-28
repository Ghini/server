from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'import full genera derivation'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

        # Optional argument
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']

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
                    parent, _ = Taxon.objects.get_or_create(epithet=parent_epithet, rank=rank[parent_rank])
                    if orig.parent != parent:
                        orig.parent = parent
                        orig.save()
                    orig = parent
                    for_sake_of_logging.append(orig.epithet)
                print("\r{}".format(", ".join(for_sake_of_logging)), end=" ")

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string())
            else:
                username = get_random_string()
            User.objects.create_user(username=username, email='', password='123')
