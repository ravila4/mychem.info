import os
import json
from collections import defaultdict
from biothings.utils.dataload import dict_sweep, unlist, value_convert_to_number
from biothings.utils.dataload import boolean_convert


def load_data(data_folder):
    # Data paths
    molecules_file = os.path.join(data_folder, "molecules.json")
    activities_file = os.path.join(data_folder, "activities.json")
    drug_indications_file = os.path.join(data_folder, "drug_indications.json")
    mechanisms_file = os.path.join(data_folder, "mechanisms.json")
    metabolisms_file = os.path.join(data_folder, "metabolisms.json")
    # Parse files
    molecules_list = json.load(open(molecules_file))['molecules']
    activities = json.load(open(activities_file))['activities']
    activities = restructure_activities(activities)
    drug_indications = json.load(open(drug_indications_file))['drug_indications']
    drug_indications = restructure_drug_indications(drug_indications)
    mechanisms = json.load(open(mechanisms_file))['mechanisms']
    mechanisms = restructure_mechanisms(mechanisms)
    metabolisms = json.load(open(metabolisms_file))['metabolisms']
    metabolisms = restructure_metabolisms(metabolisms)
    for i in range(0, len(molecules_list)):
        restr_dict = restructure_dict(molecules_list[i])
        try:
            _id = restr_dict["chembl"]['inchi_key']
            restr_dict["_id"] = _id
        except KeyError:
            pass

        # Add additional metadata
        chembl_id = restr_dict['chembl']["molecule_chembl_id"]
        # Activities
        try:
            restr_dict["activities"] = activities[chembl_id]
            print(json.dumps(restr_dict, indent=2))
        except KeyError:
            pass
        # Drug interactions
        try:
            restr_dict["drug_indications"] = drug_indications[chembl_id]
        except KeyError:
            pass
        # Mechanisms
        try:
            restr_dict["mechanisms"] = mechanisms[chembl_id]
        except KeyError:
            pass
        # Metabolisms
        try:
            restr_dict["metabolisms"] = metabolisms[chembl_id]
        except KeyError:
            pass
        yield restr_dict


def restructure_activities(activity_data):
    """ Group activities by molecule_chembl_id
    """
    restr_dict = {}
    for doc in activity_data:
        key = doc["molecule_chembl_id"]
        restr_dict.setdefault(key, []).append(doc)
    restr_dict = unlist(restr_dict)
    return restr_dict


def restructure_drug_indications(indication_data):
    """ Group drug indications by molecule_chembl_id
    """
    restr_dict = {}
    for doc in indication_data:
        key = doc["molecule_chembl_id"]
        restr_dict.setdefault(key, []).append(doc)
    restr_dict = unlist(restr_dict)
    return restr_dict


def restructure_mechanisms(mechanism_data):
    """ Group mechanism data by molecule_chembl_id
    """
    restr_dict = {}
    for doc in mechanism_data:
        key = doc["molecule_chembl_id"]
        restr_dict.setdefault(key, []).append(doc)
    restr_dict = unlist(restr_dict)
    return restr_dict


def restructure_metabolisms(metabolism_data):
    """ Group metabolism data by molecule_chembl_id
    """
    restr_dict = {}
    for doc in metabolism_data:
        key = doc["drug_chembl_id"]
        restr_dict.setdefault(key, []).append(doc)
    restr_dict = unlist(restr_dict)
    return restr_dict


def restructure_xref(xref_list):
    """
    Group the cross references field based on the source
    Also change the field name
    """
    xref_output = defaultdict(list)
    for _record in xref_list:
        # note that the 'xref' field names are from the chembl datasource, not the parser
        if 'xref_src' in _record and _record['xref_src'] == 'PubChem':
            assert _record['xref_name'].startswith('SID: ')
            xref_output['pubchem'].append({'sid': int(_record['xref_id'])})
        elif 'xref_src' in _record and _record['xref_src'] == 'Wikipedia':
            xref_output['wikipedia'].append({'url_stub': _record['xref_id']})
        elif 'xref_src' in _record and _record['xref_src'] == 'TG-GATEs':
            xref_output['tg-gates'].append({'name': _record['xref_name'], 'id': int(_record['xref_id'])})
        elif 'xref_src' in _record and _record['xref_src'] == 'DailyMed':
            xref_output['dailymed'].append({'name': _record['xref_name']})
        elif 'xref_src' in _record and _record['xref_src'] == 'DrugCentral':
            xref_output['drugcentral'].append({'name': _record['xref_name'], 'id': int(_record['xref_id'])})
    return xref_output


def restructure_dict(dictionary):
    restr_dict = dict()
    _flag = 0
    for key in list(dictionary):  # this is for 1
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
    if 'cross_references' in restr_dict['chembl'] and restr_dict['chembl']['cross_references']:
        restr_dict['chembl']['xrefs'] = restructure_xref(restr_dict['chembl']['cross_references'])

    del restr_dict['chembl']['molecule_structures']
    del restr_dict['chembl']['cross_references']
    restr_dict = unlist(restr_dict)
    # Add "CHEBI:" prefix, standardize the way representing CHEBI IDs
    if 'chebi_par_id' in restr_dict['chembl'] and restr_dict['chembl']['chebi_par_id']:
        restr_dict['chembl']['chebi_par_id'] = 'CHEBI:' + str(restr_dict['chembl']['chebi_par_id'])
    else:
        # clean, could be a None
        restr_dict['chembl'].pop("chebi_par_id",None)

    restr_dict = dict_sweep(restr_dict, vals=[None,".", "-", "", "NA", "None","none", " ", "Not Available", "unknown","null"])
    restr_dict = value_convert_to_number(restr_dict, skipped_keys=["chebi_par_id","first_approval"])
    restr_dict = boolean_convert(restr_dict, ["topical","oral","parenteral","dosed_ingredient","polymer_flag",
        "therapeutic_flag","med_chem_friendly","molecule_properties.ro3_pass"])
    return restr_dict


if __name__ == "__main__":
    data = load_data("/home/ravila/.data/biothings_studio/datasources/chembl/ChEMBL_27")
    for doc in data:
        pass
        #print(json.dumps(doc, indent=2))
