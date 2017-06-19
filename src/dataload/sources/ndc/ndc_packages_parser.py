from biothings.utils.dataload import dict_sweep, unlist
import csv

def restr_dict(dictionary):
    _d = {}
    _d['ndc'] = {}
    _d['ndc']['package'] = {}

    for key in dictionary:
        if key is None:
            continue
        if key == 'PRODUCTID':
            _d.update({'_id':dictionary[key]})
            _d['ndc'].update({'product_id':dictionary[key]})
        elif key == 'NDCPACKAGECODE':
            _d['ndc']['package'].update({key.lower():dictionary[key]})
        elif key == 'PACKAGEDESCRIPTION':
            _d['ndc']['package'].update({key.lower():dictionary[key]})
        else:
            _d['ndc'].update({key.lower():dictionary[key]})
    return _d

def load_data(_file):
    f = open(_file,'r',encoding='latin1')
    reader = csv.DictReader(f,dialect='excel-tab')
    for row in reader:
        _dict = restr_dict(row)
        _dict = unlist(dict_sweep(_dict))
        #_dict["_id"] = _dict["ndc"]["productndc"]
        yield _dict

