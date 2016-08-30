__METADATA__ = {
    "src_name": 'PharmGKb',
    "src_url": 'https://www.pharmgkb.org/',    
    "field": "pharmgkb"
}

def get_mapping():
    mapping = {
        "pharmgkb" : {
            "properties" : {
                "pharmgkb_accession_id" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "name" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "generic_names" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "trade_names" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "brand_mixtures" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "type" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "cross_references" : {
                    "properties" : {
                        "chebi" : {
                            "type":"string"
                            },
                        "chemspider" : {
                            "type":"string"
                            },
                        "therapeutic_targets_database" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "pubchem_substance" : {
                            "type":"string"
                            },
                        "web_resource" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "drugbank" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "drugs_product_database" : {
                            "type":"string"
                            },
                        "pubchem_compound" : {
                            "type":"string"
                            },
                        "bindingdb" : {
                            "type":"string"
                            },
                        "kegg_drug" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "fda_drug_label_at_dailymed" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "national_drug_code_directory" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "kegg_compound" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "pdb" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "iuphar_ligand" : {
                            "type":"string"
                            },
                        "clinicaltrials_gov" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "het" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "genbank" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "uniprotkb" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            }
                        }
                    },
                "smiles" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "inchi" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "dosing_guideline" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "external_vocabulary" : {
                    "properties" : {
                        "umls" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "rxnorm" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "ndfrt" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "atc" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "mesh" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            }
                    }
                }
            }
        }
    }
    return mapping
    
