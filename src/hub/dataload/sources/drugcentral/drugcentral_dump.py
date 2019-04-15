"""
Aeolus Dumper - placeholder
"""
# pylint: disable=E0401, E0611, C0412, C0413
import os
import os.path
import biothings
import config
biothings.config_for_app(config)
from biothings.hub.dataload.dumper import DummyDumper
from config import DATA_ARCHIVE_ROOT


class AeolusDumper(DummyDumper):
    """
    Drugcentral dumper - a placeholder because the source is already in MongoDB
    """
    # pylint: disable=R0903
    SRC_NAME = "drugcentral_dt"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)
