import os
import glob
import pymongo

from .drugbank_parser import load_data
from hub.dataload.uploader import BaseDrugUploader
import biothings.hub.dataload.storage as storage
from biothings.utils.common import unzipall


SRC_META = {
        "url" : "http://www.drugbank.ca",
        "license_url" : "https://www.drugbank.ca/releases/latest",
        "license_url_short" : "https://goo.gl/kvVASD",
        "license" : "CC BY-NC 4.0",
        }


class DrugBankUploader(BaseDrugUploader):

    name = "drugbank"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        xmlfiles = glob.glob(os.path.join(data_folder,"*.xml"))
        if not xmlfiles:
            self.logger.info("Unzipping drugbank archive")
            unzipall(data_folder)
            self.logger.info("Load data from '%s'" % data_folder)
            xmlfiles = glob.glob(os.path.join(data_folder,"*.xml"))
        assert len(xmlfiles) == 1, "Expecting one xml file, got %s" % repr(xmlfiles)
        input_file = xmlfiles.pop()
        assert os.path.exists(input_file), "Can't find input file '%s'" % input_file
        return load_data(input_file)

    def post_update_data(self, *args, **kwargs):
        for idxname in ["drugbank.drugbank_id","drugbank.chebi","drugbank.inchi"]:
            self.logger.info("Indexing '%s'" % idxname)
            # background=true or it'll lock the whole database...
            self.collection.create_index([(idxname,pymongo.HASHED)],background=True)
        # hashed index won"t support arrays, values are small enough to standard
        self.collection.create_index("drugbank.products.ndc_product_code")

    @classmethod
    def get_mapping(klass):
        mapping = {
                "drugbank": {
                    "properties": {
                        "drugs_com": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "guide_to_pharmacology": {
                            "type": "integer"
                            },
                        "groups": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "uniprotkb": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "pharmacology": {
                            "properties": {
                                "protein_binding": {
                                    "type": "string"
                                    },
                                "indication": {
                                    "type": "string"
                                    },
                                "absorption": {
                                    "type": "string"
                                    },
                                "clearance": {
                                    "type": "string"
                                    },
                                "route_of_elimination": {
                                    "type": "string"
                                    },
                                "volume_of_distribution": {
                                    "type": "string"
                                    },
                                "snp_adverse_drug_reactions": {
                                    "properties": {
                                        "reaction": {
                                            "properties": {
                                                "protein-name": {
                                                    "type": "string"
                                                    },
                                                "gene-symbol": {
                                                    "analyzer": "string_lowercase",
                                                    "type": "string"
                                                    },
                                                "pubmed-id": {
                                                    "type": "integer"
                                                    },
                                                "rs-id": {
                                                    "analyzer": "string_lowercase",
                                                    "type": "string"
                                                    },
                                                "description": {
                                                    "type": "string"
                                                    },
                                                "allele": {
                                                    "type": "string"
                                                    },
                                                "uniprot-id": {
                                                    "analyzer": "string_lowercase",
                                                    "type": "string"
                                                    },
                                                "adverse-reaction": {
                                                    "type": "string"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                "toxicity": {
                                        "type": "string"
                                        },
                                "pharmacodynamics": {
                                        "type": "string"
                                        },
                                "snp_effects": {
                                        "properties": {
                                            "effect": {
                                                "properties": {
                                                    "defining-change": {
                                                        "type": "string"
                                                        },
                                                    "protein-name": {
                                                        "type": "string"
                                                        },
                                                    "rs-id": {
                                                        "analyzer": "string_lowercase",
                                                        "type": "string"
                                                        },
                                                    "pubmed-id": {
                                                        "type": "integer"
                                                        },
                                                    "description": {
                                                        "type": "string"
                                                        },
                                                    "allele": {
                                                        "type": "string"
                                                        },
                                                    "uniprot-id": {
                                                        "analyzer": "string_lowercase",
                                                        "type": "string"
                                                        },
                                                    "gene-symbol": {
                                                        "analyzer": "string_lowercase",
                                                        "type": "string"
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                "half_life": {
                                        "type": "string"
                                        },
                                "description": {
                                        "type": "string"
                                        },
                                "metabolism": {
                                        "type": "string"
                                        },
                                "affected_organisms": {
                                        "type": "string"
                                        },
                                "mechanism_of_action": {
                                        "type": "string"
                                        }
                                }
                    },
                    "rxlist": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "pubchem_substance": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "pubchem_compound": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "transporters": {
                            "properties": {
                                "organism": {
                                    "type": "string"
                                    },
                                "id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    },
                                "known_action": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "uniprot": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "source": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "general_function": {
                                    "type": "string"
                                    },
                                "actions": {
                                    "type": "string"
                                    },
                                "specific_function": {
                                    "type": "string"
                                    }
                                }
                            },
                    "food_interactions": {
                            "type": "string"
                            },
                    "inchi_key": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "synonyms": {
                            "type": "string"
                            },
                    "patents": {
                            "properties": {
                                "country": {
                                    "type": "string"
                                    },
                                "approved": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "number": {
                                    "type": "string"
                                    },
                                "expires": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "pediatric-extension": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                    "pdrhealth": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "iupac": {
                            "type": "string"
                            },
                    "pharmgkb": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "inchi": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "mixtures": {
                            "properties": {
                                "name": {
                                    "type": "string"
                                    },
                                "ingredients": {
                                    "type": "string"
                                    }
                                }
                            },
                    "manufacturers": {
                            "type": "string"
                            },
                    "iuphar": {
                            "type": "integer"
                            },
                    "smiles": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "pathways": {
                            "properties": {
                                "enzymes": {
                                    "properties": {
                                        "uniprot-id": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            }
                                        }
                                    },
                                "drugs": {
                                    "properties": {
                                        "drugbank-id": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "name": {
                                            "type": "string"
                                            }
                                        }
                                    },
                                "smpdb_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    }
                                }
                            },
                    "international_brands": {
                            "properties": {
                                "company": {
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    }
                                }
                            },
                    "bindingdb": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "dpd": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "predicted_properties": {
                            "properties": {
                                "number_of_rings": {
                                    "type": "integer"
                                    },
                                "smiles": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "h_bond_acceptor_count": {
                                    "type": "integer"
                                    },
                                "logp": {
                                    "type": "float"
                                    },
                                "traditional_iupac_name": {
                                    "type": "string"
                                    },
                                "inchikey": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "h_bond_donor_count": {
                                    "type": "integer"
                                    },
                                "polar_surface_area_(psa)": {
                                    "type": "float"
                                    },
                                "water_solubility": {
                                    "type": "string"
                                    },
                                "rotatable_bond_count": {
                                    "type": "integer"
                                    },
                                "inchi": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "refractivity": {
                                    "type": "float"
                                    },
                                "pka_(strongest_acidic)": {
                                    "type": "float"
                                    },
                                "logs": {
                                    "type": "float"
                                    },
                                "bioavailability": {
                                    "type": "boolean"
                                    },
                                "pka_(strongest_basic)": {
                                    "type": "float"
                                    },
                                "mddr_like_rule": {
                                        "type": "boolean"
                                        },
                                "physiological_charge": {
                                        "type": "integer"
                                        },
                                "polarizability": {
                                        "type": "float"
                                        },
                                "molecular_weight": {
                                        "type": "float"
                                        },
                                "monoisotopic_weight": {
                                        "type": "float"
                                        },
                                "iupac_name": {
                                        "type": "string"
                                        },
                                "rule_of_five": {
                                        "type": "boolean"
                                        },
                                "ghose_filter": {
                                        "type": "boolean"
                                        },
                                "molecular_formula": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        }
                                }
                    },
                    "carriers": {
                            "properties": {
                                "organism": {
                                    "type": "string"
                                    },
                                "id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    },
                                "known_action": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "uniprot": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "source": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "general_function": {
                                    "type": "string"
                                    },
                                "actions": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "specific_function": {
                                    "type": "string"
                                    }
                                }
                            },
                    "categories": {
                            "properties": {
                                "mesh-id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "category": {
                                    "type": "string"
                                    }
                                }
                            },
                    "name": {
                            "type": "string"
                            },
                    "wikipedia": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "kegg_compound": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "weight": {
                            "properties": {
                                "monoisotopic": {
                                    "type": "float"
                                    },
                                "average": {
                                    "type": "float"
                                    }
                                }
                            },
                    "chembl": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "drugbank_id": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "taxonomy": {
                            "properties": {
                                "subclass": {
                                    "type": "string"
                                    },
                                "superclass": {
                                    "type": "string"
                                    },
                                "class": {
                                    "type": "string"
                                    },
                                "substituent": {
                                    "type": "string"
                                    },
                                "description": {
                                    "type": "string"
                                    },
                                "alternative-parent": {
                                    "type": "string"
                                    },
                                "direct-parent": {
                                    "type": "string"
                                    },
                                "kingdom": {
                                    "type": "string"
                                    }
                                }
                            },
                    "products": {
                            "properties": {
                                "otc": {
                                    "type": "boolean"
                                    },
                                "approved": {
                                    "type": "boolean"
                                    },
                                "route": {
                                    "type": "string"
                                    },
                                "fda_application_number": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "started_marketing_on": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "generic": {
                                    "type": "boolean"
                                    },
                                "dosage_form": {
                                    "type": "string"
                                    },
                                "source": {
                                    "type": "string"
                                    },
                                "ended_marketing_on": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "country": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "strength": {
                                    "type": "string"
                                    },
                                "dpd": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    },
                                "ndc_product_code": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                    "food-interactions": {
                            "type": "string"
                            },
                    "packagers": {
                            "type": "string"
                            },
                    "therapeutic_targets_database": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "salts": {
                            "type": "string"
                            },
                    "kegg_drug": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "accession_number": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "enzymes": {
                            "properties": {
                                "organism": {
                                    "type": "string"
                                    },
                                "id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    },
                                "known_action": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "uniprot": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "source": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "general_function": {
                                    "type": "string"
                                    },
                                "actions": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "specific_function": {
                                    "type": "string"
                                    }
                                }
                            },
                    "targets": {
                            "properties": {
                                "organism": {
                                    "type": "string"
                                    },
                                "id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    },
                                "known_action": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "uniprot": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "source": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "general_function": {
                                    "type": "string"
                                    },
                                "actions": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "specific_function": {
                                    "type": "string"
                                    }
                                }
                            },
                    "formula": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "chemspider": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "experimental_properties": {
                            "properties": {
                                "water_solubility": {
                                    "type": "string"
                                    },
                                "logs": {
                                    "type": "float"
                                    },
                                "boiling_point": {
                                    "type": "string"
                                    },
                                "caco2_permeability": {
                                    "type": "float"
                                    },
                                "melting_point": {
                                    "type": "string"
                                    },
                                "pka": {
                                    "type": "string"
                                    },
                                "logp": {
                                    "type": "float"
                                    }
                                }
                            },
                    "drug_interactions": {
                            "properties": {
                                "drugbank-id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "description": {
                                    "type": "string"
                                    },
                                "name": {
                                    "type": "string"
                                    }
                                }
                            },
                    "chebi": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "atc_codes": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "pdb": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                    "ahfs_codes": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            }
                    }
            }
        }

        return mapping

