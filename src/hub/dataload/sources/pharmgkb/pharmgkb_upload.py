import os
import glob

import biothings.hub.dataload.storage as storage
from biothings.utils.mongo import get_src_db

from .pharmgkb_parser import load_data
from hub.dataload.uploader import BaseDrugUploader


SRC_META = {
        "url": 'https://www.pharmgkb.org/',
        "license_url": "https://www.pharmgkb.org/page/dataUsagePolicy",
        "license_url_short": "https://goo.gl/6ZW4iX",
        "license": "CC BY-SA 4.0"
        }


class PharmGkbUploader(BaseDrugUploader):

    name = "pharmgkb"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        self.logger.info("Load data from '%s'" % data_folder)
        input_file = os.path.join(data_folder,"drugs.tsv")
        assert os.path.exists(input_file), "Can't find input file '%s'" % input_file
        # get others source collection for inchi key conversion
        drugbank_col = get_src_db()["drugbank"]
        assert drugbank_col.count() > 0, "'drugbank' collection is empty (required for inchikey " + \
                "conversion). Please run 'drugbank' uploader first"
        pubchem_col = get_src_db()["pubchem"]
        assert pubchem_col.count() > 0, "'pubchem' collection is empty (required for inchikey " + \
                "conversion). Please run 'pubchem' uploader first"
        chembl_col = get_src_db()["chembl"]
        assert chembl_col.count() > 0, "'chembl' collection is empty (required for inchikey " + \
                "conversion). Please run 'chembl' uploader first"
        chebi_col = get_src_db()["chebi"]
        assert chebi_col.count() > 0, "'chebi' collection is empty (required for inchikey " + \
                "conversion). Please run 'chebi' uploader first"
        return load_data(input_file,drugbank_col,pubchem_col,chembl_col,chebi_col)

    @classmethod
    def get_mapping(klass):
        mapping = {
                "pharmgkb": {
                    "properties": {
                        "id": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "dosing_guideline": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "inchi": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "name": {
                            "type": "string"
                            },
                        "smiles": {
                            "analyzer": "string_lowercase",
                            "type": "string"
                            },
                        "generic_names": {
                            "type": "string"
                            },
                        "brand_mixtures": {
                            "type": "string"
                            },
                        "trade_names": {
                            "type": "string"
                            },
                        "type": {
                            "type": "string"
                            },
                        "xref": {
                            "properties": {
                                "web_resource": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "uniprotkb": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "pubchem": {
                                    "properties": {
                                        "sid": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            },
                                        "cid": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            }
                                        }
                                    },
                                "het": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "wikipedia": {
                                    "properties": {
                                        "url_stub": {
                                            "analyzer": "string_lowercase",
                                            "type": "string"
                                            }
                                        }
                                    },
                                "iuphar_ligand": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "meddra": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "atc": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "kegg_compound": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "umls": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    },
                                "clinicaltrials": {
                                        "properties": {
                                            "gov": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                }
                                            }
                                        },
                                "genbank": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "rxnorm": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "chebi": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "cas": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "ttd": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "kegg_drug": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "mesh": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "ndc": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "chemspider": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "hmdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "dailymed": {
                                        "properties": {
                                            "setid": {
                                                "analyzer": "string_lowercase",
                                                "type": "string"
                                                }
                                            }
                                        },
                                "ndfrt": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "bindingdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "drugbank": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "pdb": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        },
                                "dpd": {
                                        "analyzer": "string_lowercase",
                                        "type": "string"
                                        }
                                }
                        }
                    }
                }
            }
        return mapping

