import httplib2
import sys
import os
from nose.tools import ok_, eq_

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from biothings.tests.test_helper import BiothingTestHelperMixin

class MyChemTest(BiothingTestHelperMixin):
    host = os.getenv("MC_HOST", "")
    host = host.rstrip('/')
    print(host)
    api = host + '/v1'
    if host:
        sys.stderr.write("Testing on host: {}...\n".format(api))
    else:
        sys.stderr.write("Testing on build-in server: {}...\n".format(api))
    h = httplib2.Http()


    def has_hits(self, q, morethan=0):
        d = self.json_ok(self.get_ok(self.api + '/query?q='+q))
        ok_(d.get('total', 0) > morethan and len(d.get('hits', [])) > 0)
        ok_('_id' in d['hits'][0])

    def test_non_fielded_query(self):
        # we can't really compare the results, we just need to ensure we have data
        self.has_hits('imatinib')
        self.has_hits('drugbank.name:imatinib')
