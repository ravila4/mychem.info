import pandas as pd
import json


def main():

    unii = pd.read_csv('unii_records.tsv', sep='\t', low_memory=False, dtype=str)
    unii.rename(columns={'MF': 'molecular_formula',
                         'PT': 'preferred_term',
                         'RN': 'registry_number'}, inplace=True)
    unii.columns = unii.columns.str.lower()

    # half of them don't have inchikeys
    # set the primary key to inchikey and fill in missing ones with unii
    unii['_id'] = unii.inchikey
    unii['_id'].fillna(unii.unii, inplace=True)

    dupes = set(unii._id) - set(unii._id.drop_duplicates(False))
    records = [{k:v for k,v in record.items() if pd.notnull(v)} for record in unii.to_dict("records") if record['_id'] not in dupes]
    records = [{'_id': record['_id'], 'unii': record} for record in records]
    # take care of a couple cases with identical inchikeys
    for dupe in dupes:
        dr = unii.query("_id == @dupe").to_dict("records")
        dr = [{k:v for k,v in record.items() if pd.notnull(v)} for record in dr]
        records.append({'_id': dupe, 'unii': dr})
    for record in records:
        if isinstance(record['unii'], dict):
            del record['unii']['_id']
        else:
            for subr in record['unii']:
                del subr['_id']


    with open("unii_records.json", "w") as f:
        for record in records:
            print(json.dumps(record), file=f)


def do_import():
    from pymongo import MongoClient

    from local import MONGO_PASS
    db = MongoClient('mongodb://mydrug_user:{}@su08.scripps.edu:27017/drugdoc'.format(MONGO_PASS)).drugdoc
    coll = db['unii']

    with open("unii_records.json") as f:
        for line in f:
            doc = json.loads(line)
            coll.insert_one(doc)