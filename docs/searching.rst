searching
---------------------------


The search strategies implemented by ghini.server and exposed through ghini.web:

:single field: ``<DOMAIN>`` . ``<field>`` ``<op>`` ``<INTEGER>``

                Filter, based on the value of a single field of the
                specified domain.

:domain: ``<DOMAIN>`` ``<op>`` ``<TERM>``

         Filter, based on the value of the default selection fields of the
         specified domain.  It can be seen as a shortcut to the previous,
         but where the match can be on multiple fields.

:terms: ``<TERMS>``

         Filter, based on the value of the default selection fields of any of the search
         domains.  ``TERMS`` is a space-separated list of values.  Again it can be seen as a
         shortcut to the previous, but where the match can be on any domain.  The filter
         succeeds if all the terms match.  If prefixed with the optional keyword ``or``, the
         filter succeeds if any one of the terms matches.

:sql-like: ``<DOMAIN>`` where ``<COMPLEX-QUERY>``

           This is the most generic and powerful search.  You give a search domain, then
           specify an expression to be matched.

           Expressions are composed of boolean tests on fields, either of the domain or of a
           connected domain (think of ``accession.plants.images``, or
           ``plant.accession.verifications.taxon.epithet``), tested with an operator (think
           of ``=``, ``like``, ``contains``, against values (think of a string, or a
           number).  Boolean tests can be combined with ``and``, ``or``, ``not``, and
           parentheses.

:depending: ``<query>`` | depending

            On any of the previous search strategies, you can append the
            query modifier ``| depending``.  This changes the resulting
            query-set, applying the *depending* function to each of the
            elements in the original result.

Logged in users can use the ghini.server API to run these queries, or use teh ghini.web
interface to enter them and have the results nicely organized in the various ghini.web tabs.
