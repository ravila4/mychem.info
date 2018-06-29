import biothings.hub.dataload.uploader as uploader

class DrugCentralUploader(uploader.DummySourceUploader):

    name = "drugcentral"
    __metadata__ = {
            "src_meta" : {
                "url" : "http://drugcentral.org/",
                "license_url" : "http://drugcentral.org/privacy",
                "license_url_short" : "https://goo.gl/QDNyNe",
                "license" : "CC BY-SA 4.0",
                }
            }

    @classmethod
    def get_mapping(klass):
        mapping = {
            "drugcentral": {
                "properties": {
                    "approval": {
                        "properties": {
                            "company": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "date": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "agency": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            }
                        }
                    },
                    "fda_adverse_event": {
                        "properties": {
                            "drug_ae": {
                                "type": "integer"
                            },
                            "drug_no_ae": {
                                "type": "integer"
                            },
                            "no_drug_ae": {
                                "type": "integer"
                            },
                            "no_drug_no_ar": {
                                "type": "integer"
                            },
                            "level": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "meddra_code": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "meddra_term": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "llr": {
                                "type": "float"
                            },
                            "llr_threshold": {
                                "type": "float"
                            }
                        }
                    }
                    "bioactivity": {
                        "properties": {
                            "act_source": {
                                "type": "string"
                            },
                            "act_type": {
                                "type": "string"
                            },
                            "act_value": {
                                "analyzer": "float"
                            },
                            "action_type": {
                                "type": "string"
                            },
                            "uniprot": {
                                "properties": {
                                    "gene_symbol": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                    },
                                    "swissprot_entry": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                    },
                                    "uniprot_id": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                    }
                                }
                            },
                            "moa": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "target_name": {
                                "type": "string"
                            },
                            "target_class": {
                                "type": "string"
                            }
                        }
                    },
                    "drug_dosage": {
                        "properties": {
                            "dose": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "route": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "unit": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            }
                        }
                    },
                    "drug_use": {
                        "properties": {
                            "contraindication": {
                                "properties": {
                                    "concept_name": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "cui_semantic_type": {
                                        "type": "string"
                                    },
                                    "snomed_concept_id": {
                                        "analyzer": "integer"
                                    },
                                    "snomed_full_name": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "umls_cui": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "indication": {
                                "properties": {
                                    "concept_name": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "cui_semantic_type": {
                                        "type": "string"
                                    },
                                    "snomed_concept_id": {
                                        "analyzer": "integer"
                                    },
                                    "snomed_full_name": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "umls_cui": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    },
                    "pharmacology_class": {
                        "properties": {
                            "chebi": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "mesh_pa": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "fda_epc": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "fda_chemical/ingredient": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "fda_moa": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            },
                            "fda_pe": {
                                "properties": {
                                    "description": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    },
                                    "code": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    },
                    "structures": {
                        "properties": {
                            "cas_rn": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "inchi": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "inchikey": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "inn": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "smiles": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            }
                        }
                    },
                    "synonyms": {
                        "type": "string"
                    },
                    "xref": {
                        "properties": {
                            "chebi": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "chembl_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "drugbank_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "inn_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "iuphar_ligand_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "kegg_drug": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "mesh_descriptor_ui": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "mesh_supplemental_record_ui": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "mmsl": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "nddf": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "ndfrt": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "nui": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "pdb_chem_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "pubchem_cid": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "rxnorm": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "secondary_cas_rn": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "snomedct_us": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "umlscui": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "unii": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "vandf": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "vuid": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }

        return mapping


"""