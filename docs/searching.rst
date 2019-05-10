search strategies
---------------------------


The search strategies implemented, or planned, are:

:single field: ``<DOMAIN>`` . ``<field>`` ``<op>`` ``<INTEGER>``

                Filter, based on the value of a single field of the
                specified domain.
                
:domain: ``<DOMAIN>`` ``<op>`` ``<TERM>``

         Filter, based on the value of the default selection fields of the
         specified domain.  It can be seen as a shortcut to the previous.
         
:terms: ``<TERMS>``

         Filter, based on the value of the default selection fields of any
         of the search domains.  Again it can be seen as a shortcut to the
         previous.
        
:sql-like: ``<DOMAIN>`` where ``<COMPLEX-QUERY>``

           not implemented yet.
           
:depending: ``<query>`` | depending

            On any of the previous search strategies, you can append the
            query modifier ``| depending``.  This changes the resulting
            query-set, applying the *depending* function to each of the
            elements in the original result.
