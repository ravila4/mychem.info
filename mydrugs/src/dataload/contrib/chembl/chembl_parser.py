from __future__ import print_function
import urllib2
import json
import collections
from utils.dataload import dict_sweep, unlist, value_convert, boolean_convert

def load_data(path):
    molecules_list = []      
    url = urllib2.urlopen(path)
    status_code = url.getcode()
    if status_code == 200:   
        data = urllib2.urlopen(path)
        json_data = json.load(data)
        total_cnt = json_data["page_meta"]['total_count']  #total number of compounds    
    for i in range(0,total_cnt,1000):
        url = path+"?limit=1000&offset="+str(i)    
        data = urllib2.urlopen(url)        
        json_data = json.load(data)  #type dictionary, lenght 2        
        molecules_list = json_data['molecules'] #1000 dictionaries
        for i in range(0,len(molecules_list)):
            restr_dict = restructure_dict(molecules_list[i])        
            yield restr_dict  

def restructure_dict(dictionary):     
    restr_dict = dict()
    _flag = 0
    for key in dictionary:          
        if key == 'molecule_chembl_id':
            restr_dict['_id']=dictionary[key]               
        if key == 'molecule_structures' and type(dictionary['molecule_structures'])==dict:
            restr_dict['chembl'] = dictionary            
            _flag=1
            for x,y in dictionary['molecule_structures'].iteritems():
                if x == 'standard_inchi_key':
                    restr_dict['chembl'] = dict(dictionary.items()+{'inchi_key':y}.items())                                        
                if x == 'canonical_smiles':
                    restr_dict['chembl']['smiles'] = y                    
                if x == 'standard_inchi':
                    restr_dict['chembl']['inchi'] = y            
    if _flag == 0:
        restr_dict['chembl'] = dictionary
    del restr_dict['chembl']['molecule_structures']          
    restr_dict = unlist(restr_dict)
    restr_dict = dict_sweep(restr_dict, vals=[None,".", "-", "", "NA", "None","none", " ", "Not Available", "unknown","null"])        
    restr_dict = value_convert(restr_dict, skipped_keys=["chebi_par_id","first_approval"])
    restr_dict = boolean_convert(restr_dict, added_keys=["mddr_like_rule","black_box_warning","ghose_filter","rule_of_five","topical","oral","parenteral",
                              "dosed_ingredient","polymer_flag","therapeutic_flag","med_chem_friendly","ro3_pass"])     
    return restr_dict






