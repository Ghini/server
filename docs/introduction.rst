introduction
---------------------------

Ghini server is a AGPL software, aiming at letting professional and amateur botanists share
knowledge, in the form of plant images, localization of plant observations, taxonomic
identifications.

Ghini server follows established best practices for botanical collections, so that it can
successfully be used by botanical institutions needing a strong database foundation.

The combination ghini.server + ghini.web is the natural successor of ghini.desktop, a GPL
desktop program.  Even if the interface are very similar, they are based on different
technologies, and are not compatible at the database level.  There might come a
ghini.desktop version compatible with ghini.server.

serving
~~~~~~~~~~~

Installation of a ghini.server site amounts to installing a standard django service.  This
is a rather technical task, so please either look for and refer to the corresponding
documentation, or ask for advise and support.

fallback
~~~~~~~~~~~

Please refer to ghini.desktop

showcasing
~~~~~~~~~~~

Ghini server's initial goal is to showcase itself in the form of geographic botanical
collections.  If you have a use case and want to participate, please contact the Ghini team.
As of now, there's the following projects:

- `cuaderno <https://cuaderno.ghini.me>`_, a botanist's collection handbook.
- `almaghreb <https://almaghreb.ghini.me>`_, wild plants in the Atlas Region.

- `tanager <https://tanager.ghini.me>`_, a small privately held botanical garden.  The data
  in the database is by far not the complete garden's collection.
- `caribe <https://caribe.ghini.me>`_, wild plants in the Caribbean Area.

Participants get access to ghini's editing facilities and the django admin interface to the
database, while anonymous visitors can browse and query the data from the ghini interface.
