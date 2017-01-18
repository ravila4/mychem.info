"""
Import mysql database using instructions in readme file here:
http://datadryad.org/resource/doi:10.5061/dryad.8q0s4

Then run parser.sh

Then run this..

"""

import json

import pandas as pd
import sys
from pymongo import MongoClient

from local import MONGO_PASS


def merge_with_unii(aeolus, unii):
    df = pd.merge(unii[['unii', 'pt', 'rxcui', 'inchikey']], aeolus, how="right", left_on="rxcui", right_on="drug_code")
    gb = df.groupby("inchikey")

    for inchikey, subdf in gb:
        subdf_records = subdf[['ror', 'prr', 'prr_95_CI_lower', 'prr_95_CI_upper', 'ror_95_CI_lower', 'ror_95_CI_upper',
                               'vocab', 'case_count', 'code', 'id', 'name']]
        top_level_df = subdf[['unii', 'drug_code', 'drug_name', 'drug_vocab', 'inchikey', 'drug_id', 'rxcui', 'pt']].drop_duplicates()
        if len(top_level_df) != 1:
            raise ValueError(top_level_df)

        top_level = dict(top_level_df.iloc[0])
        top_level['no_of_outcomes'] = len(subdf_records)
        dr = subdf_records.to_dict("records")
        dr = [{k: v for k, v in record.items() if pd.notnull(v)} for record in dr]
        dr.sort(key=lambda x: x['case_count'], reverse=True)

        # group CI fields
        for doc in dr:
            doc['prr_95_ci'] = [doc.get('prr_95_CI_lower', None), doc.get('prr_95_CI_upper', None)]
            doc['ror_95_ci'] = [doc.get('ror_95_CI_lower', None), doc.get('ror_95_CI_upper', None)]
            for field in ['prr_95_CI_lower', 'prr_95_CI_upper', 'ror_95_CI_lower',  'ror_95_CI_upper']:
                if field in doc:
                    del doc[field]

        top_level['outcomes'] = dr
        yield {'_id': inchikey, 'aeolus': top_level}


def merge_with_ginas(aeolus, ginas):
    df = pd.merge(
        ginas[['CAS_primary', 'RXCUI', 'UNII', 'mixture_UNII', 'preferred_names', 'substanceClass', 'inchikey']],
        aeolus, how="right", left_on="RXCUI",
        right_on="drug_concept_code")


def main():
    aeolus = pd.read_csv('aeolus.tsv', sep='\t', low_memory=False,
                         dtype={'drug_concept_id': str, 'outcome_concept_id': str,
                                'drug_concept_code': str,
                                'outcome_concept_code': str,
                                'snomed_outcome_concept_id': str})

    aeolus.rename(columns={'prr_95_percent_lower_confidence_limit': 'prr_95_CI_lower',
                           'prr_95_percent_upper_confidence_limit': 'prr_95_CI_upper',
                           'ror_95_percent_lower_confidence_limit': 'ror_95_CI_lower',
                           'ror_95_percent_upper_confidence_limit': 'ror_95_CI_upper',
                           'outcome_concept_code': 'code',
                           'outcome_concept_id': 'id',
                           'outcome_name': 'name',
                           'outcome_vocabulary': 'vocab',
                           'drug_concept_code': 'drug_code',
                           'drug_concept_id': 'drug_id',
                           'drug_vocabulary': 'drug_vocab',
                           }, inplace=True)

    unii = pd.read_csv('../unii/unii_records.tsv', sep='\t', low_memory=False, dtype=str)
    unii.columns = unii.columns.str.lower()

    i = merge_with_unii(aeolus, unii)

    with open("aeolus.json", "w") as f:
        for doc in i:
            print(json.dumps(doc), file=f)


def insert_mongo():
    db = MongoClient('mongodb://mydrug_user:{}@su08.scripps.edu:27017/drugdoc'.format(MONGO_PASS)).drugdoc
    # db = MongoClient('mongodb://mydrug_user:{}@localhost:27027/drugdoc'.format(MONGO_PASS)).drugdoc
    coll = db['aeolus']
    coll.drop()

    docs = open("aeolus.json")

    for doc in docs:
        coll.insert_one(json.loads(doc))


if __name__ == "__main__":
    main()

    if len(sys.argv) == 2 and sys.argv[1] == "mongo":
        insert_mongo()

"""
# print missing
df[df.INCHIKEY.isnull()][['drug_concept_code', 'drug_name', 'UNII', 'RXCUI']].drop_duplicates().to_csv("missing.csv")


"""
