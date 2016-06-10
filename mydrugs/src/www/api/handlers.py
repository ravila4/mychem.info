# -*- coding: utf-8 -*-
from biothings.www.api.handlers import MetaDataHandler, BiothingHandler, QueryHandler, StatusHandler, FieldsHandler
from biothings.settings import BiothingSettings
from www.api.es import ESQuery

bts = BiothingSettings()

class DrugsHandler(BiothingHandler):
    ''' This class is for the /drugs endpoint. '''

class QueryHandler(QueryHandler):
    ''' This class is for the /query endpoint. '''

class StatusHandler(StatusHandler):
    ''' This class is for the /status endpoint. '''

class FieldsHandler(FieldsHandler):
    ''' This class is for the /metadata/fields endpoint. '''

class MetaDataHandler(MetaDataHandler):
    ''' This class is for the /metadata endpoint. '''
    disable_caching = True

def return_applist():
    ret = [
        (r"/status", StatusHandler),
        (r"/metadata", MetaDataHandler),
        (r"/metadata/fields", FieldsHandler),
    ]
    if bts._api_version:
        ret += [
            (r"/" + bts._api_version + "/metadata", MetaDataHandler),
            (r"/" + bts._api_version + "/metadata/fields", FieldsHandler),
            (r"/" + "/".join([bts._api_version, bts._annotation_endpoint, "(.+)", "?"]), DrugsHandler),
            (r"/" + "/".join([bts._api_version, bts._annotation_endpoint, "?$"]), DrugsHandler),
            (r"/" + "/".join([bts._api_version, bts._query_endpoint, "?"]), QueryHandler),
        ]
    else:
        ret += [
            (r"/" + bts._annotation_endpoint + "/(.+)/?", DrugsHandler),
            (r"/" + bts._annotation_endpoint + "/?$", DrugsHandler),
            (r"/" + bts._query_endpoint + "/?", QueryHandler),
        ]
    return ret
