#!/usr/bin/env python

import asyncio, asyncssh, sys
import concurrent.futures
from functools import partial

import config, biothings
biothings.config_for_app(config)

import logging
logging.info("Hub DB backend: %s" % biothings.config.HUB_DB_BACKEND)
logging.info("Hub database: %s" % biothings.config.DATA_HUB_DB_DATABASE)

from biothings.utils.manager import JobManager
loop = asyncio.get_event_loop()
process_queue = concurrent.futures.ProcessPoolExecutor(max_workers=config.HUB_MAX_WORKERS)
thread_queue = concurrent.futures.ThreadPoolExecutor()
loop.set_default_executor(process_queue)
max_mem = type(config.HUB_MAX_MEM_USAGE) == int and config.HUB_MAX_MEM_USAGE * 1024**3 or config.HUB_MAX_MEM_USAGE
job_manager = JobManager(loop,
                      process_queue, thread_queue,
                      max_memory_usage=max_mem,
                      )

import dataload
import biothings.hub.dataload.uploader as uploader
import biothings.hub.dataload.dumper as dumper
import biothings.hub.databuild.builder as builder
import biothings.hub.databuild.differ as differ
import biothings.hub.databuild.syncer as syncer
import biothings.hub.dataindex.indexer as indexer
from databuild.builder import MyChemDataBuilder
from dataindex.indexer import DrugIndexer

# will check every 10 seconds for sources to upload
upload_manager = uploader.UploaderManager(poll_schedule = '* * * * * */10', job_manager=job_manager)
upload_manager.register_sources(dataload.__sources_dict__)
upload_manager.poll()

dmanager = dumper.DumperManager(job_manager=job_manager)
dmanager.register_sources(dataload.__sources_dict__)
dmanager.schedule_all()

build_manager = builder.BuilderManager(builder_class=MyChemDataBuilder,job_manager=job_manager)
build_manager.configure()

differ_manager = differ.DifferManager(job_manager=job_manager)
differ_manager.configure()
syncer_manager = syncer.SyncerManager(job_manager=job_manager)
syncer_manager.configure()

pindexer = partial(DrugIndexer,es_host=config.ES_HOST)
index_manager = indexer.IndexerManager(pindexer=pindexer,
        job_manager=job_manager)
index_manager.configure()


from biothings.utils.hub import schedule, top, pending, done

COMMANDS = {
        # dump commands
        "dm" : dmanager,
        "dump" : dmanager.dump_src,
        "dump_all" : dmanager.dump_all,
        # upload commands
        "um" : upload_manager,
        "upload" : upload_manager.upload_src,
        "upload_all": upload_manager.upload_all,
        # building/merging
        "bm" : build_manager,
        "merge" : partial(build_manager.merge,"drug"),
        "mongo_sync" : partial(syncer_manager.sync,"mongo"),
        "es_sync" : partial(syncer_manager.sync,"es"),
        "es_sync_test" : partial(syncer_manager.sync,"es",target_backend=config.ES_TEST),
        #"es_sync_prod" : partial(syncer_manager.sync,"es",target_backend=config.ES_PROD),
        "es_test": config.ES_TEST,
        #"es_prod": config.ES_PROD,
        "sm" : syncer_manager,
        # diff
        "dim" : differ_manager,
        "diff" : partial(differ_manager.diff,"jsondiff"),
        "report": differ_manager.diff_report,
        # indexing commands
        "im" : index_manager,
        "index" : index_manager.index,
        "snapshot" : index_manager.snapshot,
        # admin/advanced
        "loop" : loop,
        "pqueue" : process_queue,
        "tqueue" : thread_queue,
        "g": globals(),
        "sch" : partial(schedule,loop),
        "top" : partial(top,process_queue,thread_queue),
        "pending" : pending,
        "done" : done,
        }

passwords = {
        'guest': '', # guest account with no password
        }

from biothings.utils.hub import start_server

server = start_server(loop,"MyChem.info hub",passwords=passwords,port=config.SSH_HUB_PORT,commands=COMMANDS)

try:
    loop.run_until_complete(server)
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()

