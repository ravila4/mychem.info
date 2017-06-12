from biothings.utils.dataload import dict_sweep, unlist, value_convert_to_number


def load_data(sdf_file):
    f = open(sdf_file,'r').read()
    comp_list = f.split("$$$$") #split the compounds and list
    comp_list = [ele.split("\n> <") for ele in comp_list] #split from \n> <
    comp_list = list(map(lambda x:[ele.strip("\n") for ele in x],comp_list))
    comp_list = list(map(lambda x: [ele.split('>\n') for ele in x],comp_list))
    for item in comp_list:
        del item[0] #remove molecule structure - Marvin
    for element in comp_list:
        element = map(lambda x: [ele.split('\n') for ele in x],element)
    comp_list = list(map(lambda x: dict([ ele for ele in x]),comp_list)) #python 3 compatible
    del comp_list[-1]
    for compound in comp_list:
        restr_dict = restructure_dict(compound)
        yield restr_dict

def clean_up(_dict):
    _temp = dict()
    for key, value in iter(_dict.items()):
        key = key.lower().replace(' ','_').replace('-','_')
        value = value.split('\n')

        if key == "definition":
            value[0] = value[0].replace('<stereo>','').replace('<ital>','')
            value[0] = value[0].replace('</stereo>','').replace('</ital>','')
        _temp[key] = value
    return _temp

def restructure_dict(dictionary):
    restr_dict = dict()
    restr_dict['_id'] = dictionary['ChEBI ID']
    restr_dict['chebi']= dictionary
    restr_dict['chebi'] = clean_up(restr_dict['chebi'])
    restr_dict = dict_sweep(restr_dict,vals=[None,".", "-", "", "NA", "none", " ", "Not Available", "unknown","null","None"])
    restr_dict = value_convert_to_number(unlist(restr_dict),skipped_keys=["beilstein_registry_numbers","pubchem_database_links","pubmed_citation_links","sabio_rk_database_links","gmelin_registry_numbers","molbase_database_links"])
    return restr_dict

# FIXME: chedi_id -> inchi-key will require a mapper
def get_id_for_merging(doc, src, db):
    _flag = 0

    if 'inchikey' in doc[src]:
        _id = doc[src]['inchikey']
    else:
        if 'drugbank_database_links' in doc[src]:
            d = db.drugbank.find_one({'_id':doc[src]['drugbank_database_links']})
            if d != None:
                try:
                    _id = d['drugbank']['inchi_key']
                except:
                    _id = d['_id']
            else:
                _flag = 1
        else:
            _flag = 1

        if _flag:
            _flag = 0
            d = db.chembl.find_one({'chembl.chebi_par_id':doc['_id'][6:]},no_cursor_timeout=True)
            if d != None:
                try:
                    _id = d['chembl']['inchi_key']
                except:
                    _id = d['_id']
            else:
                d = db.drugbank.find_one({'drugbank.chebi':doc['_id'][6:]})
                if d != None:
                    try:
                        _id = d['chembl']['inchi_key']
                    except:
                        _id = d['_id']
                else:
                    _id = doc['_id']
    return _id

