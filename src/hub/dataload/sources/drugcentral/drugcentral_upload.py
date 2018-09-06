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
                                    "type": "text"
                                    },
                                "cas_rn": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "inn": {
                                    "type": "text"
                                    },
                                "inchi": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "inchikey": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
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
                                    "analyzer": "string_lowercase",
                                    "type": "text"
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
                                        "type": "text"
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
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                }
                                            }
                                        },
                                    "fda_epc": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                }
                                            }
                                        },
                                    "fda_pe": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                }
                                            }
                                        },
                                    "fda_chemical/ingredient": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                }
                                            }
                                        },
                                    "fda_moa": {
                                        "properties": {
                                            "description": {
                                                "type": "text"
                                                },
                                            "code": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                }
                                            }
                                        },
                                    "mesh_pa": {
                                            "properties": {
                                                "description": {
                                                    "type": "text"
                                                    },
                                                "code": {
                                                    "analyzer": "string_lowercase",
                                                    "type": "text"
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
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "company": {
                                    "type": "text"
                                    },
                                "orphan": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
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
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "indication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "text"
                                            },
                                        "cui_semantic_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "contraindication": {
                                    "properties": {
                                        "snomed_full_name": {
                                            "type": "text"
                                            },
                                        "cui_semantic_type": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "concept_name": {
                                            "type": "text"
                                            },
                                        "umls_cui": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "snomed_concept_id": {
                                            "type": "integer"
                                            }
                                        }
                                    },
                                "symptomatic treatment": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                },
                                            "snomed_concept_id": {
                                                "type": "integer"
                                                }
                                            }
                                        },
                                "off-label use": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                },
                                            "snomed_concept_id": {
                                                "type": "integer"
                                                }
                                            }
                                        },
                                "diagnosis": {
                                        "properties": {
                                            "snomed_full_name": {
                                                "type": "text"
                                                },
                                            "cui_semantic_type": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
                                                },
                                            "concept_name": {
                                                "type": "text"
                                                },
                                            "umls_cui": {
                                                "analyzer": "string_lowercase",
                                                "type": "text"
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
                                            "analyzer": "string_lowercase",
                                            "type": "text"
                                            },
                                        "swissprot_entry": {
                                            "analyzer": "string_lowercase",
                                            "type": "text"
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
                            "type": "text"
                            },
                    "xref": {
                            "properties": {
                                "pubchem_cid": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "nui": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "nddf": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "pdb_chem_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "kegg_drug": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "secondary_cas_rn": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "vandf": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "ndfrt": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "chembl_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "drugbank_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "inn_id": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "mmsl": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "snomedct_us": {
                                    "analyzer": "string_lowercase",
                                    "type": "text"
                                    },
                                "mesh_supplemental_record_ui": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "unii": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "umlscui": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "chebi": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "mesh_descriptor_ui": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "vuid": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "iuphar_ligand_id": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        },
                                "rxnorm": {
                                        "analyzer": "string_lowercase",
                                        "type": "text"
                                        }
                                }
                    }
                }
            }
        }

        return mapping


"""
