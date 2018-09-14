import os
import asyncio

import config
import biothings.hub.dataindex.indexer as indexer


class DrugIndexer(indexer.Indexer):

    def get_mapping(self, enable_timestamp=True):
        mapping = super(DrugIndexer,self).get_mapping(enable_timestamp=enable_timestamp)
        # TODO: enrich with myvariant specific stuff
        return mapping

    def get_index_creation_settings(self):
        return {"codec" : "best_compression"}

    @asyncio.coroutine
    def index(self, target_name, index_name, job_manager, steps=["index","post"],
              batch_size=10000, ids=None, mode="index"):
        # force smaller batch, as mychem has huge documents
        return super(DrugIndexer,self).index(
                target_name=target_name,
                index_name=index_name,
                job_manager=job_manager,
                steps=steps,
                batch_size=2500,
                ids=ids,
                mode=mode)
