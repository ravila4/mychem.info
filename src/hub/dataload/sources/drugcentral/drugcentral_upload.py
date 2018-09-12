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
                        "structures": {
                            "properties": {
                                "smiles": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "cas_rn": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "inn": {
                                    "type": "string"
                                    },
                                "inchi": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "inchikey": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                        "fda_adverse_event": {
                            "properties": {
                                "llr": {
                                    "type": "float"
                                    },
                                "meddra_term": {
                                    "type": "string"
                                    },
                                "llr_threshold": {
                                    "type": "float"
                                    },
                                "drug_ae": {
                                    "type": "integer"
                                    },
                                "level": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
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
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                    "route": {
                                        "type": "string"
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
                    "approval": {
                            "properties": {
                                "agency": {
                                    "type": "string"
                                    },
                                "date": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "company": {
                                    "type": "string"
                                    },
                                "orphan": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                    "drug_use": {
                            "properties": {
                                "reduce risk": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "string"
                                            },
                                        "cui_semantic_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "concept_name": {
                                            "type": "string"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "indication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "string"
                                            },
                                        "cui_semantic_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "concept_name": {
                                            "type": "string"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "contraindication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "string"
                                            },
                                        "cui_semantic_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "concept_name": {
                                            "type": "string"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "symptomatic treatment": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "string"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "concept_name": {
                                                "type": "string"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "snomed_concept_id": {
                                                "type": "integer"
                                                }
                                            }
                                        },
                                "off-label use": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "string"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "concept_name": {
                                                "type": "string"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "snomed_concept_id": {
                                                "type": "integer"
                                                }
                                            }
                                        },
                                "diagnosis": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "string"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "concept_name": {
                                                "type": "string"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                },
                                            "snomed_concept_id": {
                                                "type": "integer"
                                                }
                                            }
                                        }
                                }
                    },
                    "bioactivity": {
                            "properties": {
                                "organism": {
                                    "type": "string"
                                    },
                                "target_class": {
                                    "type": "string"
                                    },
                                "action_type": {
                                    "type": "string"
                                    },
                                "moa": {
                                    "type": "float"
                                    },
                                "target_name": {
                                    "type": "string"
                                    },
                                "act_type": {
                                    "type": "string"
                                    },
                                "moa_source": {
                                    "type": "string"
                                    },
                                "uniprot": {
                                    "properties": {
                                        "uniprot_id": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "swissprot_entry": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "gene_symbol": {
                                            "type": "string"
                                            }
                                        }
                                    },
                                "act_source": {
                                    "type": "string"
                                    },
                                "act_value": {
                                    "type": "float"
                                    }
                                }
                            },
                    "synonyms": {
                            "type": "string"
                            },
                    "xref": {
                            "properties": {
                                "pubchem_cid": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "nui": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "nddf": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "pdb_chem_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "kegg_drug": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "secondary_cas_rn": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "vandf": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "ndfrt": {
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
                                "mmsl": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "snomedct_us": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "mesh_supplemental_record_ui": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "unii": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "umlscui": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "chebi": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "mesh_descriptor_ui": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "vuid": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "iuphar_ligand_id": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "rxnorm": {
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
