import pandas as pd
import csv

from biothings.utils.dataload import dict_sweep, value_convert_to_number

def load_data(_file, pubchem_col=None):
    _dict = {}
    prev_id = ''
    f = open(_file,'r')
    next(f)
    reader = csv.reader(f)
    for row in reader:
        _id = row[1]
        if _id == prev_id:
            _d = restr_dict(_dict,row)
            _dict['sider'].append(_d)
        else:
            prev_id = _id
            if len(_dict)!=0:
                _dict["_id"] = find_inchi_key(_dict, pubchem_col)
                yield _dict
                _dict = {}
            _dict.update({'_id':row[1]})
            _dict.update({'sider': []})
            _d = restr_dict(_dict,row)
            _dict['sider'].append(_d)
    _dict["_id"] = find_inchi_key(_dict, pubchem_col)
    yield _dict

def restr_dict(_dict,row):
    _d = {}
    _d.update({'stitch':{'flat':row[1],'stereo':row[2]}})
    _d.update({'side_effect':{'name':row[10],'placebo':bool(row[4]),'frequency':row[5]}})
    _d.update({'meddra':{'type':row[8],'umls_id':row[9]}})
    _d.update({'indication':{'method_of_detection':row[11],'name':row[12]}})
    _d = dict_sweep(value_convert_to_number(_d))
    return _d

def find_inchi_key(doc, pubchem_col):
    _id = doc["_id"]
    if not pubchem_col:
        return _id
    assert _id.startswith('CID')
    assert len(_id) == 12
    pubchem_id = str(int(_id[4:]))
    d = pubchem_col.find_one({'pubchem.cid':pubchem_id})
    if d:
        _id = d['pubchem']['inchi_key']
    else:
        _id = 'CID' + pubchem_id
    return _id

