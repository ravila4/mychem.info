from hub.dataload.uploader import BaseDrugUploader
from biothings.utils.mongo import get_src_conn

import biothings.hub.dataload.storage as storage
from hub.datatransform.keylookup import MyChemKeyLookup


class AeolusUploader(BaseDrugUploader):

    storage_class = storage.RootKeyMergerStorage
    name = "aeolus"
    __metadata__ = {
        "src_meta": {
            "url": "http://www.nature.com/articles/sdata201626",
            "license_url": "http://datadryad.org/resource/doi:10.5061/dryad.8q0s4",
            "license_url_short": "http://bit.ly/2DIxWwF",
            "license": "CC0 1.0"
        }
    }

    keylookup = MyChemKeyLookup(
            [('inchikey', 'aeolus.inchikey'),
             ('unii', 'aeolus.unii'),
             ('drugname', 'aeolus.drug_name')],
            copy_from_doc=True
            )

    def load_data(self, data_folder):
        # read data from the source collection
        src_col = self.db[self.src_col_name]
        def load_data():
            yield from src_col.find()

        # perform keylookup on source collection
        return self.keylookup(load_data, debug=True)()

    @classmethod
    def get_mapping(klass):
        mapping = {
            "aeolus": {
                "properties": {
                    "drug_id": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword",
                    },
                    "drug_name": {
                        "type": "text",
                        "copy_to": ["all"]
                    },
                    "inchikey": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword",
                    },
                    "no_of_outcomes": {
                        "type": "integer",
                    },
                    "pt": {
                        "type": "text",
                    },
                    "unii": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword",
                    },
                    "drug_vocab": {
                        "type": "text"
                    },
                    "drug_code": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword",
                    },
                    "rxcui": {
                        "normalizer": "keyword_lowercase_normalizer",
                        "type": "keyword",
                    },
                    "relationships": {
                        "properties": {
                            "relatedSubstance": {
                                "properties": {
                                    "approvalID": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                    },
                                    "refPname": {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                    }
                                }
                            },
                            "type": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                            }
                        }
                    },
                    "outcomes": {
                        "properties": {
                            "meddra_code": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                            },
                            "case_count": {
                                "type": "long"
                            },
                            "id": {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword"
                            },
                            "name": {
                                "type": "text"
                            },
                            "prr": {
                                "type": "float"
                            },
                            "prr_95_ci": {
                                "type": "float"
                            },
                            "ror": {
                                "type": "float"
                            },
                            "ror_95_ci": {
                                "type": "float"
                            }
                        }
                    }
                }
            }
        }

        return mapping
