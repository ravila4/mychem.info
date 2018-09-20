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
                        "brand_names": {
                            "type": "string"
                            },
                        "id": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "iupac": {
                            "type": "string"
                            },
                        "inchi": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "definition": {
                            "type": "string"
                            },
                        "star": {
                            "type": "integer"
                            },
                        "smiles": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "last_modified": {
                            "type": "string"
                            },
                        "inn": {
                            "type": "string"
                            },
                        "xref": {
                            "properties": {
                                "molbase": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "resid": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "come": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "pubchem": {
                                    "properties": {
                                        "sid": {
                                            "type": "integer"
                                            },
                                        "cid": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "beilstein": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "wikipedia": {
                                    "properties": {
                                        "url_stub": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            }
                                        }
                                    },
                                "metacyc": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "biomodels": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "reactome": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "um_bbd_compid": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "lincs": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "uniprot": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "sabio_rk": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "patent": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "pdbechem": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "arrayexpress": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "cas": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "lipid_maps_class": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "kegg_drug": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "knapsack": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "lipid_maps_instance": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "intenz": {
                                        "type": "string"
                                        },
                                "kegg_glycan": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "ecmdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "hmdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "kegg_compound": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "ymdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "drugbank": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "rhea": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "gmelin": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "intact": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        }
                                }
            },
            "monoisotopic_mass": {
                    "type": "float"
                    },
            "mass": {
                    "type": "float"
                    },
            "secondary_chebi_id": {
                    "analyzer": "string_lowercase",
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
            "name": {
                    "type": "string"
                    },
            "charge": {
                    "type": "integer"
                    },
            "synonyms": {
                    "type": "string"
                    },
            "citation": {
                    "properties": {
                        "pubmed": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "agricola": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "pmc": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "chinese_abstracts": {
                            "type": "integer"
                            },
                        "citexplore": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            }
                        }
                    }
                }
            }
        }
        return mapping


