import os
import glob
import zipfile

from .pubchem_parser import load_data
from dataload.uploader import BaseDrugUploader


# common to both hg19 and hg38
SRC_META = {
        "url": "https://pubchem.ncbi.nlm.nih.gov/",
        "license_url" : "?",
        }


class PubChemUploader(BaseDrugUploader):

    name = "pubchem"

    def load_data(self,data_folder):
        self.logger.info("Load data from '%s'" % data_folder)
        input_file = "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/"
        # FIXME: this should be downloaded locally
        return load_data(input_file)

    @classmethod
    def get_mapping(klass):
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

