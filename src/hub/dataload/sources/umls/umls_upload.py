import os.path
from .parser import load_data
import biothings.hub.dataload.uploader as uploader


class UMLSUploader(uploader.BaseSourceUploader):

    name = "umls"

    def load_data(self, data_folder):
        umls_docs = load_data(data_folder)
        return umls_docs

    @classmethod
    def get_mapping(klass):
        mapping = {
            "umls": {
                "properties": {
                    "cui": {
                        "type": "keyword",
                        "normalizer" : "keyword_lowercase_normalizer",
                        'copy_to': ['all'],
                    },
                    "mesh": {
                        "type": "keyword",
                        "normalizer" : "keyword_lowercase_normalizer",
                        'copy_to': ['all'],
                    },
                    "name": {
                        "type": "keyword",
                        "normalizer" : "keyword_lowercase_normalizer"
                    }
                }
            }
        }
        return mapping
