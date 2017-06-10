import os
import os.path
import sys
import time

import biothings, config
biothings.config_for_app(config)

from config import DATA_ARCHIVE_ROOT
from biothings.dataload.dumper import ManualDumper


class DrugBankDumper(ManualDumper):

    SRC_NAME = "drugbank"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    def __init__(self, *args, **kwargs):
        super(DrugBankDumper,self).__init__(*args,**kwargs)
        self.logger.info("""Assuming manual download""")
