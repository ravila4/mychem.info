
__METADATA__ = {
    "src_name": 'National Drug Code Directory',
    "src_url": 'http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm',    
    "field": "ndc"
}

def get_id_for_merging(doc, src, db):    
    _id = doc[src]['productndc']   
    return _id

def get_mapping():
    mapping = {
        "ndc" : {
            "properties" : {
                "product_id" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "productndc" : {
                    "type" : "string"
                    },
                "producttypename" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "proprietaryname" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "proprietarynamesuffix" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "nonproprietaryname" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "dosageformname" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "routename" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "startmarketingdate" : {
                    "type" : "string"
                    },
                "endmarketingdate" : {
                    "type" : "string"
                    },
                "marketingcategoryname" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "applicationnumber" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "labelername" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "substancename" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "active_numerator_strength" : {
                    "type" : "string"                    
                    },
                "active_ingred_unit" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "pharm_classes" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "deaschedule" : {
                    "type" : "string",
                    "analyzer":"string_lowercase"
                    },
                "package" : {
                    "properties" : {
                        "packagedescription" : {
                            "type" : "string",
                            "analyzer":"string_lowercase"
                            },
                        "ndcpackagecode" : {
                            "type" : "string"
                            }
                    }
                }
            }
        }
    }
    return mapping