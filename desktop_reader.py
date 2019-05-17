#!/usr/bin/env python3

# ugly script that imports a ghini.desktop-1.0 backup into ghini-reloaded. it
# does NOT do all the tables, just the ones listed in the outer loop in the
# function `do_import`.

# please read the docs before using this script.  it will most likely not do
# what you expect.  in particular, you need to massage the database before even
# attempting the import.

# for each table, there's an importer function.  if you want to do an other
# table, write the importer function first.  keep in mind foreign keys when
# adding tables, order of importing is relevant.

# this script is meant to be run from `./manage.py shell`, and we have a
# `redo.sh` bash script that prepares the situation.

#

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
    # epithet is unique at rank above species, within rank.
    result = Taxon.objects.get_or_create(rank=Family, epithet=o['family'])
    return result


def genus_creator(o):
    if o['genus'].startswith('Zzz'):
        return (pk2obj[('family', o['family_id'])], False)
    # epithet is unique at rank above species, within rank.
    result = Taxon.objects.get_or_create(rank=Genus, epithet=o['genus'],
                                         defaults={'authorship': o['author'],
                                                   'parent': pk2obj[('family', o['family_id'])]})
    return result


def species_creator(o):
    # epithets at rank species and lower are not unique, not even within rank,
    # it is only so in combination with parent, so we 'get_or_create' based on
    # the three fields rank, epithet, parent.
    if o['sp'] in ['sp.', 'sp'] or o['infrasp1'] in ['sp', 'sp.']:
        return (pk2obj[('genus', o['genus_id'])], False)
    result = Taxon.objects.get_or_create(rank=Species, epithet=o['sp'], parent=pk2obj[('genus', o['genus_id'])],
                                         defaults={'authorship': o['sp_author'], })
    if o['infrasp1'] != '' and o['infrasp1_rank'].strip():
        try:
            rank = Rank.objects.get(short=o['infrasp1_rank'].replace('cv.', 'cv'))
            infrasp = Taxon.objects.get_or_create(rank=rank, epithet=o['infrasp1'], parent=result[0],
                                                  defaults={'authorship': o['infrasp1_author'], })
            print('v', end='')
            return infrasp
        except Exception as e:
            print('\n', type(e).__name__, e, o)
    return result


def location_creator(o):
    result = Location.objects.get_or_create(
        code=o['code'],
        defaults=o)
    return result


def accession_creator(o):
    try:
        result = Accession.objects.get_or_create(
            code=o['code'],
            defaults={'accessioned_date': o['date_accd'] or None,
                      'received_date': o['date_recvd'] or None,
                      'received_quantity': o['quantity_recvd'] or 1,
                      'received_type': o['recvd_type'],
            })
        initial_verification = Verification.objects.get_or_create(
            accession=result[0],
            taxon=pk2obj['species', o['species_id']],
            defaults={ 'contact': default_contact,
                       'date': o['date_accd'] or '1901-01-01',
                       'level': '0',
                       'seq': 1,
            }
        )
        return result
    except Exception as e:
        print('\n', type(e).__name__, e, o)
        raise


def plant_creator(o):
    result = Plant.objects.get_or_create(
        accession=pk2obj[('accession', o['accession_id'])],
        code=o['code'],
        location=pk2obj[('location', o['location_id'])],
        quantity=o['quantity'],)
    return result


def do_import():
    for (table, importer) in [('location', location_creator),
                          ('family', family_creator),
                          ('genus', genus_creator),
                          ('species', species_creator),
                          ('accession', accession_creator),
                          ('plant', plant_creator)]:
        print('\n{}: '.format(table), end='')
        with open('/tmp/1.0/{}.txt'.format(table)) as csvfile:
            spamreader = csv.reader(csvfile)
            header = next(spamreader)
            for row in spamreader:
                o = {k: v for (k,v) in zip(header, row) if not k.startswith('_')}
                oid = o.pop('id')
                (obj, isnew) = importer(o)
                pk2obj[(table, oid)] = obj
                print(isnew and '+' or '.', end='')
                sys.stdout.flush()
    print()


if __name__ == '__main__':
    do_import()
