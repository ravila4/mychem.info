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
                            "applicant": {
                                "type": "string"
                            },
                            "date": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            }
                        }
                    },
                    "bioactivity": {
                        "properties": {
                            "act_comment": {
                                "type": "string"
                            },
                            "act_source": {
                                "type": "string"
                            },
                            "act_type": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "act_value": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "action_type": {
                                "type": "string"
                            },
                            "gene_name": {
                                "type": "string"
                            },
                            "moa": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "moa_source": {
                                "type": "string"
                            },
                            "swissprot": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "target": {
                                "type": "string"
                            },
                            "target_class": {
                                "type": "string"
                            },
                            "uniprot_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            }
                        }
                    },
                    "drug_dosage": {
                        "properties": {
                            "atc_code": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
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
                            "relation": {
                                "type": "string"
                            },
                            "snomed_id": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "snomed_name": {
                                "type": "string"
                            }
                        }
                    },
                    "pharmacology_action": {
                        "properties": {
                            "class_code": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "source": {
                                "analyzer": "string_lowercase",
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            }
                        }
                    },
                    "struct_id": {
                        "analyzer": "string_lowercase",
                        "type": "string"
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
