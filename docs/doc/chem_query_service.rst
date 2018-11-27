Chemical query service
******************************

.. role:: raw-html(raw)
   :format: html
.. |info| image:: /_static/information.png
             :alt: information!


This page describes the reference for MyChem.info chemical query web service. It's also recommended to try it live on our `interactive API page <http://mychem.info/v1/api>`_.


Service endpoint
=================

::

    http://mychem.info/v1/query

GET request
==================

Query parameters
-----------------

q
"""""
    Required, passing user query. The detailed query syntax for parameter "**q**" we explained `below <#query-syntax>`_.

fields
""""""
    Optional, a comma-separated string to limit the fields returned from the matching chemical/drug hits. The supported field names can be found from any chemical object (e.g. `here <http://mychem.info/v1/chem/MNJVRJDLRVPLFE-UHFFFAOYSA-N>`_). Note that it supports dot notation, and wildcards as well, e.g., you can pass "drugbank", "drugbank.name", or "dbnsfp.products.*". If "fields=all", all available fields will be returned. Default: "all".

size
""""
    Optional, the maximum number of matching chemical hits to return (with a cap of 1000 at the moment). Default: 10.

from
""""
    Optional, the number of matching chemical hits to skip, starting from 0. Default: 0

.. Hint:: The combination of "**size**" and "**from**" parameters can be used to get paging for large query:

::

    q=drugbank.name:acid*&size=50                     first 50 hits
    q=drugbank.name:acid*&size=50&from=50             the next 50 hits

fetch_all
"""""""""
    Optional, a boolean, which when TRUE, allows fast retrieval of all unsorted query hits.  The return object contains a **_scroll_id** field, which when passed as a parameter to the query endpoint, returns the next 1000 query results.  Setting **fetch_all** = TRUE causes the results to be inherently unsorted, therefore the **sort** parameter is ignored.  For more information see `examples using fetch_all here <#scrolling-queries>`_.  Default: FALSE.

scroll_id
"""""""""
    Optional, a string containing the **_scroll_id** returned from a query request with **fetch_all** = TRUE.  Supplying a valid **scroll_id** will return the next 1000 unordered results.  If the next results are not obtained within 1 minute of the previous set of results, the **scroll_id** becomes stale, and a new one must be obtained with another query request with **fetch_all** = TRUE.  All other parameters are ignored when the **scroll_id** parameter is supplied.  For more information see `examples using scroll_id here <#scrolling-queries>`_.

sort
""""
    Optional, the comma-separated fields to sort on. Prefix with "-" for descending order, otherwise in ascending order. Default: sort by matching scores in descending order.

facets
""""""
    Optional, a single field or comma-separated fields to return facets, can only be used on non-free text fields.  E.g. "facets=chembl.molecule_properties.full_mwt".  See `examples of faceted queries here <#faceted-queries>`_.

facet_size
""""""""""
    Optional, an integer (1 <= **facet_size** <= 1000) that specifies how many buckets to return in a faceted query.

callback
""""""""
    Optional, you can pass a "**callback**" parameter to make a `JSONP <http://ajaxian.com/archives/jsonp-json-with-padding>`_ call.

dotfield
""""""""
    Optional, can be used to control the format of the returned chemical object.  If "dotfield" is true, the returned data object is returned flattened (no nested objects) using dotfield notation for key names.  Default: false.

email
""""""
    Optional, if you are regular users of our services, we encourage you to provide us an email, so that we can better track the usage or follow up with you.


Query syntax
------------
Examples of query parameter "**q**":


Simple queries
""""""""""""""

search for everything::

    q=imatinib                        # search all default fields for term


Fielded queries
"""""""""""""""
::

    q=chebi.xref.uniprot:P80175               # for matching value on a specific field

    q=drugbank.name:(acid alcohol)            # multiple values for a field
    q=drugbank.name:(acid OR alcohol)         # multiple values for a field using OR

    q=_exists_:pubchem                        # having pubchem field
    q=NOT _exists_:drugbank                   # missing drugbank field


.. Hint:: For a list of available fields, see :ref:`here <available_fields>`.


Range queries
"""""""""""""
::

    q=pubchem.exact_mass:<200
    q=pubchem.exact_mass:>=500

    q=pubchem.exact_mass:[200 TO 500]         # bounded (including 200 and 500)
    q=pubchem.exact_mass:{200 TO 500}        # unbounded


Wildcard queries
""""""""""""""""
Wildcard character "*" or "?" is supported in either simple queries or fielded queries::

    q=drugbank.name:acid*

.. note:: Wildcard character can not be the first character. It will be ignored.


Scrolling queries
"""""""""""""""""
If you want to return ALL results of a very large query, sometimes the paging method described `above <#from>`_ can take too long.  In these cases, you can use a scrolling query.
This is a two-step process that turns off database sorting to allow very fast retrieval of all query results.  To begin a scrolling query, you first call the query
endpoint as you normally would, but with an extra parameter **fetch_all** = TRUE.  For example, a GET request to::

    http://mychem.info/v1/query?q=_exists_:drugbank&fields=drugbank.name&fetch_all=TRUE

Returns the following object:

.. code-block:: json


    {
      "_scroll_id": "cXVlcnlUaGVuRmV0Y2g7MTA7Njg4ODAwOTI6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDA5MTpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDkzOkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTQ6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDEwMDpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDk2OkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTg6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDA5NzpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDk5OkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTU6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzswOw==",
      "max_score": 1.0,
      "took": 2042,
      "total": 11290,
      "hits": [
        {
          "_id": "SDUQYLNIPVEERB-QPPQHZFASA-N",
          "_score": 1.0,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Gemcitabine"
          }
        },
        {
          "_id": "SESFRYSPDFLNCH-UHFFFAOYSA-N",
          "_score": 1.0,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Benzyl Benzoate"
          }
        },
        .
        .
        .
      ],
    }

At this point, the first 1000 hits have been returned (of ~11,000 total), and a scroll has been set up for your query.  To get the next batch of 1000 unordered results, simply execute a GET request to the following address, supplying the _scroll_id from the first step into the **scroll_id** parameter in the second step::

    http://mychem.info/v1/query?scroll_id=cXVlcnlUaGVuRmV0Y2g7MTA7Njg4ODAwOTI6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDA5MTpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDkzOkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTQ6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDEwMDpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDk2OkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTg6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzs2ODg4MDA5NzpKZTRyT2gxNlRQcXJFeVhJM09LakxnOzY4ODgwMDk5OkplNHJPaDE2VFBxckV5WEkzT0tqTGc7Njg4ODAwOTU6SmU0ck9oMTZUUHFyRXlYSTNPS2pMZzswOw==

.. Hint:: Your scroll will remain active for 1 minute from the last time you requested results from it.  If your scroll expires before you get the last batch of results, you must re-request the scroll_id by setting **fetch_all** = TRUE as in step 1.

.. Hint:: When you need to use this "scrolling query" feature via "fetch_all" parameter, we recommend you to use our Python client "`biothings_client <doc/packages.html>`_".

Boolean operators and grouping
""""""""""""""""""""""""""""""

You can use **AND**/**OR**/**NOT** boolean operators and grouping to form complicated queries::

    q=_exists_:drugbank AND _exists_:pubchem                               AND operator
    q=_exists_:drugbank AND NOT _exists_:pubchem                           NOT operator
    q=_exists_:drugbank OR (_exists_:chebi AND _exists_:pubchem)           grouping with ()


Escaping reserved characters
""""""""""""""""""""""""""""
If you need to use these reserved characters in your query, make sure to escape them using a back slash ("\\")::

    + - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /



Returned object
---------------

A GET request like this::

    http://mychem.info/v1/query?q=drugbank.name:acid&fields=drugbank.name

should return hits as:

.. code-block:: json

    {
      "max_score": 7.929331,
      "took": 102,
      "total": 1063,
      "hits": [
        {
          "_id": "BDAGIHXWWSANSR-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Formic Acid"
          }
        },
        {
          "_id": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Acetylsalicylic acid"
          }
        },
        {
          "_id": "KGBXLFKZBHKPEV-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Boric acid"
          }
        },
        {
          "_id": "LPEPZBJOKDYZAD-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Flufenamic Acid"
          }
        },
        {
          "_id": "JXMIBUGMYLQZGO-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Iotroxic acid"
          }
        },
        {
          "_id": "HXQVQGWHFRNKMS-UHFFFAOYSA-M",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Ethylmercurithiosalicylic acid"
          }
        },
        {
          "_id": "LOAUVZALPPNFOQ-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Quinaldic Acid"
          }
        },
        {
          "_id": "LDKRAXXVBWHMRH-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Phosphonoacetohydroxamic Acid"
          }
        },
        {
          "_id": "GWYFCOCPABKNJV-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Isovaleric Acid"
          }
        },
        {
          "_id": "HJZKOAYDRQLPME-UHFFFAOYSA-N",
          "_score": 7.929331,
          "drugbank": {
            "_license": "http://bit.ly/2PSfZTD",
            "name": "Oxidronic acid"
          }
        }
      ]
    }

"**total**" in the output gives the total number of matching hits, while the actual hits are returned under "**hits**" field. "**size**" parameter controls how many hits will be returned in one request (default is 10). Adjust "**size**" parameter and "**from**" parameter to retrieve the additional hits.

Faceted queries
----------------
If you need to perform a faceted query, you can pass an optional "`facets <#facets>`_" parameter.

A GET request like this::

    http://mychem.info/v1/query?q=drugbank.name:acid&fields=drugbank.name&facets=drugbank.targets.organism&size=0

should return hits as:

.. code-block:: json

    {
      "facets": {
        "drugbank.targets.organism": {
          "other": 1782,
          "_type": "terms",
          "missing": 8,
          "total": 1483,
          "terms": [
            {
              "count": 545,
              "term": "human"
            },
            {
              "count": 250,
              "term": "strain"
            },
            {
              "count": 155,
              "term": "escherichia"
            },
            {
              "count": 154,
              "term": "coli"
            },
            {
              "count": 138,
              "term": "k12"
            },
            {
              "count": 79,
              "term": "atcc"
            },
            {
              "count": 54,
              "term": "pseudomonas"
            },
            {
              "count": 43,
              "term": "dsm"
            },
            {
              "count": 34,
              "term": "bacillus"
            },
            {
              "count": 31,
              "term": "sp"
            }
          ]
        }
      },
      "max_score": 0.0,
      "took": 12,
      "total": 1063,
      "hits": []
    }


Batch queries via POST
======================

Although making simple GET requests above to our chemical query service is sufficient for most use cases,
there are times you might find it more efficient to make batch queries (e.g., retrieving chemical
annotation for multiple chemicals). Fortunately, you can also make batch queries via POST requests when you
need::


    URL: http://mychem.info/v1/query
    HTTP method:  POST


Query parameters
----------------

q
"""
    Required, multiple query terms seperated by comma (also support "+" or white space), but no wildcard, e.g., 'q=SDUQYLNIPVEERB-QPPQHZFASA-N,SESFRYSPDFLNCH-UHFFFAOYSA-N'

scopes
""""""
    Optional, specify one or more fields (separated by comma) as the search "scopes", e.g., "scopes=drugbank".  The available "fields" can be passed to "**scopes**" parameter are
    :ref:`listed here <available_fields>`. Default:

fields
""""""
    Optional, a comma-separated string to limit the fields returned from the matching chem hits. The supported field names can be found from any chemical object. Note that it supports dot notation, and wildcards as well, e.g., you can pass "drugbank", "drugbank.name", or "dbnsfp.products.*". If "fields=all", all available fields will be returned. Default: "all".

email
""""""
    Optional, if you are regular users of our services, we encourage you to provide us an email, so that we can better track the usage or follow up with you.

Example code
------------

Unlike GET requests, you can easily test them from browser, make a POST request is often done via a
piece of code. Here is a sample python snippet using `httplib2 <https://pypi.org/project/httplib2/>`_ module::

    import httplib2
    h = httplib2.Http()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = 'q=CHEBI:175901,CHEBI:41237&scopes=chebi.id&fields=drugbank.name'
    res, con = h.request('http://mychem.info/v1/query', 'POST', params, headers=headers)

or this example using `requests <http://docs.python-requests.org>`_ module::

    import requests
    params = {'q': 'CHEBI:175901,CHEBI:41237', 'scopes': 'chebi.id', 'fields': 'drugbank.name'}
    res = request.post('http://mychem.info/v1/query', params)
    con = res.json()

Returned object
---------------

Returned result (the value of "con" variable above) from above example code should look like this:

.. code-block:: json


    [
      {
        "query": "CHEBI:175901",
        "_score": 16.388842,
        "drugbank": {
          "_license": "http://bit.ly/2PSfZTD",
          "name": "Gemcitabine"
        },
        "_id": "SDUQYLNIPVEERB-QPPQHZFASA-N"
      },
      {
        "query": "CHEBI:41237",
        "_score": 16.388842,
        "drugbank": {
          "_license": "http://bit.ly/2PSfZTD",
          "name": "Benzyl Benzoate"
        },
        "_id": "SESFRYSPDFLNCH-UHFFFAOYSA-N"
      }
    ]

.. Tip:: "query" field in returned object indicates the matching query term.

If a query term has no match, it will return with "**notfound**" field as "**true**":

.. code-block:: json

      [
        ...,
        {'query': '...',
         'notfound': true},
        ...
      ]


.. raw:: html

    <div id="spacer" style="height:300px"></div>
