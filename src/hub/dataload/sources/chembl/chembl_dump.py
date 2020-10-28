import glob
import json
import os
import os.path

import biothings
import config
from config import DATA_ARCHIVE_ROOT
biothings.config_for_app(config)

from biothings.hub.dataload.dumper import HTTPDumper
from biothings.utils.common import iter_n


class ChemblDumper(HTTPDumper):

    SRC_NAME = "chembl"
    SRC_ROOT_FOLDER = os.path.join(DATA_ARCHIVE_ROOT, SRC_NAME)
    # Keys are set to be the same as the top level key in each document's JSON data.
    SRC_DATA_URLS = {
            #"drug_indications": "https://www.ebi.ac.uk/chembl/api/data/drug_indication.json",
            #"activities": "https://www.ebi.ac.uk/chembl/api/data/activity.json",
            "molecules": "https://www.ebi.ac.uk/chembl/api/data/molecule.json",
            #"mechanisms": "https://www.ebi.ac.uk/chembl/api/data/mechanism.json",
            #"metabolisms": "https://www.ebi.ac.uk/chembl/api/data/metabolism.json",
            }
    SRC_VERSION_URL = "https://www.ebi.ac.uk/chembl/api/data/status.json"
    SCHEDULE = "0 12 * * *"
    CHUNK_MERGE_SIZE = 100  # number of part files merged together after download

    def remote_is_better(self, remotefile, localfile):
        remote_data = json.loads(self.client.get(self.__class__.SRC_VERSION_URL).text)
        assert "chembl_db_version" in remote_data
        assert remote_data["status"] == "UP"  # API is working correctly
        self.release = remote_data["chembl_db_version"]
        if localfile is None:
            # ok we have the release, we can't compare further so we need to download
            return True
        local_data = json.load(open(localfile))
        # comparing strings should work since it's formatted as "ChEMBL_xxx"
        if remote_data["chembl_db_version"] > local_data["chembl_db_version"]:
            return True
        else:
            return False

    def create_todump_list(self, force=False):
        version_filename = os.path.basename(self.__class__.SRC_VERSION_URL)
        try:
            current_localfile = os.path.join(self.current_data_folder, version_filename)
            if not os.path.exists(current_localfile):
                current_localfile = None
        except TypeError:
            # current data folder doesn't even exist
            current_localfile = None
        remote_better = self.remote_is_better(self.__class__.SRC_VERSION_URL, current_localfile)
        # Total number of records is determined by the molecules dataset
        data = json.loads(self.client.get(self.__class__.SRC_DATA_URLS["molecules"]).text)
        self.total_count = data["page_meta"]["total_count"]
        # Download data files
        for name, url in self.__class__.SRC_DATA_URLS.items():
            # get the total count from the first page
            data = json.loads(self.client.get(url).text)
            total_count = data["page_meta"]["total_count"]
            if force or current_localfile is None or remote_better:
                new_localfile = os.path.join(self.new_data_folder, version_filename)
                self.to_dump.append({"remote": self.__class__.SRC_VERSION_URL,
                                     "local": new_localfile})
                # now we need to scroll the API endpoint. Let's get the total number of records
                # and generate URLs for each call to parallelize the downloads
                for num, i in enumerate(range(0, total_count, 100)):
                    remote = url + "?limit=100&offset=" + str(i)
                    local = os.path.join(self.new_data_folder, "{}.part{}".format(name, str(num).zfill(4)))
                    self.to_dump.append({"remote": remote, "local": local})

    def post_dump(self, *args, **kwargs):
        self.logger.info("Merging JSON documents in '%s'" % self.new_data_folder)
        # we'll merge 100 files together, that's 100'000 documents. That way we don't have one huge
        # big files and we don't have thousands of them too. We'll also remove metadata (useless now)
        for name in self.__class__.SRC_DATA_URLS.keys():
            parts = glob.iglob(os.path.join(self.new_data_folder, "{}.part*".format(name)))
            for chunk, cnt in iter_n(parts, self.__class__.CHUNK_MERGE_SIZE, with_cnt=True):
                outfile = os.path.join(self.new_data_folder, "{}.{}.json".format(name, cnt))
                merged_data = {name: []}
                for f in chunk:
                    data = json.load(open(f))
                    merged_data[name].extend(data[name])
                json.dump(merged_data, open(outfile, "w"))
                self.logger.info("Merged %s files" % cnt)
        # now we can delete the parts
        #self.logger.info("Deleting part files")
        #parts = glob.iglob(os.path.join(self.new_data_folder, "*.part*"))
        #for f in parts:
        #    os.remove(f)
        self.logger.info("Post-dump merge done")
