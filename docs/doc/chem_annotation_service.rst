Chemical annotation service
*************************************

This page describes the reference for the MyVariant.info chemical annotation web 
service.  It's also recommended to try it live on our `interactive API page <http://mychem.info/tryapi/>`_.


Service endpoint
=================
::

    http://mychem.info/v1/chem


GET request
==================

Obtaining the chem annotation via our web service is as simple as calling this URL::

    http://mychem.info/v1/chem/<chemid>

**chemid** above is an HGVS name based chemical id using genomic location based on hg19 human genome assembly.

By default, this will return the complete chemical annotation object in JSON format. See `here <#returned-object>`_ for an example and :ref:`here <chemical_object>` for more details. If the input **variantid** is not valid, 404 (NOT FOUND) will be returned.

Optionally, you can pass a "**fields**" parameter to return only the annotation you want (by filtering returned object fields)::

    http://mychem.info/v1/chem/chr1:g.35367G>A?fields=cadd

"**fields**" accepts any attributes (a.k.a fields) available from the chemical object. Multiple attributes should be separated by commas. If an attribute is not available for a specific chemical object, it will be ignored. Note that the attribute names are case-sensitive.

Just like the `chemical query service <chem_query_service.html>`_, you can also pass a "**callback**" parameter to make a `JSONP <http://ajaxian.com/archives/jsonp-json-with-padding>`_ call.


Query parameters
-----------------

fields
""""""""
    Optional, can be a comma-separated fields to limit the fields returned from the chemical object. If "fields=all", all available fields will be returned. Note that it supports dot notation as well, e.g., you can pass "cadd.gene". Default: "fields=all".

callback
"""""""""
    Optional, you can pass a "**callback**" parameter to make a `JSONP <http://ajaxian.com/archives/jsonp-json-with-padding>`_ call.

filter
"""""""
    Alias for "fields" parameter.

email
""""""
    Optional, if you are regular users of our services, we encourage you to provide us an email, so that we can better track the usage or follow up with you.

-----------------

Returned object
---------------

A GET request like this::

    http://mychem.info/v1/chem/chr1:g.35367G>A

should return a chemical object below:

.. container :: chemical-object-container

    .. include :: chem_object.json


Batch queries via POST
======================

Although making simple GET requests above to our chemical query service is sufficient in most use cases,
there are some times you might find it's easier to batch query (e.g., retrieving chemical
annotations for multiple chemicals). Fortunately, you can also make batch queries via POST requests when you
need::


    URL: http://mychem.info/v1/chem
    HTTP method:  POST


Query parameters
----------------

ids
"""""
    Required. Accept multiple HGVS chemical ids separated by comma, e.g., "ids=chr1:g.35367C>T,chr7:g.55241707G>T,chr16:g.28883241A>G". Note that currently we only take the input ids up to **1000** maximum, the rest will be omitted.

fields
"""""""
    Optional, can be a comma-separated fields to limit the fields returned from the matching hits. 
    If “fields=all”, all available fields will be returned. Note that it supports dot notation as well, e.g., you can pass "dbnsfp", "dbnsfp.genename", or "dbnsfp.aa.*". Default: "all".

email
""""""
    Optional, if you are regular users of our services, we encourage you to provide us an email, so that we can better track the usage or follow up with you.

Example code
------------

Unlike GET requests, you can easily test them from browser, make a POST request is often done via a
piece of code, still trivial of course. Here is a sample python snippet::

    import httplib2
    h = httplib2.Http()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = 'ids=chr16:g.28883241A>G,chr1:g.35367G>A&fields=dbnsfp.genename,cadd.gene'
    res, con = h.request('http://mychem.info/v1/chem', 'POST', params, headers=headers)

Returned object
---------------

Returned result (the value of "con" variable above) from above example code should look like this:


.. code-block :: json

    [
      {
        "_id": "chr16:g.28883241A>G",
        "cadd": {
          "gene": {
            "ccds_id": "CCDS53996.1",
            "cds": {
              "cdna_pos": 1889,
              "cds_pos": 1450,
              "rel_cdna_pos": 0.61,
              "rel_cds_pos": 0.64
            },
            "feature_id": "ENST00000322610",
            "gene_id": "ENSG00000178188",
            "genename": "SH2B1",
            "prot": {
              "protpos": 484, "rel_prot_pos": 0.64
            }
          }
        },
        "dbnsfp": {
          "genename": "SH2B1"
        },
        "query": "chr16:g.28883241A>G"
      },
      {
        "_id": "chr1:g.35367G>A",
        "cadd": {
          "gene": {
            "cds": {
              "cdna_pos": 476, 
              "rel_cdna_pos": 0.4
            },
            "feature_id": "ENST00000417324",
            "gene_id": "ENSG00000237613",
            "genename": "FAM138A"
          }
        },
        "dbnsfp": {
          "genename": "FAM138A"
        },
        "query": "chr1:g.35367G>A"
      }
    ]

.. raw:: html

    <div id="spacer" style="height:300px"></div>
