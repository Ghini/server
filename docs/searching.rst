searching
---------------------------

ghini exposes several search strategies, the most simple of which allows you to enter
values, or ``<TERMS>``, and ghini will attempt matching them against the data:

:terms: ``<TERMS>``

         Filter, based on the value of the default selection fields of any of the search
         domains.  ``<TERMS>`` is a space-separated list of values.  A match is found if one
         of the default search fields in one of the default search *domain* is found equal
         to one of the given terms.

         The filter succeeds on an element of a domain if all the terms match for that
         element.

         If prefixed with the optional keyword ``or``, the filter succeeds if any one of the
         terms matches.

         The **terms** strategy can be seen as a shortcut to the following, where we limit
         the search to a specific ``<DOMAIN>``.

:domain: ``<DOMAIN>`` ``<op>`` ``<TERM>``

         Filter based on the value of the default selection fields of the specified
         ``<DOMAIN>``, applying a specific comparison.

         ``<DOMAIN>`` is one of the data types, that's ``accession``, ``plant``, ``taxon``,
         etc.

         ``<op>`` is a comparison operator, that's ``=``, ``<=``, etc.

         The **domain** strategy can be seen as a shortcut to the following, in which we
         explicitly mention the ``<field>`` to be matched.

:single field: ``<DOMAIN>`` . ``<field>`` ``<op>`` ``<TERM>``

                Filter, based on the value of a single field of the specified domain.

Besides the three above term matching strategies, we have a rather complex and powerful
SQL-like search strategy.
                
:sql-like: ``<DOMAIN>`` ``where`` ``<COMPLEX-QUERY>``

           This is the most generic and powerful search.  You give a search domain, then
           specify an expression to be matched.  The literal string ``where`` in second
           position is what triggers usage of this strategy.

           ``COMPLEX-QUERY`` is an expression, composed of boolean tests on fields, either
           of the domain or of a connected domain (think of ``accession.plants.images``),
           tested with an operator (think of ``=``, ``like``, ``contains``, against values
           (think of a string, or a number).  Boolean tests can be combined with ``and``,
           ``or``, ``not``, and parentheses.

           For domains that specify a geometry (for example, ``plant``, where the
           ``geometry`` field is the current plant location) you can use the clause
           ``geometry in area``, where you specify the area by selecting it in the **map**
           page.

           Please consider that ghini will fall back to one of the above more generic search
           strategies if the query is somehow incorrect.  This will most likely return an
           empty result set.

:depending: ``<query>`` | depending

            On any of the previous search strategies, you can append the query modifier ``|
            depending``.  This changes the resulting query-set, applying the *depending*
            function to each of the elements in the original result.

Logged in users can use the ghini.server API to run these queries, or use the ghini.web
interface to enter them and have the results nicely organized in the various ghini.web tabs.
