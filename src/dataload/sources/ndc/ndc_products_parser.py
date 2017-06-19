import csv

from biothings.utils.dataload import dict_sweep, unlist

def restr_dict(dictionary):
    _d = {}
    _d['ndc'] = {}
    for key in dictionary:
        if key is None:
            continue
        if key == 'PRODUCTID':
            _d.update({'_id':dictionary[key]})
            _d['ndc'].update({'product_id':dictionary[key]})
        else:
            _d['ndc'].update({key.lower():dictionary[key]})
    return _d

def convert_to_unicode(dictionary):
    for key, val in dictionary.items():
        if isinstance(val, str):
            dictionary[key] = str(val)
        elif isinstance(val, dict):
            convert_to_unicode(val)
    return dictionary

def load_data(_file):
    f = open(_file,'r',encoding="latin1")
    reader = csv.DictReader(f,dialect='excel-tab')
    for row in reader:
        _dict = restr_dict(row)
        _dict = convert_to_unicode(dict_sweep(_dict))
        #_dict["_id"] = _dict["ndc"]["productndc"]
        yield _dict




