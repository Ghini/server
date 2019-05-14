technical documentation
---------------------------

rest-api
~~~~~~~~~~

We have a main api for interacting with the database.

Each object has its URL, which really identifies the object (e.g.: plant #1 for
accession 101 in year 2001)::

  /garden/accession/2001.0101/plant/1/

Removing the object's trailing identificator from the URL gives the class
URL (e.g.: the plants collection)::

  /garden/accession/2001.0101/plant/

The trailing slash is part of the URL, but the server will add it if it's
missing.

**collections**

We organized the objects in three sections: ``taxonomy``, ``collection``,
``garden``.  There might come some day a ``herbarium`` or ``seedbank``
section, or we may reorganize in fewer sections, we will see.  As of now, we
have these collections::

  /taxonomy/rank/
  /taxonomy/taxon/
  /collection/accession/
  /collection/contact/
  /collection/accession/<code>/verification/
  /garden/accession/<code>/plant/
  /garden/accession/<code>/plant/<code>/propagation/
  /garden/location/

Verifications and Plants only make sense in combination with an accession,
so their collections are behind an accession code.  Same for Propagations,
which only make sense in relation with the mother plant.

**individual objects**

Append a primary key to a collection URL, and you get the URL for an
individual within the collection.

As far as their URLs are concerned, ``rank``, ``taxon``, ``contact`` have a
primary key which is a sequential number, with no semantics.

Accessions have their own accession code, Plants have a sequential plant
code within the Accession they belong to, Verifications also have a unique
sequential number within the Accession they describe.  Propagations have a
sequential number within their mother Plant.

.. note::

   If we generalize the database to model more than one garden, we will need
   to associate accessions to gardens, we will probably identify gardens
   with a stub, and will prepend accession urls with a garden stub code.  As
   of now, we only deal with a single garden.

**GET and her sisters**

Collection URLs implement the ``GET`` and ``POST`` verbs, respectively for getting
the whole collection (or a selection thereof), and for adding an individual
object to the collection.  These URLs get a ``-list`` suffix in their Django
name.

Individual URLs implement the ``GET``, ``PUT`` and ``DELETE`` verbs, with
their obvious meanings, applying to the specific individual only.  These
URLs get a ``-detail`` suffix in their Django name.

**more URLs**

Collections also have an URL for the empty html form, to be populated by
the user and posted to the server.  The corresponding Django names have
suffix ``-post-form``.

Individual objects have more entry points, respectively for:

- The populated html form (suffix ``-put-form``)
- A json data dictionary for the infobox (suffix ``-infobox``)
- A dictionary with several representations for the same object (suffix ``-markup``)

**search API**

``filter`` is the main query api entry point.  It expects a ``q`` parameter,
which it interprets according to several search strategies.  Search
strategies are described in some detail in the user manual.

The result of a ``filter`` request is a dictionary, where the keys are the
names of the collection in the result, and the values are the objects
matched by the ``q`` query.

Executing a search corresponds to constructing a queryset, each element in
the queryset is returned as a dictionary, with the structure:

:inline: The string shown in the result.  It may contain html tags.
:infobox_url: The url to get the corresponding infobox.

The ``inline`` entry is meant to be included in the results box.  The
``infobox_url`` provides quick access to the URL where we will get the
infobox data, but you can just replace the trailing *infobox/* part and
replace with whatever other valid suffix.  at the moment of writing, the
URLs implemented are *form/*, *markup/*, *depending/*.

importing from ghini.desktop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please consider this work in progress, try out the instructions, and be
prepared to ask for help or to open an issue if the present instructions do
not work.

First of all: taxasoft-ghini is not complete, not yet.  The current goal is
to have it do something useful, and to be visible on-line, it does not (yet)
substitute ghini.desktop.  Not at all.  Expect things to be exciting, but do
not expect things to work out of the box.

Got this?  Good, now let's see how to copy your ghini.desktop collection
into taxasoft-ghini!

from ghini.desktop
.................................

#. open ghini-1.0

   #. export your (complete) data to csv.

#. close ghini

#. open ghini-1.0 again,

   #. create a new sqlite3 connection,
   #. let ghini create the database.
   #. import the data, this will again initialize the database.

#. close ghini

   the result of the above steps is an expendable sqlite3 database: maybe
   you used something else, and we do not want to touch your original data.

#. remove all taxonomic information that is not used, straight on the database::

     sqlite3 ghini.db
     delete from genus where id not in (select genus_id from species);
     delete from family where id not in (select family_id from genus);
     delete from genus_synonym where genus_id not in (select id from genus);
     delete from genus_synonym where synonym_id not in (select id from genus);

#. consider removing history too, as long as it's not imported::

     delete from history;

#. open ghini.desktop-1.0

   #. export your (reduced) data to csv.

#. close ghini

now to taxasoft-ghini
.................................

#. enter the directory of your check-out;
#. activate the virtual environment;
#. if you didn't export to ``/tmp/1.0/``, you need to edit ``desktop_reader``
   so that it points to your csv export; look in particular for a string
   looking like ``/tmp/1.0/{}.txt`` and edit it to match your situation.
#. move any previous database out of the way;
#. create a new database and initialize it::

     ./manage.py migrate

#. run the command::

     ./manage.py shell <<EOF
     import desktop_reader
     desktop_reader.do_import()
     EOF

   this will output as many ``+`` as the objects it inserted, as many ``.`` as
   the objects it already found in place.  for species, a ``v`` is added if
   the related species is at lower rank.

#. create your superuser::

     ./manage.py createsuperuser

#. run your server::

     ./manage.py runserver

#. I'm sure there will be errors.  please open issues about them, and if you
   have a solution, propose it.
