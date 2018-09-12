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
                            "type": "text"
                            },
                        "id": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "iupac": {
                            "type": "text"
                            },
                        "inchi": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "definition": {
                            "type": "text"
                            },
                        "star": {
                            "type": "integer"
                            },
                        "smiles": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "last_modified": {
                            "type": "text"
                            },
                        "inn": {
                            "type": "text"
                            },
                        "xref": {
                            "properties": {
                                "molbase": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "resid": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "come": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
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
                                    "type": "text"
                                    },
                                "wikipedia": {
                                    "properties": {
                                        "url_stub": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            }
                                        }
                                    },
                                "metacyc": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "biomodels": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "reactome": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "um_bbd_compid": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "lincs": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "uniprot": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "sabio_rk": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "patent": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "pdbechem": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "arrayexpress": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "cas": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "lipid_maps_class": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "kegg_drug": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "knapsack": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "lipid_maps_instance": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "intenz": {
                                        "type": "text"
                                        },
                                "kegg_glycan": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "ecmdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "hmdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "kegg_compound": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "ymdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "drugbank": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "rhea": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "gmelin": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "intact": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
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
                    "type": "text"
                    },
            "formulae": {
                    "analyzer": "string_lowercase",
                    "type": "text"
                    },
            "inchikey": {
                    "analyzer": "string_lowercase",
                    "type": "text"
                    },
            "name": {
                    "type": "text"
                    },
            "charge": {
                    "type": "integer"
                    },
            "synonyms": {
                    "type": "text"
                    },
            "citation": {
                    "properties": {
                        "pubmed": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "agricola": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "pmc": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            },
                        "chinese_abstracts": {
                            "type": "integer"
                            },
                        "citexplore": {
                            "analyzer": "string_lowercase",
                            "type": "text"
                            }
                        }
                    }
                }
            }
        }
        return mapping


