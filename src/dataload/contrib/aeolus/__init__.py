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
                        "outcome_code": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "outcome_id": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "outcome_name": {
                            "type": "string",
                        },
                        "outcome_vocab": {
                            "type": "string",
                        },
                        "prr": {
                            "type": "float",
                        },
                        "prr_95_CI_lower": {
                            "type": "float",
                        },
                        "prr_95_CI_upper": {
                            "type": "float",
                        },
                        "ror": {
                            "type": "float",
                        },
                        "ror_95_CI_lower": {
                            "type": "float",
                        },
                        "ror_95_CI_upper": {
                            "type": "float",
                        },
                    },
                }
            }
        }
    }

    return mapping
