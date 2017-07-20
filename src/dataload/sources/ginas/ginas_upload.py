import biothings.hub.dataload.uploader as uploader

class GinasUploader(uploader.DummySourceUploader):

    name = "ginas"
    __metadata__ = {
            "src_meta" : {
                "url" : "https://ginas.ncats.nih.gov",
                "license_url" : "?",
                }
            }

    @classmethod
    def get_mapping(klass):
        mapping = {
                "ginas": {
                    "properties": {
                        "cas_primary": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "relationships": {
                            "properties": {
                                "type": {
                                    "analyzer": "string_lowercase",
                                    "type": "string"
                                    }
                                }
                            },
                        "unii": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "approvalID": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "definitionLevel": {
                            "type": "string",
                            },
                        "inchikey": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "mixture_unii": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "mixture_inchikey": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "names_list": {
                            "type": "string"
                            },
                        "preferred_name": {
                            "type": "string"
                            },
                        "properties": {
                            "type": "string",
                            },
                        "status": {
                            "type": "string"
                            },
                        "substanceClass": {
                            "type": "string"
                            },
                        "tags": {
                            "type": "string",
                            },
                        "uuid": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                            },
                        "xrefs": {
                                "properties": {
                                    "CAS": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                        },
                                    "DRUG BANK": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                        },
                                    "MESH": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                        },
                                    "NCI_THESAURUS": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                        },
                                    "RXCUI": {
                                        "type": "string",
                                        "analyzer": "string_lowercase"
                                        },
                                    "WIKIPEDIA": {
                                        "type": "string",
                                        }
                                    }
                                },
                        }
                }
            }

        return mapping
