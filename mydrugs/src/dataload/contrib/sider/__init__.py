from .sider_parser import load_data as _load_data

__METADATA__ = {
    "src_name": 'SIDER',
    "src_url": 'http://sideeffects.embl.de/',    
    "field": "sider"
}

SIDER_INPUT_FILE1 = '/home/jadesara/ENV/meddra_freq.tsv'
SIDER_INPUT_FILE2 = '/home/jadesara/ENV/meddra_all_se.tsv'
SIDER_INPUT_FILE3 = '/home/jadesara/ENV/meddra_all_indications.tsv'

def merge_files(SIDER_INPUT_FILE1, SIDER_INPUT_FILE2, SIDER_INPUT_FILE3):
    #merge first two files- side effect and side effect with frequency
    #add header to csv files
    df1 = pd.read_csv('meddra_freq.tsv', delimiter='\t')
    df2 = pd.read_csv('meddra_all_se.tsv', delimiter='\t')
    s1 = pd.merge(df1, df2, how='outer',on=['stitch_id(flat)','stitch_id(stereo)','umls_id(label)','meddra_type','umls_id(meddra)','se_name'])

    #merge above merged file with indication file
    df4 = pd.read_csv('meddra_all_indications.tsv',delimiter='\t')
    s2 = pd.merge(s1,df4,how='outer',on=['stitch_id(flat)','umls_id(label)','meddra_type','umls_id(meddra)'])
    s3 = s2.sort('stitch_id(flat)')
    s3.to_csv('merged_file.csv')
    return 

def load_data():
    sider_data = _load_data('merged_file.csv')
    return sider_data

def get_id_for_merging(doc, src, db):    
    cid = str(abs(100000000-int(doc['_id'][3:])))
    d = db.pubchem.find_one({'_id':cid})
    if d!= None:
        _id = d['pubchem']['inchi_key']
    else:
        _id = doc['_id']
    return _id

def get_mapping():
    mapping = {
        "sider" : {
            "properties" : {
                "meddra" : {
                    "properties" : {
                        "umls_id" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "type" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            }
                        }
                    },
                "side_effect" : {
                    "properties" : {
                        "frequency" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "name" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "placebo" : {
                            "type":"boolean"
                            }
                        }
                    },
                "stitch" : {
                    "properties" : {
                        "flat" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "stereo" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            }
                        }                                        
                    },
                "indication" : {
                    "properties" : {
                        "name" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "method_of_detection" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            }
                        }                                        
                    }
            }
        }
    }
    return mapping
