"""
Import mysql database using instructions in readme file here:
http://datadryad.org/resource/doi:10.5061/dryad.8q0s4

Then run parser.sh

Then run this..

"""

import pandas as pd
from pymongo import MongoClient

from local import MONGO_PASS


def parse(aeolus, unii):
    df = pd.merge(unii[['UNII', 'PT', 'RXCUI', 'INCHIKEY']], aeolus, how="right", left_on="RXCUI",
                  right_on="drug_concept_code")
    gb = df.groupby("INCHIKEY")

    for inchikey, subdf in gb:
        dr = subdf.to_dict("records")
        dr = [{k.lower(): v for k, v in record.items() if pd.notnull(v)} for record in dr]
        yield {'_id': inchikey, 'unii': dr}


if __name__ == "__main__":

    aeolus = pd.read_csv('aeolus.tsv', sep='\t', low_memory=False,
                         dtype={'drug_concept_id': str, 'outcome_concept_id': str,
                                'drug_concept_code': str,
                                'outcome_concept_code': str,
                                'snomed_outcome_concept_id': str})

    unii = pd.read_csv('../unii/unii_records.tsv', sep='\t', low_memory=False, dtype=str)

    db = MongoClient('mongodb://mydrug_user:{}@su08.scripps.edu:27017/drugdoc'.format(MONGO_PASS)).drugdoc
    coll = db['aeolus']

    for doc in parse(aeolus, unii):
        coll.insert_one(doc)
