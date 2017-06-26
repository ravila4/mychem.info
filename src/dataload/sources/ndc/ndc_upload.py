import os
import glob
import pymongo

from .ndc_parser import load_data
from dataload.uploader import BaseDrugUploader
import biothings.dataload.storage as storage
from biothings.utils.common import unzipall
from biothings.utils.mongo import get_src_db


SRC_META = {
        "url" : "http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm",
        "license_url" : "?",
        }


class NDCUploader(BaseDrugUploader):

    name = "ndc"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        drugbank_col = get_src_db()["drugbank"]
        assert drugbank_col.count() > 0, "'drugbank' collection is empty (required for inchikey " + \
                "conversion). Please run 'drugbank' uploader first"
        return load_data(data_folder,drugbank_col)


    @classmethod
    def get_mapping(klass):
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

