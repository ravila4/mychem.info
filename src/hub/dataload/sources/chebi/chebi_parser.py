from biothings.utils.dataload import dict_sweep, unlist, value_convert_to_number


def load_data(sdf_file, drugbank_col=None, chembl_col=None):
    import biothings.utils.mongo as mongo
    f = open(sdf_file,'r').read()
    comp_list = f.split("$$$$") #split the compounds and list
    comp_list = [ele.split("\n> <") for ele in comp_list] #split from \n> <
    comp_list = list(map(lambda x:[ele.strip("\n") for ele in x],comp_list))
    comp_list = list(map(lambda x: [ele.split('>\n',1) for ele in x],comp_list))
    for item in comp_list:
        del item[0] #remove molecule structure - Marvin
    for element in comp_list:
        element = map(lambda x: [ele.split('\n') for ele in x],element)
    comp_list = list(map(lambda x: dict([ ele for ele in x]),comp_list)) #python 3 compatible
    del comp_list[-1]
    for compound in comp_list:
        restr_dict = restructure_dict(compound)
        restr_dict["_id"] = find_inchikey(restr_dict,drugbank_col,chembl_col)
        yield restr_dict

def clean_up(_dict):
    _temp = dict()
    _xref = dict()
    _citation = dict()
    for key, value in iter(_dict.items()):
        key = key.lower().replace(' ','_').replace('-','_')
        value = value.split('\n')
        if key == "definition":
            value[0] = value[0].replace('<stereo>','').replace('<ital>','')
            value[0] = value[0].replace('</stereo>','').replace('</ital>','')
        # restructure the pubchem_database_links field
        elif key == 'pubchem_database_links':
            new_pubchem_dict = {}
            if type(value) == list:
                for _value in value:
                    splitted_results = _value.split(':')
                    if len(splitted_results) == 2:
                        new_pubchem_dict[splitted_results[0].lower()] = splitted_results[1][1:]
            value = new_pubchem_dict
        elif key == 'iupac_names':
            key = 'iupac'
        elif key == 'chebi_id':
            key = 'id'
        elif key == 'chebi_name':
            key = 'name'

        if key == 'wikipedia_database_links':
            key = 'wikipedia'
            value = {'url_stub': value}
            _xref[key] = value
        elif key == 'beilstein_registry_numbers':
            key = 'beilstein'
            _xref[key] = value
        elif '_database_links' in key:
            key = key.replace('_database_links', '')
            _xref[key] = value
        elif '_registry_numbers' in key:
            key = key.replace('_registry_numbers', '')
            _xref[key] = value
        elif '_citation_links' in key:
            key = key.replace('_citation_links', '')
            if key == 'pubmed_central':
                key = 'pmc'
            _citation[key] = value
        else:
            _temp[key] = value

    if _xref.keys():
        _temp['xref'] = _xref
    if _citation.keys():
        _temp['citation'] = _citation
    return _temp

def restructure_dict(dictionary):
    restr_dict = dict()
    restr_dict['_id'] = dictionary['ChEBI ID']
    restr_dict['chebi']= dictionary
    restr_dict['chebi'] = clean_up(restr_dict['chebi'])
    restr_dict = dict_sweep(restr_dict,vals=[None,".", "-", "", "NA", "none", " ", "Not Available",
        "unknown","null","None","NaN"])
    restr_dict = value_convert_to_number(unlist(restr_dict),skipped_keys=["beilstein","pubmed","sabio_rk","gmelin_registry_numbers","molbase", "synonyms", "wikipedia"])
    return restr_dict

def find_inchikey(doc, drugbank_col, chembl_col):
    _flag = 0
    _id = doc["_id"] # default if we can't find anything

    if 'inchikey' in doc["chebi"]:
        _id = doc["chebi"]['inchikey']
    elif drugbank_col and chembl_col:
        if 'drugbank' in doc["chebi"]:
            d = drugbank_col.find_one({'_id':doc["chebi"]['drugbank']})
            if d != None:
                try:
                    _id = d['drugbank']['inchi_key']
                except KeyError:
                    # no inchi-key in drugbank
                    _id = d['_id']
            else:
                _flag = 1
        else:
            _flag = 1

        if _flag:
            _flag = 0
            d = chembl_col.find_one({'chembl.chebi_par_id':doc['_id'][6:]},no_cursor_timeout=True)
            if d != None:
                try:
                    _id = d['chembl']['inchi_key']
                except:
                    _id = d['_id']
            else:
                d = drugbank_col.find_one({'drugbank.chebi':doc['_id'][6:]})
                if d != None:
                    try:
                        _id = d['chembl']['inchi_key']
                    except:
                        _id = d['_id']
                else:
                    _id = doc['_id']
    return _id
