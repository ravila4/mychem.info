from __future__ import print_function
import csv
import sys

csv.field_size_limit(sys.maxsize)

def load_data(tsv_file):
    _file = open(tsv_file) 
    reader = csv.DictReader(_file,delimiter='\t')
    _dict = {}
    drug_list = []
    for row in reader:
        _id = row["PharmGKB Accession Id"]   
        _d = restr_dict(row)  
        _d = clean_up(_d)
        _d = unlist(dict_sweep(_d))        
        _dict.update({'_id':_id,'pharmgkb':_d})
        drug_list.append(_dict)
    return drug_list
        
    
def restr_dict(d):
    _d = {}
    _li2 = ["External Vocabulary","Trade Names","Generic Names","Brand Mixtures","Dosing Guideline","Cross-references"]
    _li1 = ["SMILES","Name","Type","InChI"]
    for key, val in d.items():  
        if key in _li1:
            _d.update({key.lower():val})
        elif key in _li2:            
            val = val.split(',"')
            val = map(lambda each:each.strip('"'), val)            
            k = key.lower().replace(" ","_").replace('-','_')
            _d.update({k:val})  
        elif key == "PharmGKB Accession Id":
            k = key.lower().replace(" ","_")
            _d.update({k:val})    
    return _d

def clean_up(d):
    _li = ['cross_references','external_vocabulary']
    for key, val in d.items():       
        if key in _li:
            _d= {}
            for ele in val:                
                idx = ele.find(':')
                k = ele[0:idx].lower().replace(' ','_').replace('-','_')
                v = ele[idx+1:]
                _d.update({k:v})            
            d.update({key:_d})
    return d
                     



      
