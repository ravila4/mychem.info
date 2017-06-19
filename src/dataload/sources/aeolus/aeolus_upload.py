import biothings.dataload.uploader as uploader

class AeolusUploader(uploader.DummySourceUploader):

    name = "aeolus"
    __metadata__ = {
            "src_meta" : {
                "url" : "http://www.nature.com/articles/sdata201626",
                "license_url" : "http://datadryad.org/resource/doi:10.5061/dryad.8q0s4",
                "license" : "CC0 1.0",
                }
            }

    @classmethod
    def get_mapping(klass):
        mapping = {
            "aeolus": {
                "properties": {
                    "drug_rxcui": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "drug_id": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "drug_name": {
                        "type": "string",
                    },
                    "inchikey": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "no_of_outcomes": {
                        "type": "integer",
                    },
                    "pt": {
                        "type": "string",
                    },
                    "unii": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "outcomes": {
                        "properties": {
                            "case_count": {
                                "type": "long",
                            },
                            "meddra_code": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "id": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "name": {
                                "type": "string",
                            },
                            "prr": {
                                "type": "float",
                            },
                            "prr_95_ci": {
                                "type": "float",
                            },
                            "ror": {
                                "type": "float",
                            },
                            "ror_95_ci": {
                                "type": "float",
                            },
                        },
                    },
                    "indications": {
                        "properties": {
                            "meddra_code": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "id": {
                                "type": "string",
                                "analyzer": "string_lowercase"
                            },
                            "name": {
                                "type": "string",
                            },
                            "count": {
                                "type": "integer",
                            },
                        }
                    }
                }
            }
        }

        return mapping
