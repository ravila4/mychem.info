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

    def test_get_chem(self):
        # test different endpoint aliases
        drug = self.json_ok(self.get_ok(self.api + '/drug/ZRALSGWEFCBTJO-UHFFFAOYSA-N'))
        chem = self.json_ok(self.get_ok(self.api + '/chem/ZRALSGWEFCBTJO-UHFFFAOYSA-N'))
        compound = self.json_ok(self.get_ok(self.api + '/compound/ZRALSGWEFCBTJO-UHFFFAOYSA-N'))

        assert drug == chem
        assert chem == compound

        # test different drug identifiers
        drugbank = self.json_ok(self.get_ok(self.api + '/drug/DB00551'))
        assert 'drugbank' in drugbank
        assert 'drugbank_id' in drugbank['drugbank']
        assert drugbank['drugbank']['drugbank_id'] == 'DB00551'

        chembl = self.json_ok(self.get_ok(self.api + '/drug/CHEMBL1308'))
        assert 'chembl' in chembl
        assert 'molecule_chembl_id' in chembl['chembl']
        assert chembl['chembl']['molecule_chembl_id'] == 'CHEMBL1308'

        unii = self.json_ok(self.get_ok(self.api + '/drug/7AXV542LZ4'))
        assert 'unii' in unii
        assert 'unii' in unii['unii']
        assert unii['unii']['unii'] == '7AXV542LZ4'

        chebi = self.json_ok(self.get_ok(self.api + '/drug/CHEBI:6431'))
        assert 'chebi' in chebi
        assert 'id' in chebi['chebi']
        assert chebi['chebi']['id'] == 'CHEBI:6431'

    def test_query_chem(self):
        # test query by drug name
        monobenzone = self.query_has_hits(q='drugbank.name:monobenzone')
        assert 'drugbank' in monobenzone['hits'][0]
        assert 'name' in monobenzone['hits'][0]['drugbank']
        assert monobenzone['hits'][0]['drugbank']['name'].lower() == 'monobenzone'

        # test query by drug target
        P34981 = self.query_has_hits(q='drugbank.targets.uniprot:P34981')
        assert 'drugbank' in P34981['hits'][0]
        assert 'targets' in P34981['hits'][0]['drugbank']
        assert 'uniprot' in P34981['hits'][0]['drugbank']['targets']
        assert P34981['hits'][0]['drugbank']['targets']['uniprot'] == 'P34981'

        #C0242339 = self.json_ok(self.get_ok(self.api + '/query?q=drugcentral.drug_use.indication.umls_cui:C0242339'))
        #assert 'drugcentral' in C0242339
        #assert 'drug_use' in C0242339['drugcentral']
        #assert 'indication' in C0242339['drugcentral']['drug_use']
        #assert 'umls_cui' in C0242339['drugcentral']['drug_use']['indication']
