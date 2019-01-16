from hub.dataload.uploader import BaseDrugUploader
from biothings.utils.mongo import get_src_conn

from hub.datatransform.keylookup import MyChemKeyLookup


class DrugCentralUploader(BaseDrugUploader):

    src_col_name = "drugcentral"
    name = "drugcentral_dt"

    __metadata__ = {
            "src_meta" : {
                "url" : "http://drugcentral.org/",
                "license_url" : "http://drugcentral.org/privacy",
                "license_url_short" : "http://bit.ly/2SeEhUy",
                "license" : "CC BY-SA 4.0",
                }
            }

    keylookup = MyChemKeyLookup(
            [('inchikey', 'drugcentral.structures.inchikey'),
             ('unii', 'drugcentral.xref.unii'),
             # other keys are present but not currently used by keylookup
             ('inchi', 'drugcentral.structures.inchi'),
             ('drugbank', 'drugcentral.xrefs.drugbank_id'),
             ('chebi', 'drugcentral.xrefs.chebi'),
             ('chembl', 'drugcentral.xrefs.chembl_id'),
             ('pubchem', 'drugcentral.xrefs.pubchem_cid')],
             # ('drugname', 'drugcentral.synonyms')], # unhashable type - list
            copy_from_doc=True,
            debug=["CHEMBL1743070"]
            )

    def load_data(self, data_folder):
        # read data from the source collection
        src_col = self.db[self.src_col_name]
        def load_data():
            yield from src_col.find()

        # perform keylookup on source collection
        return self.keylookup(load_data)()

    @classmethod
    def get_mapping(klass):
        mapping = {
                "drugcentral": {
                    "properties": {
                        "structures": {
                            "properties": {
                                "smiles": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "cas_rn": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "inn": {
                                    "type": "text",
                                    'copy_to': ['all'],
                                    },
                                "inchi": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "inchikey": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    }
                                }
                            },
                        "fda_adverse_event": {
                            "properties": {
                                "llr": {
                                    "type": "float"
                                    },
                                "meddra_term": {
                                    "type": "text"
                                    },
                                "llr_threshold": {
                                    "type": "float"
                                    },
                                "drug_ae": {
                                    "type": "integer"
                                    },
                                "level": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "drug_no_ae": {
                                    "type": "integer"
                                    },
                                "no_drug_no_ar": {
                                    "type": "integer"
                                    },
                                "meddra_code": {
                                    "type": "integer"
                                    },
                                "no_drug_ae": {
                                    "type": "integer"
                                    }
                                }
                            },
                        "drug_dosage": {
                                "properties": {
                                    "unit": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                    "route": {
                                        "type": "text"
                                        },
                                    "dosage": {
                                        "type": "float"
                                        }
                                    }
                                },
                        "pharmacology_class": {
                                "properties": {
                                    "chebi": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                }
                                            }
                                        },
                                    "fda_epc": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                }
                                            }
                                        },
                                    "fda_pe": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                }
                                            }
                                        },
                                    "fda_chemical/ingredient": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                }
                                            }
                                        },
                                    "fda_moa": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                }
                                            }
                                        },
                                    "mesh_pa": {
                                            "properties": {
                                                "description": {
                                                    "type": "text"
                                                    },
                                                "code": {
                                                    "normalizer": "keyword_lowercase_normalizer",
                                                    "type": "keyword",
                                                    }
                                                }
                                            }
                                    }
                    },
                    "approval": {
                            "properties": {
                                "agency": {
                                    "type": "text"
                                    },
                                "date": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "company": {
                                    "type": "text"
                                    },
                                "orphan": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    }
                                }
                            },
                    "drug_use": {
                            "properties": {
                                "reduce risk": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "text"
                                            },
                                        "cui_semantic_type": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "snomed_concept_id": {
                                            "type": "long"
                                            }
                                        }
                                    },
                                "indication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "text"
                                            },
                                        "cui_semantic_type": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "snomed_concept_id": {
                                            "type": "long"
                                            }
                                        }
                                    },
                                "contraindication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "text"
                                            },
                                        "cui_semantic_type": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "snomed_concept_id": {
                                            "type": "long"
                                            }
                                        }
                                    },
                                "symptomatic treatment": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "snomed_concept_id": {
                                                "type": "long"
                                                }
                                            }
                                        },
                                "off-label use": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "snomed_concept_id": {
                                                "type": "long"
                                                }
                                            }
                                        },
                                "diagnosis": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "normalizer": "keyword_lowercase_normalizer",
                                                "type": "keyword",
                                                },
                                            "snomed_concept_id": {
                                                "type": "long"
                                                }
                                            }
                                        }
                                }
                    },
                    "bioactivity": {
                            "properties": {
                                "organism": {
                                    "type": "text"
                                    },
                                "target_class": {
                                    "type": "text"
                                    },
                                "action_type": {
                                    "type": "text"
                                    },
                                "moa": {
                                    "type": "float"
                                    },
                                "target_name": {
                                    "type": "text"
                                    },
                                "act_type": {
                                    "type": "text"
                                    },
                                "moa_source": {
                                    "type": "text"
                                    },
                                "uniprot": {
                                    "properties": {
                                        "uniprot_id": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "swissprot_entry": {
                                            "normalizer": "keyword_lowercase_normalizer",
                                            "type": "keyword",
                                            },
                                        "gene_symbol": {
                                            "type": "text"
                                            }
                                        }
                                    },
                                "act_source": {
                                    "type": "text"
                                    },
                                "act_value": {
                                    "type": "float"
                                    }
                                }
                            },
                    "synonyms": {
                            "type": "text",
                            'copy_to': ['all'],
                            },
                    "xrefs": {
                            "properties": {
                                "pubchem_cid": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "nui": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "nddf": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "pdb_chem_id": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "kegg_drug": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "secondary_cas_rn": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "vandf": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "ndfrt": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "chembl_id": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "drugbank_id": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "inn_id": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "mmsl": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "snomedct_us": {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "mesh_supplemental_record_ui": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "unii": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "umlscui": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "chebi": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "mesh_descriptor_ui": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "vuid": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "iuphar_ligand_id": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                "rxnorm": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        }
                                }
                    }
                }
            }
        }

        return mapping

