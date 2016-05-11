from .drugbank_parser import load_data as _load_data

__METADATA__ = {
    "src_name": 'DRUGBANK',
    "src_url": 'http://www.drugbank.ca/',    
    "field": "drugbank"
}

DRUGBANK_INPUT_FILE = '/home/jadesara/ENV/drugbank/drugbank.xml'

def load_data():
    drugbank_data = _load_data(DRUGBANK_INPUT_FILE)
    return drugbank_data
    
def get_mapping():    
    mapping = {
        "drugbank": {
            "properties": {
                "name": {
                    "type":"string"
                },
                "ndc_directory": {  
                    "type":"string"                    
                },
                "cas": {  
                    "type":"string"
                },
                "kegg": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "uniprotkb": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "pharmagkb": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "wikipedia": {
                    "type":"string"
                },
                "dpd": {
                    "type":"string"
                },
                "groups": {
                    "type":"string"
                },
                "fasta_sequences": { 
                    "type":"string"
                },                
                "ahfs_code": {  
                    "type":"string"
                },
                "smiles": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "inchi_key": { 
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "inchi": {
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "iupac": {
                    "type":"string"
                },
                "synonyms": {  
                    "type":"string"
                },
                "weight": {
                    "properties": {
                        "average": {
                            "type":"float"                            
                        },
                        "monoisotopic": {
                            "type":"float"
                        }                        
                    }
                },
                "accession_number": {  
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "formula": {  
                    "type":"string",
                    "analyzer":"string_lowercase"
                },
                "drug_interaction": {  
                    "properties": {
                        "description": {
                            "type":"string",                            
                        },
                        "drugbank-id": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "name": {
                            "type":"string" ,
                            "analyzer":"string_lowercase"
                        }
                    }
                },
                "food_interaction": {  
                    "type":"string"                                        
                } ,             
                "pharmacology": {
                    "properties": {
                        "toxicity": {
                            "type":"string"
                        },
                        "protein_binding": {
                            "type":"string"
                        },
                        "description": {
                            "type":"string"                    
                        },
                        "absorption": {
                            "type":"string"
                        },
                        "pharmacodynamics": {
                            "type":"string"
                        },
                        "affected_organisms": { 
                            "type":"string" 
                        },
                        "mechanism_of_action": {
                            "type":"string"
                        },
                        "route_of_elimination": {
                            "type":"string"
                        },
                        "half_life": {
                            "type":"string"
                        },
                        "indication": {
                            "type":"string"
                        },
                        "volume_of_distribution": {
                            "type":"string"
                        },
                        "clearance": {
                            "type":"string"
                        },
                        "metabolism": {
                            "type":"string"
                        }                       
                    }
                },
                "experimental_properties": {
                    "properties": {
                        "melting_point": {  
                            "type":"string"
                        },
                        "isoelectric_point": {
                            "type":"float"                            
                        },
                        "molecular_formula": { 
                            "type":"string"
                        },
                        "hydrophobicity": {
                            "type":"float"
                        },
                        "molecular_weight": {
                            "type":"float"
                        },
                        "pka": {
                            "type":"float"
                        },
                        "water_solubility": {
                            "type":"string"
                        },
                        "logs": {
                            "type":"float"
                        },
                        "logp": {
                            "type":"float"
                        }
                    }
                },
                "predicted_properties": {
                    "properties": {
                        "mddr_like_rule": {  
                            "type":"string"                            
                        },
                        "logs": {
                            "type":"float"                            
                        },
                        "logp": {
                            "type":"float"
                        },
                        "number_of_rings": {
                            "type":"integer"
                        },
                        "ghose_filter": {  
                            "type":"string"
                        },
                        "h_bond_donor_count": {
                            "type":"integer"
                        },
                        "molecular_weight": {
                            "type":"float"
                        },
                        "monoisotopic_weight": {
                            "type":"float"
                        },
                        "water_solubility": { 
                            "type":"string"
                        },
                        "rotatable_bond_count": {
                            "type":"integer"
                        },
                        "iupac_name": {
                            "type":"string"                                                      
                        },
                        "polarizability": {
                            "type":"float"
                        },
                        "smiles": { 
                            "type":"string",
                            "analyzer":"string_lowercase"
                            
                        },
                        "inchikey": { 
                            "type":"string" ,
                            "analyzer":"string_lowercase"
                        },
                        "bioavailability": {  
                            "type":"string"
                        },
                        "physiological_charge": {
                            "type":"float"
                        },
                        "pka_(strongest_basic)": {
                            "type":"float"
                        },
                        "inchi": { 
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "polar_surface_area_(psa)": {
                            "type":"float"
                        },
                        "rule_of_five": {  
                            "type":"string"
                        },
                        "refractivity": {
                            "type":"float"
                        },
                        "pka_(strongest_acidic)": {
                            "type":"float"
                        },
                        "traditional_iupac_name": {
                            "type":"string"
                        },
                        "h_bond_acceptor_count": {
                            "type":"integer"
                        },
                        "molecular_formula": {  
                            "type":"string",
                            "analyzer":"string_lowercase" 
                        }
                    }                    
                },
                "taxonomy": {
                    "properties": {
                        "kingdom": {
                            "type":"string"                            
                        },
                        "description": {
                            "type":"string"                            
                        },
                        "subclass": {
                            "type":"string"                            
                        },
                        "substituent": {  
                            "type":"string"                           
                        },
                        "alternative_parent": {  
                            "type":"string"                           
                        },
                        "superclass": {
                            "type":"string"                            
                        },
                        "direct_parent": {
                            "type":"string"                            
                        },
                        "class": {
                            "type":"string"                            
                        }
                    }
                }, 
                "packagers": {  
                    "type":"string"                    
                },
                "manufacturers": {  
                    "type":"string"                                        
                },              
                "categories": {  
                    "type":"string"                                       
                },                
                "products": {
                    "properties": {
                        "strength": {
                            "type":"string"                            
                        },
                        "name": {  
                            "type":"string"                             
                        },
                        "generic": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "route": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "otc": {
                            "type":"string",
                            "analyzer":"string_lowercase"
                        },
                        "dosage_form": {
                            "type":"string"                              
                        }                        
                    }
                }
            }
        }
    }
    return mapping


