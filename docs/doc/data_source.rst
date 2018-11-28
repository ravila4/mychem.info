Data Sources
============

This page records the notes specific to each data source, regarding the ETL process when their data were integrated into `MyChem.info <http://mychem.info>`_:

.. note:: The structured metadata about all data sources can be accessed from `the metadata endpoint <http://mychem.info/v1/metadata>`_. The detailed information about the integrated data is described in this `data page <data.html>`_.

AEOLUS
------

ChEBI
------

This data source uses the ExcludeFieldsById class with the "chebi.xrefs.intenz", "chebi.xrefs.rhea", "chebi.xrefs.uniprot", "chebi.xrefs.sabio_rk", and "chebi.xrefs.patent" fields.  Please see the ExcludeFieldsById section below.  The `exclusion_ids.py <https://github.com/biothings/mychem.info/blob/master/src/hub/dataload/sources/chebi/exclusion_ids.py>`_ file affects 142 documents.

ChEMBL
------

DrugBank
--------

This data source uses the ExcludeFieldsById class with the "drugbank.drug_interactions", "drugbank.products", "drugbank.mixtures" fields.  Please see the ExcludeFieldsById section below.  The `exclusion_ids.py <https://github.com/biothings/mychem.info/blob/master/src/hub/dataload/sources/drugbank/exclusion_ids.py>`_ file affects 7 documents.

DrugCentral
-----------

ginas
-----

NDC
---

This data source uses the ExcludeFieldsById class with the "ndc" and "ndc.productndc" fields.  Please see the ExcludeFieldsById section below.  The `exclusion_ids.py <https://github.com/biothings/mychem.info/blob/master/src/hub/dataload/sources/ndc/exclusion_ids.py>`_ file affects 4 documents.

PharmGKB
--------

PubChem
-------

SIDER
------

Sider elements (doc['sider']) which are natively represented as a list are sorted by the field 'sider.side_effect.frequency'.  From that sorted list, only the top 2000 elements are kept in the document.  The sorting function is defined in 'sider_parser.py'.  Documents that do not have a 'sider.side_effect.frequency' field are placed at the top of the list.

UNII
----

ExcludeFieldsById
-----------------

This class is being used by several data sources to exclude large fields for common chemicals.  Identifiers for these common chemicals are recorded in the 'exclusion_ids.py' file within the data source.  For these documents, fields were excluded if their lists were of size 1000 or greater; this size can be modified as a parameter.
