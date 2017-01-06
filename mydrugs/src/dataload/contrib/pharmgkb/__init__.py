from .pharmgkb_parser import load_data as _load_data

__METADATA__ = {
    "src_name": 'PharmGKb',
    "src_url": 'https://www.pharmgkb.org/',    
    "field": "pharmgkb"
}

PHARMGKB_INPUT_FILE = '/home/jadesara/ENV/pharmgkb/drugs.tsv'

def load_data():
    pharmgkb_data = _load_data(PHARMGKB_INPUT_FILE)
    return pharmgkb_data

def get_id_for_merging(doc, src, db):    
    _flag = 0
    if 'inchi' in doc[src]:
        _inchi = doc[src]['inchi']
        d = db.drugbank.find_one({'drugbank.inchi':_inchi})        
        if d != None:
            try:
                _id = d['drugbank']['inchi_key']
            except:
                _id = d['_id']            
        else:
            d = db.pubchem.find_one({'pubchem.inchi':_inchi})
            if d != None:
                try:
                    _id = d['pubchem']['inchi_key']
                except:
                    _id = d['_id']               
            else:
                d = db.chembl.find_one({'chembl.inchi':doc[src]['inchi']})
                if d != None:
                    try:
                        _id = d['chembl']['inchi_key']
                    except:
                        _id = d['_id']                    
                else:
                    _flag = 1    
    else:
        _flag = 1

    if _flag:
        _flag = 0
        if 'cross_references' in doc [src]:          
            for key in doc[src]['cross_references']:              
                if key == 'pubchem_compound':                 
                    cid = doc[src]['cross_references'].get(key) 
                    d = db.pubchem.find_one({'_id':cid})  
                    if d != None:                        
                        try:
                           _id = d['pubchem']['inchi_key']
                        except:
                            _id = d['_id']    
                                          
                elif key=='drugbank':                    
                    db_id = doc[src]['cross_references'].get(key)   
                    d = db.drugbank.find_one({'_id':db_id})
                    if d != None:
                        try:
                           _id = d['drugbank']['inchi_key']
                        except:
                            _id = d['_id']  
                elif key =='chebi':                    
                    chebi = doc[src]['cross_references'].get(key)
                    d = db.chebi.find_one({'_id':'CHEBI:'+chebi})
                    if d != None:
                        try:
                           _id = d['chebi']['inchikey']
                        except:
                            _d = db.merged_coll.find_one({'chebi.chebi_id':d['_id']})
                            _id = _d['_id']
                else:
                    _id = doc['_id']                           
                 
        else:
            _id = doc['_id']
    
    return _id

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
    
