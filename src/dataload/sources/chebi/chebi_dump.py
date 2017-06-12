import os
import os.path
import sys
import time

import biothings, config
biothings.config_for_app(config)

from config import DATA_ARCHIVE_ROOT
from biothings.dataload.dumper import ManualDumper


class ChebiDumper(ManualDumper):

    SRC_NAME = "chebi"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    def __init__(self, *args, **kwargs):
        super(ChebiDumper,self).__init__(*args,**kwargs)
        self.logger.info("""Assuming manual download""")

