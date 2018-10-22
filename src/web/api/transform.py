# -*- coding: utf-8 -*-
from biothings.web.api.es.transform import ESResultTransformer

class ESResultTransformer(ESResultTransformer):
    # Add app specific result transformations
    def _get_doc(self, doc):
        _doc = doc.get('_source', doc.get('fields', {}))
        if "_source" in _doc:
            _doc = _doc['_source'][0]
        return _doc

    def _modify_doc(self, doc):
        for source, val in self.source_metadata.items():
            if source in doc:
                if isinstance(doc[source], dict):
                    try:
                        doc[source]['_license'] = val.get('license_url_short', val.get('license_url'))
                    except:
                        pass
                elif isinstance(doc[source], list):
                    for d in doc[source]:
                        try:
                            d['_license'] = val.get('license_url_short', val.get('license_url'))
                        except:
                            pass
