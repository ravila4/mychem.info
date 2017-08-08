import os
import glob

from .unii_parser import load_data
from dataload.uploader import BaseDrugUploader
import biothings.hub.dataload.storage as storage


SRC_META = {
        "url": 'https://fdasis.nlm.nih.gov/srs/',
        "license_url" : "?",
        }


class UniiUploader(BaseDrugUploader):

    name = "unii"
    storage_class = storage.IgnoreDuplicatedStorage
    __metadata__ = {"src_meta" : SRC_META}

    def load_data(self,data_folder):
        self.logger.info("Load data from '%s'" % data_folder)
        record_files = glob.glob(os.path.join(data_folder,"*Records.txt"))
        assert len(record_files) == 1, "Expecting one record.txt file, got %s" % repr(record_files)
        input_file = record_files.pop()
        assert os.path.exists(input_file), "Can't find input file '%s'" % input_file
        return load_data(input_file)

    @classmethod
    def get_mapping(klass):
        mapping = {
            "unii": {
                "properties": {
                    "unii": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "preferred_term": {
                        "type": "string",
                    },
                    "registry_number": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "ec": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "ncit": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "rxcui": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "itis": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "ncbi": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "plants": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "grin": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "inn_id": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "molecular_formula": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "inchikey": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "smiles": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "unii_type": {
                        "type": "string"
                    },
                }
            }
        }

        return mapping

