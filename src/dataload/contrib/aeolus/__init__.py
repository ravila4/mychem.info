__METADATA__ = {
    "src_name": 'AEOLUS',
    "src_url": 'http://www.nature.com/articles/sdata201626',
    "field": "aeolus"
}


def get_mapping():
    mapping = {
        "aeolus": {
            "properties": {
                "drug_code": {
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
                "drug_vocab": {
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
                "rxcui": {
                    "type": "string",
                    "analyzer": "string_lowercase"
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
                        "code": {
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
                        "vocab": {
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
                }
            }
        }
    }

    return mapping
