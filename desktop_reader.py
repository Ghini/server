import sys
import csv

from garden.models import Location, Plant
from taxonomy.models import Taxon, Rank
from collection.models import Accession, Verification, Contact

Family = Rank.objects.get(name='familia')
Genus = Rank.objects.get(name='genus')
Species = Rank.objects.get(name='species')
default_contact = Contact.objects.get_or_create(name='Jaap')[0]

pk2obj = {}


def family_creator(o):
    del o['qualifier']
    result = Taxon.objects.get_or_create(rank=Family, epithet=o['family'])
    print(o['family'], end="")
    return result


def genus_creator(o):
    result = Taxon.objects.get_or_create(rank=Genus, epithet=o['genus'],
                                         defaults={'authorship': o['author'],
                                                   'parent': pk2obj[('family', o['family_id'])]})
    return result


def species_creator(o):
    if o['sp'] in ['sp.', 'sp'] or o['infrasp1'] in ['sp', 'sp.']:
        return (pk2obj[('genus', o['genus_id'])], False)
    result = Taxon.objects.get_or_create(rank=Species, epithet=o['sp'],
                                         defaults={'authorship': o['sp_author'],
                                                   'parent': pk2obj[('genus', o['genus_id'])]})
    if o['infrasp1'] != '':
        rank = Rank.objects.get(short=o['infrasp1_rank'])
        infrasp = Taxon.objects.get_or_create(rank=rank, epithet=o['infrasp1'],
                                              defaults={'authorship': o['infrasp1_author'],
                                                        'parent': result[0]})
        print('v', end='')
        return infrasp
    return result


def location_creator(o):
    result = Location.objects.get_or_create(
        code=o['code'],
        defaults=o)
    return result


def accession_creator(o):
    result = Accession.objects.get_or_create(
        code=o['code'],
        defaults={'accessioned_date': o['date_accd'],
                  'received_date': o['date_recvd'] or None,
                  'received_quantity': o['quantity_recvd'] or 1,
                  'received_type': o['recvd_type'],
        })
    initial_verification = Verification.objects.get_or_create(
        accession=result[0],
        taxon=pk2obj['species', o['species_id']],
        seq=1,
        defaults={ 'contact': default_contact,
                   'date': o['date_accd'],
                   'level': '0', }
    )
    return result


def plant_creator(o):
    result = Plant.objects.get_or_create(
        accession=pk2obj[('accession', o['accession_id'])],
        code=o['code'],
        location=pk2obj[('location', o['location_id'])],
        quantity=o['quantity'],)
    return result


def do_import():
    for (n, importer) in [('location', location_creator),
                          ('family', family_creator),
                          ('genus', genus_creator),
                          ('species', species_creator),
                          ('accession', accession_creator),
                          ('plant', plant_creator)]:
        print('\n{}: '.format(n), end='')
        with open('/tmp/1.0/{}.txt'.format(n)) as csvfile:
            spamreader = csv.reader(csvfile)
            header = next(spamreader)
            for row in spamreader:
                o = {k: v for (k,v) in zip(header, row) if not k.startswith('_')}
                oid = o.pop('id')
                (obj, isnew) = importer(o)
                pk2obj[(n, oid)] = obj
                print(isnew and '+' or '.', end='')
                sys.stdout.flush()
    print()


if __name__ == '__main__':
    do_import()
