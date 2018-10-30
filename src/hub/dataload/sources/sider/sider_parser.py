import pandas as pd
import csv

from biothings.utils.dataload import dict_sweep, value_convert_to_number
from .utils import key_value


def load_data(_file):
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
                yield _dict
                _dict = {}
            _dict.update({'_id':row[1]})
            _dict.update({'sider': []})
            _d = restr_dict(_dict,row)
            _dict['sider'].append(_d)
    yield _dict

def restr_dict(_dict,row):
    _d = {}
    _d.update({'stitch':{'flat':row[1],'stereo':row[2]}})
    _d.update({'side_effect':{'name':row[10],'placebo':bool(row[4]),'frequency':row[5]}})
    _d.update({'meddra':{'type':row[8],'umls_id':row[9]}})
    _d.update({'indication':{'method_of_detection':row[11],'name':row[12]}})
    _d = dict_sweep(value_convert_to_number(_d))
    return _d

def sort_key(doc):
    """helper function - sort by 'sider.side_effect.frequency' """
    # take the first element from the document
    default_value = -101

    s = next(key_value(doc, "side_effect.frequency"))
    n = str(next(key_value(doc, "side_effect.name")))

    # if no element then return default value, name
    if not s:
        return default_value, n
    # drop the %
    s = s.replace("%", "")
    if '-' in s:
        bounds = s.split("-")
        if len(bounds) != 2:
            return default_value, n
        try:
            lower = float(bounds[0])
            upper = float(bounds[1])
        except ValueError:
            return default_value, n
        avg = (upper + lower) / 2
        return -1 * avg, n
    else:
        # convert to a float (return default_value, name if unsuccessful)
        try:
            return -1 * float(s), n
        except ValueError:
            # default value sends an item to the top of the list
            return default_value, n
