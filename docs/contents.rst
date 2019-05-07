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

The trailing dash is part of the URL, but the server will add it if it's
missing.

We have split the objects in three sections: ``taxonomy``, ``collection``,
``garden``.  There might come some day a ``herbarium`` or ``seedbank`` section, or
we may reorganize in fewer sections, we will see.  As of now, we have these
collections::

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

As far as their urls are concerned, ``rank``, ``taxon``, ``contact`` have a
primary key which is a sequential number, with no semantics.

Accessions have their own accession code, Plants have a sequential plant
code within the Accession they belong to, Verifications also have a unique
sequential number within the Accession they describe.  Propagations have a
sequential number within their mother Plant.

If we generalize the database to model more than one garden, we will need to
associate accessions to gardens, we will probably identify gardens with a
stub, and will prepend accession urls with a garden stub code.  As of now,
we only deal with a single garden.

Collection URLs implement the GET and POST verbs, respectively for getting
the whole collection (or a selection thereof), and for adding an individual
object to the collection.  These URLs get a ``-list`` suffix in their Django
name.

Individual URLs implement the GET, PUT and DELETE verbs, with their obvious
meanings.  These URLs get a ``-detail`` suffix in their Django name.

Collections have an extra URL, for the empty html form, to be populated by
the user and posted to the server.  Their namev have suffix ``-post-form``.

Individual objects also have other entry points, respectively for:

- The populated html form (suffix ``-put-form``)
- A json data dictionary for the infobox (suffix ``-infobox``)
- A dictionary with several representations for the same object (suffix ``-markup``)
  
