# -*- coding: utf-8 -*-
from biothings.web.api.es.query_builder import ESQueryBuilder

class ESQueryBuilder(ESQueryBuilder):
    # Implement app specific queries here
    def _build_single_query(self, term, scopes=None):
        scopes = scopes or self.default_scopes
        if len(scopes) == 1:
            _query = self.queries.match({scopes[0]:{"query": "{}".format(term), "operator": "and"}})
        else:
            _query = self.queries.multi_match({"query":"{}".format(term), "fields":scopes, "operator":"and"})
        _query['script_fields'] = {'_source': {'script': {'id': 'truncate-large-fields'}}}
        return _query

    def add_extra_filters(self, q):
        ''' Override me to add more filters '''
        q['script_fields'] = {'_source': {'script': {'id': 'truncate-large-fields'}}}
        return q

    def _annotation_GET_query(self, bid):
        # don't go to .get here, still make a match _id query
        _scopes = self._get_term_scope(bid)
        #if not _scopes:
        #    _scopes = ['_id']
        return self._return_query_kwargs({'body': self._build_single_query(bid, scopes=_scopes)})
