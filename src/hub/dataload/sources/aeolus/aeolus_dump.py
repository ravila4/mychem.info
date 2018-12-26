import os
import os.path
import sys
import time
import bs4

import biothings, config
biothings.config_for_app(config)

from config import DATA_ARCHIVE_ROOT
from biothings.hub.dataload.dumper import DummyDumper


class AeolusDumper(DummyDumper):
    """
    Aeolus dumper - a placeholder because the source is already in MongoDB
    """
    SRC_NAME = "aeolus_dt"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

