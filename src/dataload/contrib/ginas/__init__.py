import json

__METADATA__ = {
    "src_name": 'GINAS',
    "src_url": 'https://ginas.ncats.nih.gov',
    "field": "ginas"
}

ginas_input = "ginas_dump.json"


def load_data():
    with open(ginas_input) as f:
        return json.load(f)


def get_mapping():
    mapping = {
        "ginas": {
            "properties": {
                "cas_primary": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "unii": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "approvalID": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "definitionLevel": {
                    "type": "string",
                },
                "inchikey": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "mixture_unii": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "mixture_inchikey": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "names_list": {
                    "type": "string"
                },
                "preferred_name": {
                    "type": "string"
                },
                "properties": {
                    "type": "string",
                },
                "status": {
                    "type": "string"
                },
                "substanceClass": {
                    "type": "string"
                },
                "tags": {
                    "type": "string",
                },
                "uuid": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "xrefs": {
                    "properties": {
                        "CAS": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "DRUG BANK": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "MESH": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "NCI_THESAURUS": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "RXCUI": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "WIKIPEDIA": {
                            "type": "string",
                        }
                    }
                },
            }
        }
    }

    return mapping
