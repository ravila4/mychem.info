from __future__ import print_function
import xmltodict
import json
import collections
import urllib2
from utils.dataload import dict_sweep, unlist, value_convert, boolean_convert  
    
def load_data(xml_file):
    drug_list = []        
    def handle(path,item):  #streaming mode of xmltodict 
        item = restructure_dict(item)        
        drug_list.append(item)
        return True 
    with open(xml_file) as f:
        xmltodict.parse(f.read(),item_depth=2,item_callback=handle)           
    f.close()
    for drug in drug_list:
        yield drug  

def restructure_dict(dictionary):
    restr_dict = dict()
    d1 = dict()       
    products_list = [] 
    categories_list = []    
    pred_properties_dict = {}

    for key,value in dictionary.iteritems():
        if key == 'name' and value:
            d1[key] = value
            
        elif key == 'drugbank-id' and value:
            id_list = []
            if isinstance(value,list):
                for ele in value:                  
                    if isinstance(ele,collections.OrderedDict):
                        for x,y in ele.iteritems():                            
                            if x == '#text':
                                key = key.replace('-','_')
                                id_list.append(y)
                                d1.update({'accession_number':id_list})                                
                                restr_dict['_id'] = y
                    if isinstance(ele,unicode):
                        key = key.replace('-','_')
                        id_list.append(ele)
                        d1.update({'accession_number':id_list})                        
            elif isinstance(value,dict) or isinstance(value,collections.OrderedDict):
                for x,y in value.iteritems():
                    if x == '#text':
                        key = key.replace('-','_')
                        id_list.append(y)
                        d1.update({key:id_list})                        
                        restr_dict['_id'] = y             
                        
        elif key == 'description':            
            d1.update({'pharmacology':{key:value}})         
            
        elif key == 'cas-number':
            d1['cas'] = value
            
        elif key == 'groups':
            for i,j in value.iteritems():
                d1[key] = j
                
        elif key == 'indication':                       
            d1['pharmacology'].update({key:value})

        elif key == 'pharmacodynamics':
            d1['pharmacology'].update({key:value})                    
            
        elif key == 'mechanism-of-action':            
            key = key.replace('-','_')           
            d1['pharmacology'].update({key:value})

        elif key == 'toxicity':            
            d1['pharmacology'].update({key:value})           
            
        elif key == 'metabolism':            
            d1['pharmacology'].update({key:value})            
            
        elif key == 'absorption':            
            d1['pharmacology'].update({key:value})            
            
        elif key == 'half-life':            
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})           
            
        elif key == 'protein-binding':             
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})           
            
        elif key == 'route-of-elimination':            
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})           
            
        elif key == 'volume-of-distribution':            
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})            
            
        elif key == 'clearance':                              
            d1['pharmacology'].update({key:value})

        elif key == 'classification' and value:
            for m,n in value.iteritems():
                m = m.lower()
                m = m.replace('-','_')
                d1.update({'taxonomy':value})                    
        
        elif key == 'salts'and value:
            salts_list = []
            for m,n in value.iteritems():
                if isinstance(n,list):
                    for ele in n:
                        for k in ele:
                            if k == 'name':
                                salts_list.append(ele[k])
                                d1.update({key:salts_list})                            
                elif isinstance(n,dict) or isinstance(n,collections.OrderedDict):
                    d1.update({key:n['name']})
            
        elif key == 'synonyms' and value:
            synonym_list = []            
            if isinstance(value,collections.OrderedDict):
                for k,l in value.iteritems():
                    for e in l:
                        for g in e:
                            if g == '#text':
                                synonym_list.append(e[g])                                
                                d1.update({key:synonym_list})

        elif key == 'products'and value:
            products_dict = {}  
                     
            for d,f in value.iteritems():
                if isinstance(f,dict) or isinstance(f,collections.OrderedDict):                    
                    for p in f:                
                        if p == 'name':
                            products_dict[p] = f[p]                            
                        if p == 'dosage-form':
                            products_dict['dosage_form'] = f[p]                           
                        if p == 'strength':
                            products_dict[p] = f[p]                            
                        if p == 'route':
                            products_dict[p] = f[p]                            
                        if p == 'over-the-counter':
                            products_dict['otc'] = f[p]                            
                        if p == 'generic':
                            products_dict[p] = f[p]
                    products_list.append(products_dict)
                    products_dict = {}                                                    
                if isinstance(f,list):
                    for p in f:
                        for i,j in p.iteritems():
                            if i == 'name':
                                products_dict[i] = j                                
                            if i == 'dosage-form':
                                products_dict['dosage_form'] = j                                
                            if i == 'strength':
                                products_dict[i] = j                                
                            if i == 'route':
                                products_dict[i] = j                                
                            if i == 'over-the-counter':
                                products_dict['otc'] = j                                
                            if i == 'generic':
                                products_dict[i] = j
                        products_list.append(products_dict)
                        products_dict = {}           

        elif key == 'packagers' and value:
            pack_list = []
            for pack in value:
                for pack1 in value[pack]:
                    for s in pack1:
                        if s == 'name' and pack1[s]:                            
                            pack_list.append(pack1[s])                          
                            d1.update({key:pack_list})                             

        elif key == 'manufacturers' and value:
            manuf_list = []
            for x,y in value.iteritems():
                if isinstance(y,dict) or isinstance(y,collections.OrderedDict):
                    for i in y:
                        if i == '#text':                            
                            manuf_list.append(y[i]) 
                            d1.update({key:manuf_list})     
                     
                if isinstance(y,list):
                    for i in y:
                        for m,n in i.iteritems():
                            if m == '#text':                                 
                                manuf_list.append(n)
                                d1.update({key:manuf_list})                                              
                             
        elif key == 'categories' and value:
            for x,y in value.iteritems():
                for i in y:
                    for m in i:
                        if m == 'category':
                            categories_list.append(i[m]) 

        elif key == "snp-effects" and value:            
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})           
                             
        elif key == "snp-adverse-drug-reactions" and value:                    
            key = key.replace('-','_')
            d1['pharmacology'].update({key:value})
                
        elif key == 'affected-organisms' and value:
            for x,y in value.iteritems():                
                key = key.replace('-','_')
                d1['pharmacology'].update({key:value["affected-organism"]})               
                                             
        elif key == 'ahfs-codes' and value:
            for x in value:
                key = key.replace('-','_')
                d1.update({key:value[x]})       

        elif key == 'food-interactions' and value:
            food_interaction_list = []
            for x,y in value.iteritems():
                if isinstance(y,list):
                    key = key.replace('-','_')
                    for i in y:
                        food_interaction_list.append(i)                        
                        d1.update({key:food_interaction_list})
                else:
                    d1.update({key:y})                      
        
        elif key == 'drug-interactions' and value:
            key = key.lower()
            key = key.replace('-','_')            
            for x,y in value.iteritems():
                d1.update({key:y})               

        elif key == 'sequences'and value:
            for x,y in value.iteritems():
                for i in y:
                    if i == '@format':
                        str1 = y[i]+'_sequences'
                        d1[str1] = y['#text']
        
        elif key == 'experimental-properties' and value:
            d1_exp_properties = {}
            for x,y in value.iteritems():
                key = key.replace('-','_')
                if isinstance(y,list):
                    for m in y:
                        for i in m:
                            k1 = m['kind']
                            k1 = k1.lower()
                            k1 = k1.replace(' ','_')
                            k1 = k1.replace('-','_')
                            d1_exp_properties[k1] = m['value']  
                            d1.update({key:d1_exp_properties})                                                 
                if isinstance(y,dict) or isinstance(y,collections.OrderedDict):
                    for i,j in y.iteritems():
                        k1 = y['kind']
                        k1 = k1.lower()
                        k1 = k1.replace(' ','_')
                        k1 = k1.replace('-','_')
                        d1_exp_properties[k1] = y['value'] 
                        d1.update({key:d1_exp_properties})                      
                        
        elif key == 'calculated-properties' and value:           
            for x,y in value.iteritems():
                if isinstance(y,list):
                    for m in y:
                        for i in m:  #m is the dictionary  
                            k = m['kind']
                            k = k.lower()
                            k = k.replace(' ','_')
                            k = k.replace('-','_')
                            pred_properties_dict[k] = m['value']                                                                                                                 
                            if m['kind'] == "IUPAC Name":
                                d1.update({'iupac':m['value']})                                
                            elif m['kind'] == "SMILES":                                
                                d1.update({'smiles':m['value']})
                            elif m['kind'] == "Molecular Formula":
                                d1.update({'formula':m['value']})                                
                            elif m['kind'] == "InChI":
                                d1.update({'inchi':m['value']})                                
                            elif m['kind'] == "InChIKey":                                
                                if m['value'][0:9] == 'InChIKey=':
                                    d1.update({'inchi_key':m['value'][9:]})                                    
                                else:
                                    d1.update({'inchi_key':m['value']})                                    
                            elif m['kind'] == "Molecular Weight":                                   
                                d1.update({'weight':{'average':m['value']}})                             
                            elif m['kind'] == "Monoisotopic Weight":                                  
                                d1['weight'].update({'monoisotopic':m['value']})                           
                                
                if isinstance(y,dict) or isinstance(y,collections.OrderedDict):
                    for i,j in y.iteritems():
                        k = y['kind']
                        k = k.lower()
                        k = k.replace(' ','_')
                        k = k.replace('-','_')
                        pred_properties_dict = y['value']                      
                        if y['kind'] == "IUPAC Name":
                            d1.update({'iupac':y['value']})                            
                        elif y['kind'] == "SMILES":
                            d1.update({'smiles':y['value']})                            
                        elif y['kind'] == "Molecular Formula":
                            d1.update({'formula':y['value']})                            
                        elif y['kind'] == "InChI":
                            d1.update({'inchi':y['value']})                            
                        elif y['kind'] == "InChIKey":
                            if y['value'][0:9] == 'InChIKey=':    
                                d1.update({'inchi_key':y['value'][9:]})                               
                            else:
                                d1.update({'inchi_key':y['value']})                                
                        elif y['kind'] == "Molecular Weight":                            
                            d1.update({'weight':{'average':y['value']}})                           
                        elif y['kind'] == "Monoisotopic Weight":
                            d1['weight'].update({'monoisotopic':y['value']})                                                                        
                            
        elif key == 'external-identifiers' and value:
            for x,y in value.iteritems():
                for m in y:
                    for i in m:
                        if i == 'resource':
                            if m[i] == "Drugs Product Database (DPD)":
                                d1['dpd'] = m['identifier']
                            if m[i] == "KEGG Drug":
                                d1['kegg'] = m['identifier']
                            if m[i] == "National Drug Code Directory":
                                d1['ndc_directory'] = m['identifier']
                            if m[i] == "PharmGKB":
                                d1['pharmgkb'] = m['identifier']
                            if m[i] == "UniProtKB":
                                d1['uniprotkb'] = m['identifier']
                            if m[i] == "Wikipedia":
                                d1['wikipedia'] = m['identifier']  

        elif key == 'patents'and value:           
            if isinstance(value,dict):                
                for x in value:
                    d1.update({key:value[x]})     
    
    d1['categories'] = categories_list
    d1['predicted_properties'] = pred_properties_dict  
    d1['products'] = products_list            
    restr_dict['drugbank'] = d1     
    restr_dict = value_convert(dict_sweep(unlist(restr_dict)), skipped_keys=["dpd"])        
    restr_dict = boolean_convert(restr_dict,added_keys=["mddr_like_rule","bioavailability","ghose_filter","rule_of_five"])        
    return restr_dict         


    

