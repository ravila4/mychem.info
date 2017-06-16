import os
import asyncio

import config
import biothings.dataindex.indexer as indexer


class DrugIndexer(indexer.Indexer):

    def get_mapping(self, enable_timestamp=True):
        mapping = super(DrugIndexer,self).get_mapping(enable_timestamp=enable_timestamp)
        # TODO: enrich with myvariant specific stuff
        return mapping

    def get_index_creation_settings(self):
        return {"codec" : "best_compression"}

