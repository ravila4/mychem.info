from .chembl_parser import load_data as _load_data

__METADATA__ = {
    "src_name": 'CHEMBL',
    "src_url": 'https://www.ebi.ac.uk/chembl/',    
    "field": "chembl"
}
CHEMBL_INPUT_URL = 'https://www.ebi.ac.uk/chembl/api/data/molecule.json'

def load_data():
    chembl_data = _load_data(CHEMBL_INPUT_URL)
    return chembl_data

def get_mapping():
    mapping = {
        "chembl": {
            "properties": {
                "max_phase": {  
                    "type":"integer"                    
                },
                "molecule_chembl_id": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "pref_name": {  
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "inchi_key": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "smiles": {  
                    "type":"string" ,
                    "analyzer":"string_lowercase"
                },
                "inchi": {  
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "molecule_type": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "chebi_par_id": {   
                    "type":"string"
                },
                "first_approval": {  
                    "type":"string"                    
                },
                "topical": {  
                    "type":"boolean"
                    
                },
                "prodrug":{  
                    "type":"integer"
                },
                "usan_stem_definition": {
                     "type":"string",
                     "analyzer":"string_lowercase"
                },
                "chirality": {  
                    "type":"integer"
                },
                "usan_stem": { 
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "usan_substem": { 
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "usan_year": { 
                    "type":"string"                    
                },
                "first_in_class": {
                    "type":"integer"
                },
                "oral": {  
                    "type":"boolean"                    
                },
                "parenteral": { 
                    "type":"boolean"                    
                },
                "dosed_ingredient": { 
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "natural_product": {  
                    "type":"integer"
                },
                "polymer_flag": {  
                    "type":"boolean"                    
                },
                "therapeutic_flag": {
                    "type":"boolean"                    
                },
                "structure_type": {  
                    "type":"string",
                    "analyzer":"string_lowercase"                                      
                },
                "helm_notation": {
                    "type":"string"
                },
                "biotherapeutic": {
                    "properties" : {
                        "biocomponents" : {
                            "properties" : {
                                "component_id": {
                                    "type":"integer"
                                    },
                                "description" : {
                                   "type":"string"
                                   },
                                "component_type" : {
                                    "type":"string"
                                    },
                                "sequence" : {
                                    "type":"string"
                                    },
                                "organism" : {
                                    "type":"string"
                                    },
                                "tax_id" : {
                                   "type":"integer"
                                   }
                                }
                            },
                        "helm_notation" : {
                            "type":"string"
                            },
                        "molecule_chembl_id" : {
                            "type":"string"
                            },
                        "description" : {
                            "type":"string"
                            }
                        }                         
                },
                "black_box_warning": { 
                    "type":"boolean"                                       
                },
                "availability_type": { 
                    "type":"integer"
                },
                "inorganic_flag": { 
                    "type":"boolean"                    
                },
                "indication_class": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "atc_classifications": {
                    "type":"string" 
                },
                "molecule_synonyms": { 
                    "properties": {
                        "synonyms": {
                            "type":"string"                            
                        },
                        "syn_type": {
                            "type":"string"                            
                        }
                    }
                },
                "molecule_hierarchy": {
                    "properties": {
                        "molecule_chembl_id": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "parent_chembl_id": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        }
                    }
                },
                "molecule_properties": {
                    "properties": {
                        "num_ro5_violations": {
                            "type":"integer"
                        },
                        "med_chem_friendly": {  
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "mw_freebase": {
                            "type":"float"
                        },
                        "full_molformula": { 
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "alogp": {
                            "type":"float"
                        },
                        "heavy_atoms": {
                            "type":"integer"
                        },
                        "num_alerts": {
                            "type":"integer"
                        },
                        "acd_logd": {
                            "type":"float"
                        },
                        "psa": {
                            "type":"float"
                        },
                        "hba": {
                            "type":"float"
                        },
                        "molecular_species": { 
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "mw_monoisotopic": {
                            "type":"float"
                        },
                        "ro3_pass": { 
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "aromatic_rings": {
                            "type":"integer"
                        },
                        "full_mwt": {  
                            "type":"float"
                        },
                        "acd_most_apka": {
                            "type":"float"
                        },
                        "rtb": {
                            "type":"integer"
                        },
                        "acd_logp": {
                            "type":"float"
                        },
                        "qed_weighted": {
                            "type":"float"
                        },
                        "hbd": {
                            "type":"integer"
                        },
                        "acd_most_bpka": {
                            "type":"float"
                        }                        
                    }
                }             
            }
        }
    }
    return mapping

