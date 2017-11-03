#!/usr/bin/env python

import asyncio, asyncssh, sys
import concurrent.futures
from functools import partial
from collections import OrderedDict

import config, biothings
biothings.config_for_app(config)

import logging
# shut some mouths...
logging.getLogger("elasticsearch").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("boto").setLevel(logging.ERROR)

logging.info("Hub DB backend: %s" % biothings.config.HUB_DB_BACKEND)
logging.info("Hub database: %s" % biothings.config.DATA_HUB_DB_DATABASE)

from biothings.utils.manager import JobManager
loop = asyncio.get_event_loop()
process_queue = concurrent.futures.ProcessPoolExecutor(max_workers=config.HUB_MAX_WORKERS)
thread_queue = concurrent.futures.ThreadPoolExecutor()
loop.set_default_executor(process_queue)
max_mem = type(config.HUB_MAX_MEM_USAGE) == int and config.HUB_MAX_MEM_USAGE * 1024**3 or config.HUB_MAX_MEM_USAGE
job_manager = JobManager(loop,num_workers=config.HUB_MAX_WORKERS,
        max_memory_usage=config.HUB_MAX_MEM_USAGE)

import hub.dataload
import biothings.hub.dataload.uploader as uploader
import biothings.hub.dataload.dumper as dumper
import biothings.hub.databuild.builder as builder
import biothings.hub.databuild.differ as differ
import biothings.hub.databuild.syncer as syncer
import biothings.hub.dataindex.indexer as indexer
from hub.databuild.builder import MyChemDataBuilder
from hub.dataindex.indexer import DrugIndexer

# will check every 10 seconds for sources to upload
upload_manager = uploader.UploaderManager(poll_schedule = '* * * * * */10', job_manager=job_manager)
upload_manager.register_sources(hub.dataload.__sources_dict__)
upload_manager.poll('upload',lambda doc: upload_manager.upload_src(doc["_id"]))

dump_manager = dumper.DumperManager(job_manager=job_manager)
dump_manager.register_sources(hub.dataload.__sources_dict__)
dump_manager.schedule_all()

build_manager = builder.BuilderManager(builder_class=MyChemDataBuilder,job_manager=job_manager)
build_manager.configure()

differ_manager = differ.DifferManager(job_manager=job_manager,
        poll_schedule="* * * * * */10")
differ_manager.configure()
differ_manager.poll("diff",lambda doc: differ_manager.diff("jsondiff-selfcontained",old=None,new=doc["_id"]))
differ_manager.poll("release_note",lambda doc: differ_manager.release_note(old=None,new=doc["_id"]))

# test will access localhost ES, no need to throttle
syncer_manager_test = syncer.SyncerManager(job_manager=job_manager)
syncer_manager_test.configure()
# prod needs to be throttled
from biothings.hub.databuild.syncer import ThrottledESJsonDiffSyncer, ThrottledESJsonDiffSelfContainedSyncer
syncer_manager_prod = syncer.SyncerManager(job_manager=job_manager)
syncer_manager_prod.configure(klasses=[partial(ThrottledESJsonDiffSyncer,config.MAX_SYNC_WORKERS),
                                           partial(ThrottledESJsonDiffSelfContainedSyncer,config.MAX_SYNC_WORKERS)])

index_manager = indexer.IndexerManager(job_manager=job_manager)
pindexer = partial(DrugIndexer,es_host=config.ES_TEST_HOST,
        timeout=config.ES_TIMEOUT,max_retries=config.ES_MAX_RETRY,
        retry_on_timeout=config.ES_RETRY)
index_manager.configure([{"default":pindexer}])

from biothings.utils.hub import schedule, pending, done

COMMANDS = OrderedDict()
# dump commands
COMMANDS["dump"] = dump_manager.dump_src
COMMANDS["dump_all"] = dump_manager.dump_all
# upload commands
COMMANDS["upload"] = upload_manager.upload_src
COMMANDS["upload_all"] = upload_manager.upload_all
# building/merging
COMMANDS["merge"] = partial(build_manager.merge,"drug")
COMMANDS["merge_demo"] = partial(build_manager.merge,"demo_drug")
COMMANDS["es_sync_test"] = partial(syncer_manager_test.sync,"es",target_backend=config.ES_TEST)
COMMANDS["es_sync_prod"] = partial(syncer_manager_prod.sync,"es",target_backend=config.ES_PROD)
COMMANDS["es_test"] = config.ES_TEST
COMMANDS["es_prod"] = config.ES_PROD
# diff
COMMANDS["diff"] = partial(differ_manager.diff,"jsondiff-selfcontained")
COMMANDS["publish_diff"] = partial(differ_manager.publish_diff,config.S3_APP_FOLDER)
COMMANDS["publish_diff_demo"] = partial(differ_manager.publish_diff,config.S3_APP_FOLDER + "-demo",
                                        s3_bucket=config.S3_DIFF_BUCKET + "-demo")
COMMANDS["report"] = differ_manager.diff_report
COMMANDS["release_note"] = differ_manager.release_note
# indexing commands
COMMANDS["index"] = partial(index_manager.index,"default")
COMMANDS["snapshot"] = index_manager.snapshot
COMMANDS["publish_snapshot"] = partial(index_manager.publish_snapshot,config.S3_APP_FOLDER)
COMMANDS["publish_snapshot_demo"] = partial(index_manager.publish_snapshot,config.S3_APP_FOLDER + "-demo")

# admin/advanced
EXTRA_NS = {                                                                                                                                                                                                                            
        "dm" : dump_manager,
        "um" : upload_manager,
        "bm" : build_manager,
        "smp" : syncer_manager_prod,
        "smt" : syncer_manager_test,
        "dim" : differ_manager,
        "im" : index_manager,
        "jm" : job_manager,
        ## admin/advanced
        #"loop" : loop,
        "q" : job_manager.process_queue,
        "t" : job_manager.thread_queue,
        "g": globals(),
        "l":loop,
        "j":job_manager,
        "sch" : partial(schedule,loop),
        "top" : job_manager.top,
        "pending" : pending,
        "done" : done,
        }

passwords = {
        'guest': '', # guest account with no password
        }

from biothings.utils.hub import start_server

server = start_server(loop,"MyChem.info hub",passwords=passwords,
        port=config.SSH_HUB_PORT,commands=COMMANDS,extra_ns=EXTRA_NS)

try:
    loop.run_until_complete(server)
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()

