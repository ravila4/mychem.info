"""
Import mysql database using instructions in readme file here:
http://datadryad.org/resource/doi:10.5061/dryad.8q0s4

Then run parser.sh

Then run this..

"""

import pandas as pd
from pymongo import MongoClient

from local import MONGO_PASS


def merge_with_unii(aeolus, unii):
    df = pd.merge(unii[['UNII', 'PT', 'RXCUI', 'INCHIKEY']], aeolus, how="right", left_on="RXCUI",
                  right_on="drug_concept_code")
    gb = df.groupby("INCHIKEY")

    for inchikey, subdf in gb:
        dr = subdf.to_dict("records")
        dr = [{k.lower(): v for k, v in record.items() if pd.notnull(v)} for record in dr]
        yield {'_id': inchikey, 'aeolus': dr}


def merge_with_ginas(aeolus, ginas):
    df = pd.merge(ginas[['CAS_primary', 'RXCUI', 'UNII', 'mixture_UNII', 'preferred_names', 'substanceClass', 'inchikey']],
                  aeolus, how="right", left_on="RXCUI",
                  right_on="drug_concept_code")

if __name__ == "__main__":

    aeolus = pd.read_csv('aeolus.tsv', sep='\t', low_memory=False,
                         dtype={'drug_concept_id': str, 'outcome_concept_id': str,
                                'drug_concept_code': str,
                                'outcome_concept_code': str,
                                'snomed_outcome_concept_id': str})

    unii = pd.read_csv('../unii/unii_records.tsv', sep='\t', low_memory=False, dtype=str)

    db = MongoClient('mongodb://mydrug_user:{}@su08.scripps.edu:27017/drugdoc'.format(MONGO_PASS)).drugdoc
    #db = MongoClient('mongodb://mydrug_user:{}@localhost:27027/drugdoc'.format(MONGO_PASS)).drugdoc
    coll = db['aeolus']

    for doc in merge_with_unii(aeolus, unii):
        coll.insert_one(doc)

"""
# print missing
df[df.INCHIKEY.isnull()][['drug_concept_code', 'drug_name', 'UNII']].drop_duplicates().to_csv("missing.csv")


"""