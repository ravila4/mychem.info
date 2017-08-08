from biothings.web.settings import BiothingESWebSettings

class MyDrugWebSettings(BiothingESWebSettings):
    # Add app-specific settings functions here
    def _source_metadata_object(self):
        _meta = {}
        try:
            _m = self.es_client.indices.get_mapping(index=self.ES_INDEX, doc_type=self.ES_DOC_TYPE)
            _meta = _m[list(_m.keys())[0]]['mappings'][self.ES_DOC_TYPE]['_meta']['src']
        except:
            pass
        return _meta
