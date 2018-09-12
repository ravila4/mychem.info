import os
import glob
import zipfile
import pymongo

from .chembl_parser import load_data
from hub.dataload.uploader import BaseDrugUploader
from biothings.hub.dataload.uploader import ParallelizedSourceUploader


SRC_META = {
        "url": 'https://www.ebi.ac.uk/chembl/',
        "license_url" : "https://www.ebi.ac.uk/about/terms-of-use",
        "license_url_short" : "https://goo.gl/FJpLMf"
        }


class ChemblUploader(BaseDrugUploader,ParallelizedSourceUploader):

    name = "chembl"
    __metadata__ = {"src_meta" : SRC_META}

    MOLECULE_PATTERN = "molecule.*.json"

    def jobs(self):
        # this will generate arguments for self.load.data() method, allowing parallelization
        json_files = glob.glob(os.path.join(self.data_folder,self.__class__.MOLECULE_PATTERN))
        return [(f,) for f in json_files]

    def load_data(self,input_file):
        self.logger.info("Load data from file '%s'" % input_file)
        return load_data(input_file)

    def post_update_data(self, *args, **kwargs):
        for idxname in ["chembl.chebi_par_id","chembl.inchi"]:
            self.logger.info("Indexing '%s'" % idxname)
            # background=true or it'll lock the whole database...
            self.collection.create_index([(idxname,pymongo.HASHED)],background=True)

    @classmethod
    def get_mapping(klass):
        mapping = {
                "chembl": {
                    "properties": {
                        "biotherapeutic": {
                            "properties": {
                                "helm_notation": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "description": {
                                    "type": "string"
                                    },
                                "biocomponents": {
                                    "properties": {
                                        "organism": {
                                            "type": "string"
                                            },
                                        "tax_id": {
                                            "type": "integer"
                                            },
                                        "sequence": {
                                            "type": "string"
                                            },
                                        "component_id": {
                                            "type": "integer"
                                            },
                                        "description": {
                                            "type": "string"
                                            },
                                        "component_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            }
                                        }
                                    },
                                "molecule_chembl_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                        "therapeutic_flag": {
                            "type": "boolean"
                            },
                        "usan_stem": {
                            "type": "string"
                            },
                        "molecule_chembl_id": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "molecule_properties": {
                            "properties": {
                                "heavy_atoms": {
                                    "type": "integer"
                                    },
                                "acd_most_bpka": {
                                    "type": "float"
                                    },
                                "mw_freebase": {
                                    "type": "float"
                                    },
                                "num_ro5_violations": {
                                    "type": "integer"
                                    },
                                "molecular_species": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "qed_weighted": {
                                    "type": "float"
                                    },
                                "ro3_pass": {
                                    "type": "boolean"
                                    },
                                "full_mwt": {
                                    "type": "float"
                                    },
                                "num_lipinski_ro5_violations": {
                                    "type": "integer"
                                    },
                                "rtb": {
                                    "type": "integer"
                                    },
                                "psa": {
                                    "type": "float"
                                    },
                                "alogp": {
                                    "type": "float"
                                    },
                                "hbd": {
                                    "type": "integer"
                                    },
                                "acd_most_apka": {
                                    "type": "float"
                                    },
                                "hbd_lipinski": {
                                    "type": "integer"
                                    },
                                "acd_logp": {
                                    "type": "float"
                                    },
                                "full_molformula": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "aromatic_rings": {
                                        "type": "integer"
                                        },
                                "hba_lipinski": {
                                        "type": "integer"
                                        },
                                "mw_monoisotopic": {
                                        "type": "float"
                                        },
                                "hba": {
                                        "type": "integer"
                                        },
                                "acd_logd": {
                                        "type": "float"
                                        }
                                }
                        },
                        "helm_notation": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "max_phase": {
                                "type": "integer"
                                },
                        "inorganic_flag": {
                                "type": "integer"
                                },
                        "usan_stem_definition": {
                                "type": "string"
                                },
                        "dosed_ingredient": {
                                "type": "boolean"
                                },
                        "chebi_par_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "withdrawn_reason": {
                                "type": "string"
                                },
                        "molecule_hierarchy": {
                                "properties": {
                                    "parent_chembl_id": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                    "molecule_chembl_id": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        }
                                    }
                                },
                        "prodrug": {
                                "type": "integer"
                                },
                        "withdrawn_flag": {
                                "type": "boolean"
                                },
                        "usan_year": {
                                "type": "integer"
                                },
                        "parenteral": {
                                "type": "boolean"
                                },
                        "black_box_warning": {
                                "type": "integer"
                                },
                        "polymer_flag": {
                                "type": "boolean"
                                },
                        "molecule_synonyms": {
                                "properties": {
                                    "molecule_synonym": {
                                        "type": "string"
                                        },
                                    "synonyms": {
                                        "type": "string"
                                        },
                                    "syn_type": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        }
                                    }
                                },
                        "atc_classifications": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "molecule_type": {
                                "type": "string"
                                },
                        "first_in_class": {
                                "type": "integer"
                                },
                        "inchi": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "structure_type": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "withdrawn_class": {
                                "type": "string"
                                },
                        "inchi_key": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "topical": {
                                "type": "boolean"
                                },
                        "oral": {
                                "type": "boolean"
                                },
                        "xref": {
                                "properties": {
                                    "drugcentral": {
                                        "properties": {
                                            "id": {
                                                "type": "integer"
                                                },
                                            "name": {
                                                "type": "string"
                                                }
                                            }
                                        },
                                    "tg-gates": {
                                        "properties": {
                                            "id": {
                                                "type": "integer"
                                                },
                                            "name": {
                                                "type": "string"
                                                }
                                            }
                                        },
                                    "wikipedia": {
                                        "properties": {
                                            "url_stub": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                }
                                            }
                                        },
                                    "dailymed": {
                                        "properties": {
                                            "name": {
                                                "type": "string"
                                                }
                                            }
                                        },
                                    "pubchem": {
                                        "properties": {
                                            "sid": {
                                                "type": "integer"
                                                }
                                            }
                                        }
                                    }
                                },
                        "chirality": {
                                "type": "integer"
                                },
                        "usan_substem": {
                                "type": "string"
                                },
                        "indication_class": {
                                "type": "string"
                                },
                        "withdrawn_country": {
                                "type": "string"
                                },
                        "withdrawn_year": {
                                "type": "integer"
                                },
                        "availability_type": {
                                "type": "integer"
                                },
                        "smiles": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                                },
                        "natural_product": {
                                "type": "integer"
                                },
                        "pref_name": {
                                "type": "string"
                                },
                        "first_approval": {
                                "type": "integer"
                                }
                        }
                }
        }

        return mapping


