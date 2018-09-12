import os
import glob
import zipfile
import pymongo

from .chebi_parser import load_data
from hub.dataload.uploader import BaseDrugUploader
from biothings.utils.mongo import get_src_db
import biothings.hub.dataload.storage as storage


SRC_META = {
        "url": 'https://www.ebi.ac.uk/chebi/',
        "license_url" : "https://www.ebi.ac.uk/about/terms-of-use",
        "license_url_short" : "https://goo.gl/FJpLMf"
        }


class ChebiUploader(BaseDrugUploader):

    name = "chebi"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        self.logger.info("Load data from '%s'" % data_folder)
        input_file = os.path.join(data_folder,"ChEBI_complete.sdf")
        # get others source collection for inchi key conversion
        drugbank_col = get_src_db()["drugbank"]
        assert drugbank_col.count() > 0, "'drugbank' collection is empty (required for inchikey " + \
                "conversion). Please run 'drugbank' uploader first"
        chembl_col = get_src_db()["chembl"]
        assert chembl_col.count() > 0, "'chembl' collection is empty (required for inchikey " + \
                "conversion). Please run 'chembl' uploader first"
        assert os.path.exists(input_file), "Can't find input file '%s'" % input_file
        return load_data(input_file,drugbank_col,chembl_col)

    def post_update_data(self, *args, **kwargs):
        for idxname in ["chebi.chebi_id"]:
            self.logger.info("Indexing '%s'" % idxname)
            # background=true or it'll lock the whole database...
            self.collection.create_index([(idxname,pymongo.HASHED)],background=True)

    @classmethod
    def get_mapping(klass):
        mapping = {
                "chebi": {
                    "properties": {
                        "citexplore_citation_links": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "pdbechem_database_links": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "sabio_rk_database_links": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "chinese_abstracts_citation_links": {
                            "type": "integer"
                            },
                        "last_modified": {
                            "type": "string"
                            },
                        "smiles": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "agricola_citation_links": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "inn": {
                            "type": "string"
                            },
                        "lipid_maps_class_database_links": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "pubchem_database_links": {
                            "properties": {
                                "SID": {
                                    "type": "integer"
                                    },
                                "CID": {
                                    "type": "integer"
                                    }
                                }
                            },
                        "intenz_database_links": {
                            "type": "string"
                            },
                        "formulae": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "inchikey": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "ymdb_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "drugbank_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "synonyms": {
                                "type": "string"
                                },
                        "wikipedia_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "chebi_name": {
                                "type": "string"
                                },
                        "patent_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "beilstein_registry_numbers": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "hmdb_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "uniprot_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "iupac_names": {
                                "type": "string"
                                },
                        "monoisotopic_mass": {
                                "type": "float"
                                },
                        "metacyc_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "intact_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "cas_registry_numbers": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "gmelin_registry_numbers": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "pubmed_central_citation_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "secondary_chebi_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "um_bbd_compid_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "lipid_maps_instance_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "mass": {
                                "type": "float"
                                },
                        "star": {
                                "type": "integer"
                                },
                        "kegg_drug_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "lincs_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "arrayexpress_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "pubmed_citation_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "ecmdb_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "molbase_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "kegg_glycan_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "chebi_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "resid_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "inchi": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "kegg_compound_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "definition": {
                                "type": "string"
                                },
                        "biomodels_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "come_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "rhea_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "brand_names": {
                                "type": "string"
                                },
                        "reactome_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "charge": {
                                "type": "integer"
                                },
                        "knapsack_database_links": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                }
                        }
            }
        }

        return mapping


