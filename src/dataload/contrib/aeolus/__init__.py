import json

__METADATA__ = {
    "src_name": 'AEOLUS',
    "src_url": 'http://www.nature.com/articles/sdata201626',
    "field": "aeolus"
}
"""
{'case_count': 1,
'drug_concept_code': '476818',
'drug_concept_id': '19059006',
'drug_name': 'Magnesium glycinate',
'drug_vocabulary': 'RxNorm',
'inchikey': 'AACACXATQSKRQG-UHFFFAOYSA-L',
'outcome_concept_code': '10009033',
'outcome_concept_id': '37219804',
'outcome_name': 'Chronic obstructive pulmonary disease',
'outcome_vocabulary': 'MedDRA',
'prr': 4.03062,
'prr_95_percent_lower_confidence_limit': 0.5713199999999999,
'prr_95_percent_upper_confidence_limit': 28.435470000000002,
'pt': 'MAGNESIUM GLYCINATE',
'ror': 4.05017,
'ror_95_percent_lower_confidence_limit': 0.5669,
'ror_95_percent_upper_confidence_limit': 28.935840000000002,
'rxcui': '476818',
'snomed_outcome_concept_id': '255573',
'unii': 'IFN18A4Y6B'}"""

def get_mapping():
    mapping = {
        "aeolus": {
            "properties": {
                "case_count": {
                    "type": "long",
                },
                "drug_concept_code": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "drug_concept_id": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "drug_name": {
                    "type": "string",
                },
                "drug_vocabulary": {
                    "type": "string",
                },
                "inchikey": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "outcome_concept_code": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "outcome_concept_id": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "outcome_name": {
                    "type": "string",
                },
                "outcome_vocabulary": {
                    "type": "string",
                },
                "prr": {
                    "type": "float",
                },
                "prr_95_percent_lower_confidence_limit": {
                    "type": "float",
                },
                "prr_95_percent_upper_confidence_limit": {
                    "type": "float",
                },
                "pt": {
                    "type": "string",
                },
                "ror": {
                    "type": "float",
                },
                "ror_95_percent_lower_confidence_limit": {
                    "type": "float",
                },
                "ror_95_percent_upper_confidence_limit": {
                    "type": "float",
                },
                "rxcui": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "snomed_outcome_concept_id": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "unii": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
            }
        }
    }

    return mapping
