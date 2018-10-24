import os
import glob
import pymongo

from .ndc_parser import load_data
from .exclusion_ids import exclusion_ids
from hub.dataload.uploader import BaseDrugUploader
import biothings.hub.dataload.storage as storage
from biothings.utils.common import unzipall
from biothings.utils.mongo import get_src_db
from mychem_utils import ExcludeFieldsById


SRC_META = {
        "url" : "http://www.fda.gov/Drugs/InformationOnDrugs/ucm142438.htm",
        "license_url" : "?",
        }


class NDCUploader(BaseDrugUploader):

    name = "ndc"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    @ExcludeFieldsById(exclusion_ids, ["ndc"])
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
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "productndc" : {
                            "type" : "text"
                            },
                        "producttypename" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "proprietaryname" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "proprietarynamesuffix" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "nonproprietaryname" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "dosageformname" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "routename" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "startmarketingdate" : {
                            "type" : "text"
                            },
                        "endmarketingdate" : {
                            "type" : "text"
                            },
                        "marketingcategoryname" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "applicationnumber" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "labelername" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "substancename" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "active_numerator_strength" : {
                                "type" : "text"                    
                                },
                        "active_ingred_unit" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "pharm_classes" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "deaschedule" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "package" : {
                                "properties" : {
                                    "packagedescription" : {
                                        "normalizer": "keyword_lowercase_normalizer",
                                        "type": "keyword",
                                        },
                                    "ndcpackagecode" : {
                                        "type" : "text"
                                        }
                                    }
                                }
                        }
            }
        }

        return mapping

