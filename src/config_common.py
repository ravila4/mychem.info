# -*- coding: utf-8 -*-

import logging, os, datetime, time

LOGGER_NAME = "hub"
from biothings.utils.loggers import setup_default_log

from biothings.www.settings.default import *
from www.api.query_builder import ESQueryBuilder
from www.api.query import ESQuery
from www.api.transform import ESResultTransformer
from www.api.handlers import DrugHandler, QueryHandler, MetadataHandler, StatusHandler

# *****************************************************************************
# Elasticsearch variables
# *****************************************************************************
# elasticsearch server transport url
ES_HOST = 'localhost:9200'
# elasticsearch index name
ES_INDEX = 'mydrugs_current'
# elasticsearch document type
ES_DOC_TYPE = 'drug'
# make these smaller for c.biothings
ES_SIZE_CAP = 10
# scrolls are smaller
ES_SCROLL_SIZE = 10

API_VERSION = 'v1'

# *****************************************************************************
# App URL Patterns
# *****************************************************************************
APP_LIST = [
    (r"/status", StatusHandler),
    (r"/metadata/?", MetadataHandler),
    (r"/metadata/fields/?", MetadataHandler),
    (r"/{}/drug/(.+)/?".format(API_VERSION), DrugHandler),
    (r"/{}/drug/?$".format(API_VERSION), DrugHandler),
    (r"/{}/compound/(.+)/?".format(API_VERSION), DrugHandler),
    (r"/{}/compound/?$".format(API_VERSION), DrugHandler),
    (r"/{}/query/?".format(API_VERSION), QueryHandler),
    (r"/{}/metadata/?".format(API_VERSION), MetadataHandler),
    (r"/{}/metadata/fields/?".format(API_VERSION), MetadataHandler),
]

###############################################################################
#   app-specific query builder, query, and result transformer classes
###############################################################################

# *****************************************************************************
# Subclass of biothings.www.api.es.query_builder.ESQueryBuilder to build
# queries for this app
# *****************************************************************************
ES_QUERY_BUILDER = ESQueryBuilder
# *****************************************************************************
# Subclass of biothings.www.api.es.query.ESQuery to execute queries for this app
# *****************************************************************************
ES_QUERY = ESQuery
# *****************************************************************************
# Subclass of biothings.www.api.es.transform.ESResultTransformer to transform
# ES results for this app
# *****************************************************************************
ES_RESULT_TRANSFORMER = ESResultTransformer

GA_ACTION_QUERY_GET = 'query_get'
GA_ACTION_QUERY_POST = 'query_post'
GA_ACTION_ANNOTATION_GET = 'drug_get'
GA_ACTION_ANNOTATION_POST = 'drug_post'
GA_TRACKER_URL = 'c.biothings.io'

ANNOTATION_ID_REGEX_LIST = [(re.compile(r'db[0-9]+', re.I), 'drugbank.drugbank_id'),
                            (re.compile(r'chembl[0-9]+', re.I), 'chembl.molecule_chembl_id'),
                            (re.compile(r'chebi\:[0-9]+', re.I), 'chebi.chebi_id'),
                            (re.compile(r'cid[0-9]+', re.I), 'pubchem.cid'),
                            (re.compile(r'[A-Z0-9]{10}'), 'unii.unii')]
# make max sizes smaller
QUERY_GET_ES_KWARGS['size']['default'] = 10
ANNOTATION_POST_CONTROL_KWARGS['ids']['max'] = 10
QUERY_POST_CONTROL_KWARGS['q']['max'] = 10

STATUS_CHECK_ID = ''

HIPCHAT_MESSAGE_COLOR = 'gray'

JSONLD_CONTEXT_PATH = 'www/context/context.json'


# ################ #
# MYCHEM HUB VARS  #
# ################ #

DATA_SRC_MASTER_COLLECTION = 'src_master'   # for metadata of each src collections
DATA_SRC_DUMP_COLLECTION = 'src_dump'       # for src data download information
DATA_SRC_BUILD_COLLECTION = 'src_build'     # for src data build information

DATA_TARGET_MASTER_COLLECTION = 'db_master'

# where to store info about processes launched by the hub
RUN_DIR = './run'

# reporting diff results, number of IDs to consider (to avoid too much mem usage)
MAX_REPORTED_IDS = 1000
# for diff updates, number of IDs randomly picked as examples when rendering the report
MAX_RANDOMLY_PICKED = 10

# ES s3 repository to use snapshot/restore (must be pre-configured in ES)
SNAPSHOT_REPOSITORY = "drug_repository"

# cache file format ("": ascii/text uncompressed, or "gz|zip|xz"
CACHE_FORMAT = "xz"

# Max queued jobs in job manager
# this shouldn't be 0 to make sure a job is pending and ready to be processed
# at any time (avoiding job submission preparation) but also not a huge number
# as any pending job will consume some memory).
MAX_QUEUED_JOBS = os.cpu_count() * 4

# when creating a snapshot, how long should we wait before querying ES
# to check snapshot status/completion ? (in seconds)
# Since myvariant's indices are pretty big, a whole snaphost won't happne in few secs,
# let's just monitor the status every 5min
MONITOR_SNAPSHOT_DELAY = 5 * 60

# Hub environment (like, prod, dev, ...)
# Used to generate remote metadata file, like "latest.json", "versions.json"
# If non-empty, this constant will be used to generate those url, as a prefix 
# with "-" between. So, if "dev", we'll have "dev-latest.json", etc...
# "" means production
HUB_ENV = ""

# Pre-prod/test ES definitions
# (see bt.databuild.backend.create_backend() for the notation)
ES_TEST_HOST = 'localhost:9200'
# Prod ES definitions
ES_PROD_HOST = "tdb"

# Max numbers of processe workers in the hub (process queue)
# - None: will use as many workers as cpu cores
# - otherwise specify a number
HUB_MAX_WORKERS = 1

# How much memory hub is allowed to use:
# - "auto", let hub decides (will use 50%-60% of available RAM)
# - None: no limit
# - otherwise specify a number in GiB
HUB_MAX_MEM_USAGE = None

# fill with "token", "roomid" and "from" keys
# to broadcast message to a Hipchat room
HIPCHAT_CONFIG = {
#        "token" : "",
#        "roomid" : "",
#        "from" : "mychem_hub"
        }

SSH_HUB_PORT = 8022
