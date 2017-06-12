import urllib.request
import json
import collections
from biothings.utils.dataload import dict_sweep, unlist, value_convert_to_number
from biothings.utils.dataload import boolean_convert

def load_data(path):
    molecules_list = []
    url = urllib.request.urlopen(path)
    status_code = url.getcode()
    if status_code == 200:
        data = urllib.request.urlopen(path).read()
        jsonData = json.loads(str(data,'utf-8'))
        total_cnt = jsonData["page_meta"]['total_count']
    for i in range(0,total_cnt,1000):
        url = path+"?limit=1000&offset="+str(i)
        data = urllib.request.urlopen(url).read()  #type instance
        jsonData = json.loads(str(data,'utf-8'))  #type dictionary, lenght 2
        molecules_list = jsonData['molecules']
        for i in range(0,len(molecules_list)):
            restr_dict = restructure_dict(molecules_list[i])
            yield restr_dict

def restructure_dict(dictionary):
    restr_dict = dict()
    _flag = 0
    for key in list(dictionary): # this is for 1
        if key == 'molecule_chembl_id':
            restr_dict['_id']=dictionary[key]
        if key == 'molecule_structures' and type(dictionary['molecule_structures'])==dict:
            restr_dict['chembl'] = dictionary
            _flag=1
            for x,y in iter(dictionary['molecule_structures'].items()):
                if x == 'standard_inchi_key':
                    restr_dict['chembl'].update(dictionary)
                    restr_dict['chembl'].update({'inchi_key':y})
                if x == 'canonical_smiles':
                    restr_dict['chembl']['smiles'] = y
                if x == 'standard_inchi':
                    restr_dict['chembl']['inchi'] = y

    if _flag == 0:
        restr_dict['chembl'] = dictionary
    del restr_dict['chembl']['molecule_structures']
    restr_dict = unlist(restr_dict)
    restr_dict = dict_sweep(restr_dict, vals=[None,".", "-", "", "NA", "None","none", " ", "Not Available", "unknown","null"])
    restr_dict = value_convert_to_number(restr_dict, skipped_keys=["chebi_par_id","first_approval"])
    restr_dict = boolean_convert(restr_dict, added_keys=["topical","oral","parenteral",
                              "dosed_ingredient","polymer_flag","therapeutic_flag","med_chem_friendly","ro3_pass"])
    return restr_dict

# FIXME: include in load_data ? or as a mapper ?
def get_id_for_merging(doc, src, db):
    try:
        _id = doc[src]['inchi_key']
    except:
        _id = doc['_id']
    return _id




