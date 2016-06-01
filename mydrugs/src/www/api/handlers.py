# -*- coding: utf-8 -*-
from biothings.www.api.handlers import MetaDataHandler, BiothingHandler, QueryHandler, StatusHandler, FieldsHandler
from biothings.settings import BiothingSettings
from www.api.es import ESQuery
import config

biothing_settings = BiothingSettings()

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
    if biothing_settings._api_version:
        ret += [
            (r"/" + biothing_settings._api_version + "/metadata", MetaDataHandler),
            (r"/" + biothing_settings._api_version + "/metadata/fields", FieldsHandler),
            (r"/" + biothing_settings._api_version + "/drug/(.+)/?", DrugsHandler),
            (r"/" + biothing_settings._api_version + "/drug/?$", DrugsHandler),
            (r"/" + biothing_settings._api_version + "/query/?", QueryHandler),
        ]
    else:
        ret += [
            (r"/drugs/(.+)/?", DrugsHandler),
            (r"/drugs/?$", DrugsHandler),
            (r"/query/?", QueryHandler),
        ]
    return ret
