from .pubchem_parser import load_data as _load_data

__METADATA__ = {
    "src_name": 'PUBCHEM',
    "src_url": "https://pubchem.ncbi.nlm.nih.gov/",    
    "field": "pubchem"
}

PUBCHEM_INPUT_URL = "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/"

def load_data():
    pubchem_data = _load_data(PUBCHEM_INPUT_URL)
    return pubchem_data

def get_id_for_merging(doc, src, db):    
    try:
        _id = doc[src]['inchi_key']
    except:
        _id = doc['_id']
    return _id

def get_mapping():
    mapping = {
        "pubchem" : {
            "properties" : {
                "inchi_key" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "undefined_atom_stereoceter_count" : {
                    "type":"integer"
                    },
                "formal_charge" : {
                    "type":"integer"
                    },
                "isotope_atom_count" : {
                    "type":"integer"
                    },
                "defined_atom_stereoceter_count" : {
                    "type":"integer"
                    },
                "molecular_weight" : {
                    "type":"float"
                    },
                "monoisotopic_weight" : {
                    "type":"float"
                    },
                "tautomers_count" : {
                    "type":"integer"
                    },
                "rotatable_bond_count" : {
                    "type":"integer"
                    },
                "exact_mass" : {
                    "type":"float"
                    },
                "chiral_bond_count" : {
                    "type":"integer"
                    },
                "smiles" : {
                    "properties" : {
                        "isomeric" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            },
                        "canonical" : {
                            "type":"string",
                            "analyzer":"string_lowercase"
                            }
                        }
                    },
                "hydrogen_bond_acceptor_count" : {
                    "type":"integer"
                    },
                "hydrogen_bond_donor_count" : {
                    "type":"integer"
                    },
                "inchi" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "undefined_bond_stereocenter_count" : {
                    "type":"integer"
                    },
                "defined_bond_stereocenter_count" : {
                    "type":"integer"
                    },
                "xlogp" : {
                    "type":"float"
                    },
                "chiral_atom_count" : {
                    "type":"integer"
                    },
                "cid" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "topological_polar_surface_area" : {
                    "type":"float"
                    },
                "iupac" : {
                    "properties" : {
                        "traditional" : {
                            "type":"string"
                            }                        
                        }
                    },
                "complexity" : {
                    "type":"float"
                    },
                "heavy_atom_count" : {
                    "type":"integer"
                    },
                "molecular_formula" : {
                    "type":"string",
                    "analyzer":"string_lowercase"
                    },
                "covalently-bonded_unit_count" : {
                    "type":"integer"
                    }
                }
            }
        }
    return mapping
    
    
    
        
