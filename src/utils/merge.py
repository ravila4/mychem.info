from pymongo import MongoClient
from tqdm import tqdm

from local import MONGO_PASS


def merge(src, target):
    """Merging docs from src collection into target collection."""

    db = MongoClient('mongodb://mydrug_user:{}@su08.scripps.edu:27017/drugdoc'.format(MONGO_PASS)).drugdoc
    src_coll = db[src]
    target_coll = db[target]
    total = src_coll.count()

    for doc in tqdm(src_coll, total=total):
        target_coll.update_one({"_id": doc['_id']}, {'$set': doc}, upsert=True)



collections = ['drugbank1127', 'ctd',  'sider', 'chebi', 'ginas', 'pharmgkb', 'chembl', 'drugbank', 'ndc', 'pubchem']

