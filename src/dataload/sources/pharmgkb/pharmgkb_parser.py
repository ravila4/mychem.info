import csv
import sys
from biothings.utils.dataload import dict_sweep, unlist

csv.field_size_limit(sys.maxsize)

def load_data(tsv_file, drugbank_col=None, pubchem_col=None, chembl_col=None, chebi_col=None):
    _file = open(tsv_file)
    reader = csv.DictReader(_file,delimiter='\t')
    _dict = {}
    drug_list = []
    for row in reader:
        _id = row["PharmGKB Accession Id"]
        _d = restr_dict(row)
        _d = clean_up(_d)
        _d = unlist(dict_sweep(_d))
        _dict = {'_id':_id,'pharmgkb':_d}
        _dict["_id"] = find_inchi_key(_dict,drugbank_col,pubchem_col,chembl_col,chebi_col)
        yield _dict

def restr_dict(d):
    _d = {}
    _li2 = ["External Vocabulary","Trade Names","Generic Names","Brand Mixtures","Dosing Guideline","Cross-references"]
    _li1 = ["SMILES","Name","Type","InChI"]
    for key, val in iter(d.items()):
        if key in _li1:
            _d.update({key.lower():val})
        elif key in _li2:
            val = val.split(',"')
            val = list(map(lambda each:each.strip('"'), val))  #python 3 compatible
            k = key.lower().replace(" ","_").replace('-','_').replace(".","_")
            _d.update({k:val})
        elif key == "PharmGKB Accession Id":
            k = key.lower().replace(" ","_").replace(".","_")
            _d.update({k:val})
    return _d

def clean_up(d):
    _li = ['cross_references','external_vocabulary']
    for key, val in iter(d.items()):
        if key in _li:
            _d= {}
            for ele in val:
                idx = ele.find(':')
                k = ele[0:idx].lower().replace(' ','_').replace('-','_').replace(".","_")
                v = ele[idx+1:]
                _d.update({k:v})
            d.update({key:_d})
    return d

def find_inchi_key(doc, drugbank_col, pubchem_col, chembl_col, chebi_col):
    _flag = 0
    _id = doc["_id"]
    if not drugbank_col or not pubchem_col or not chembl_col:
        return _id
    if 'inchi' in doc["pharmgkb"]:
        _inchi = doc["pharmgkb"]['inchi']
        d = drugbank_col.find_one({'drugbank.inchi':_inchi})
        if d != None:
            try:
                _id = d['drugbank']['inchi_key']
            except KeyError:
                _id = d['_id']
        else:
            d = pubchem_col.find_one({'pubchem.inchi':_inchi})
            if d != None:
                try:
                    _id = d['pubchem']['inchi_key']
                except KeyError:
                    _id = d['_id']
            else:
                d = chembl_col.find_one({'chembl.inchi':doc["pharmgkb"]['inchi']})
                if d != None:
                    try:
                        _id = d['chembl']['inchi_key']
                    except KeyError:
                        _id = d['_id']
                else:
                    _flag = 1
    else:
        _flag = 1

    if _flag:
        _flag = 0
        if 'cross_references' in doc ["pharmgkb"]:
            for key in doc["pharmgkb"]['cross_references']:
                if key == 'pubchem_compound':
                    cid = doc["pharmgkb"]['cross_references'].get(key)
                    d = pubchem_col.find_one({'_id':cid})
                    if d != None:
                        try:
                           _id = d['pubchem']['inchi_key']
                        except KeyError:
                            _id = d['_id']

                elif key=='drugbank':
                    db_id = doc["pharmgkb"]['cross_references'].get(key)
                    d = drugbank_col.find_one({'_id':db_id})
                    if d != None:
                        try:
                           _id = d['drugbank']['inchi_key']
                        except KeyError:
                            _id = d['_id']
                elif key =='chebi':
                    chebi = doc["pharmgkb"]['cross_references'].get(key)
                    d = chebi_col.find_one({'_id':'CHEBI:'+chebi})
                    if d != None:
                        try:
                           _id = d['chebi']['inchikey']
                        except KeyError:
                            # ??? there's no merged collection at this point (you can't rely
                            # on something you're going to build...). Also, what's the point of
                            # searching chebi.chebi_id in a merged collection, why not just chebi col ???
                            #_d = db.merged_coll.find_one({'chebi.chebi_id':d['_id']})
                            _id = d["chebi"]["chebi_id"]
                else:
                    _id = doc['_id']

        else:
            _id = doc['_id']

    return _id

