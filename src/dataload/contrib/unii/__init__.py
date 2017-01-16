import json

__METADATA__ = {
    "src_name": 'UNII',
    "src_url": 'https://fdasis.nlm.nih.gov/srs/',
    "field": "unii"
}


def load_data(path = "unii_records.json"):
    with open(path) as f:
        for line in f:
            yield json.loads(line)


def get_mapping():
    mapping = {
        "unii": {
            "properties": {
                "unii": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "preferred_term": {
                    "type": "string",
                },
                "registry_number": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "ec": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "ncit": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "rxcui": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "itis": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "ncbi": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "plants": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "grin": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "inn_id": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "molecular_formula": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "inchikey": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "smiles": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "unii_type": {
                    "type": "string"
                },
            }
        }
    }

    return mapping
