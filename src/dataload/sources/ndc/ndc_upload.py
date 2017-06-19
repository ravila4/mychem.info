import os
import glob
import pymongo

from .ndc_packages_parser import load_data as load_packages
from .ndc_products_parser import load_data as load_products
from dataload.uploader import BaseDrugUploader
import biothings.dataload.storage as storage
from biothings.utils.common import unzipall


SRC_META = {
        "url" : "http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm",
        "license_url" : "?",
        }


class NDCUploader(BaseDrugUploader):

    name = "ndc"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        package_file = os.path.join(data_folder,"package.txt")
        product_file = os.path.join(data_folder,"product.txt")
        assert os.path.exists(package_file), "Package file doesn't exist..."
        assert os.path.exists(product_file), "Product file doesn't exist..."
        for doc in load_packages(package_file):
            yield doc
        for doc in load_products(product_file):
            yield doc

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

