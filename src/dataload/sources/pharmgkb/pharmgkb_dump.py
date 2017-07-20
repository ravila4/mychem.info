import os, sys, re, time
import bs4
import dateutil.parser as dtparser
from datetime import datetime
import requests

from config import DATA_ARCHIVE_ROOT
from biothings.hub.dataload.dumper import HTTPDumper, DumperException
from biothings.utils.common import unzipall


class PharmGkbDumper(HTTPDumper):

    SRC_NAME = "pharmgkb"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)

    DATA_URL = "https://api.pharmgkb.org/v1/download/file/data/drugs.zip"
    SCHEDULE = "0 12 * * *"

    def get_latest_release(self):
        req = requests.Request('HEAD',self.__class__.DATA_URL)
        res = self.client.send(req.prepare())
        try:
            lastmodified = res.headers["last-modified"]
            latest = datetime.strptime(lastmodified, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y%M%d")
            return latest
        except Exception as e:
            raise DumperException("Can't find or parse latest release date from URL '%s': %s" % (self.__class__.DATA_URL,e))

    def create_todump_list(self,force=False,**kwargs):
        self.release = self.get_latest_release()
        if force or not self.src_doc or (self.src_doc and self.src_doc.get("release") < self.release):
            # if new release, that link points to that latest release
            local = os.path.join(self.new_data_folder,os.path.basename(self.DATA_URL))
            self.to_dump.append({"remote":self.DATA_URL, "local":local})
        else:
            self.logger.debug("Nothing to dump",extra={"notify":True})

    def post_dump(self):
        unzipall(self.new_data_folder)




