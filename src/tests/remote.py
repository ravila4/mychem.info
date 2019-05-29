''' 
    MyChem Data-Aware Tests
'''

import os

from nose.core import runmodule
from nose.tools import eq_, ok_

from biothings.tests import BiothingsTestCase


class MyChemTest(BiothingsTestCase):
    '''
        Test against server specified in environment variable BT_HOST
        or MyChem.info production server if BT_HOST is not specified
        BT_HOST must start with its protocol like http://mychem.info
    '''
    __test__ = True

    host = os.getenv("BT_HOST", "http://mychem.info")
    host = host.rstrip('/')
    api = '/v1'

    inchikey_id = 'ZRALSGWEFCBTJO-UHFFFAOYSA-N'
    drugbank_id = 'DB00551'
    chembl_id = 'CHEMBL1308'
    chebi_id = 'CHEBI:6431'
    unii_id = '7AXV542LZ4'
    pubchem_id = '60823'
    prefixed_pubchem_id = 'CID:60823'

    def test_non_fielded_query(self):
        # we can't really compare the results, we just need to ensure we have data
        self.query(q='imatinib')
        self.query(q='drugbank.name:imatinib')

    def test_chem_object(self):
        # test all fields are loaded in drug objects
        res = self.request('drug/' + self.inchikey_id).json()
        attr_li = ['_id']
        for attr in attr_li:
            assert res.get(attr, None) is not None, 'Missing field "{}" in chem "{}"'.format(
                attr, self.inchikey_id)

        # test for specific databases

    def test_query(self):
        # test query by drug name
        monobenzone = self.query(q='drugbank.name:monobenzone')
        assert 'drugbank' in monobenzone['hits'][0]
        assert 'name' in monobenzone['hits'][0]['drugbank']
        assert monobenzone['hits'][0]['drugbank']['name'].lower(
        ) == 'monobenzone'

        # test query by drug target
        P34981 = self.query(q='drugbank.targets.uniprot:P34981')
        assert 'drugbank' in P34981['hits'][0]
        assert 'targets' in P34981['hits'][0]['drugbank']
        assert 'uniprot' in P34981['hits'][0]['drugbank']['targets'][0]
        assert P34981['hits'][0]['drugbank']['targets'][0]['uniprot'] == 'P34981'

        # C0242339 = self.request('query?q=drugcentral.drug_use.indication.umls_cui:C0242339').json()
        # assert 'drugcentral' in C0242339
        # assert 'drug_use' in C0242339['drugcentral']
        # assert 'indication' in C0242339['drugcentral']['drug_use']
        # assert 'umls_cui' in C0242339['drugcentral']['drug_use']['indication']
        # public query self.api at /query via get
        con = self.request('query?q=monobenzone&callback=mycallback').text
        ok_(con.startswith('mycallback('))

        # testing non-ascii character
        res = self.request('query?q=\xef\xbf\xbd\xef\xbf\xbd').json()
        eq_(res['hits'], [])

        self.request("query", expect_status=400)

    def test_query_post(self):
        # /query via post
        self.request("query", method='POST', data={'q': self.inchikey_id}).json()

        res = self.request("query", method='POST', data={'q': self.drugbank_id,
                                                         'scopes': 'drugbank.id'}).json()
        eq_(len(res), 1)
        eq_(res[0]['_id'], 'RRUDCFGSUDOHDG-UHFFFAOYSA-N')

        res = self.request("query", method='POST', data={'q': self.drugbank_id + ',DB00441',
                                                         'scopes': 'drugbank.id'}).json()
        eq_(len(res), 2)
        eq_(res[0]['_id'], 'RRUDCFGSUDOHDG-UHFFFAOYSA-N')
        eq_(res[1]['_id'], 'SDUQYLNIPVEERB-QPPQHZFASA-N')

        res = self.request("query", method='POST', data={'q': self.drugbank_id,
                                                         'scopes': 'drugbank.id',
                                                         'fields': 'drugbank.id'}).json()
        assert len(res) == 1
        assert 'query' in res[0]
        assert 'drugbank' in res[0] and 'id' in res[0]['drugbank']
        assert res[0]['query'] == res[0]['drugbank']['id']

        self.request('query', method='POST', data={}, expect_status=400)

    def test_query_size(self):
        res = self.request('query?q=drugbank.name:acid&fields=drugbank.name').json()
        eq_(len(res['hits']), 10)    # default
        res = self.request('query?q=drugbank.name:acid&fields=drugbank.name&size=1000').json()
        eq_(len(res['hits']), 1000)
        res = self.request('query?q=drugbank.name:acid&fields=drugbank.name&size=1001').json()
        eq_(len(res['hits']), 1000)
        res = self.request('query?q=drugbank.name:acid&fields=drugbank.name&size=2000').json()
        eq_(len(res['hits']), 1000)

    def test_chem(self):
        # test different endpoint aliases
        drug = self.request('drug/' + self.inchikey_id).json()
        chem = self.request('chem/' + self.inchikey_id).json()
        compound = self.request('compound/' + self.inchikey_id).json()

        assert drug == chem
        assert chem == compound

        # test different drug identifiers
        drugbank = self.request('drug/' + self.drugbank_id + '?fields=drugbank').json()
        assert 'drugbank' in drugbank
        assert 'id' in drugbank['drugbank']
        assert drugbank['drugbank']['id'] == self.drugbank_id

        chembl = self.request('drug/' + self.chembl_id + '?fields=chembl').json()
        assert 'chembl' in chembl
        assert 'molecule_chembl_id' in chembl['chembl']
        assert chembl['chembl']['molecule_chembl_id'] == self.chembl_id

        unii = self.request('drug/' + self.unii_id + '?fields=unii').json()
        assert 'unii' in unii
        assert 'unii' in unii['unii']
        assert unii['unii']['unii'] == self.unii_id

        chebi = self.request('drug/' + self.chebi_id + '?fields=chebi').json()
        assert 'chebi' in chebi
        assert 'id' in chebi['chebi']
        assert chebi['chebi']['id'] == self.chebi_id

        pubchem = self.request('drug/' + self.pubchem_id + '?fields=pubchem').json()
        assert 'pubchem' in pubchem
        assert 'cid' in pubchem['pubchem']
        assert pubchem['pubchem']['cid'] == int(self.pubchem_id)

        prefixed_pubchem = self.request(
            'drug/' + self.prefixed_pubchem_id + '?fields=pubchem').json()
        assert prefixed_pubchem == pubchem

        res = self.request('drug/' + self.inchikey_id).json()
        eq_(res['_id'], self.inchikey_id)

        # testing non-ascii character
        self.request('drug/' + self.inchikey_id +
                     '\xef\xbf\xbd\xef\xbf\xbdmouse', expect_status=404)
        ##*************************************************##
        # testing filtering parameters
        res = self.request('drug/{}?fields=pubchem'.format(self.inchikey_id)).json()
        eq_(set(res), set(['_id', '_version', 'pubchem']))
        self.request('drug', expect_status=404)
        self.request('drug/', expect_status=404)

    def test_drug_post(self):
        res = self.request("drug", method='POST', data={'ids': self.inchikey_id}).json()
        eq_(len(res), 1)
        eq_(res[0]['_id'], self.inchikey_id)

        res = self.request("drug", method='POST', data={
                           'ids': self.inchikey_id + ',RRUDCFGSUDOHDG-UHFFFAOYSA-N'}).json()
        eq_(len(res), 2)
        eq_(res[0]['_id'], self.inchikey_id)
        eq_(res[1]['_id'], 'RRUDCFGSUDOHDG-UHFFFAOYSA-N')

        res = self.request("drug", method='POST',
                           data={'ids': self.inchikey_id + ',RRUDCFGSUDOHDG-UHFFFAOYSA-N',
                                 'fields': 'pubchem'}).json()
        eq_(len(res), 2)
        for _g in res:
            eq_(set(_g), set(['_id', 'query', 'pubchem']))

        # Test a large drug post
        # # too slow
        # res = self.request("drug", method='POST', data={'ids': DRUG_POST_LIST}).json()
        # eq_(len(res), 999)

    def test_metadata(self):
        self.request('metadata')

    def test_query_facets(self):
        res = self.request(
            'query?q=drugbank.name:acid&size=0&facets=drugbank.weight.average').json()
        assert 'facets' in res and 'drugbank.weight.average' in res['facets']

    def test_unicode(self):
        s = '基因'

        self.request('drug/' + s, expect_status=404)

        res = self.request("drug", method='POST', data={'ids': s}).json()
        eq_(res[0]['notfound'], True)
        eq_(len(res), 1)
        res = self.request("drug", method='POST', data={'ids': self.inchikey_id + ',' + s}).json()
        eq_(res[1]['notfound'], True)
        eq_(len(res), 2)

        res = self.request('query?q=' + s).json()
        eq_(res['hits'], [])

        res = self.request("query", method='POST', data={"q": s, "scopes": 'drugbank.id'}).json()
        eq_(res[0]['notfound'], True)
        eq_(len(res), 1)

        res = self.request("query", method='POST', data={
                           "q": self.drugbank_id + '+' + s, 'scopes': 'drugbank.id'}).json()
        eq_(res[1]['notfound'], True)
        eq_(len(res), 2)

    def test_get_fields(self):
        res = self.request('metadata/fields').json()
        # Check to see if there are enough keys
        ok_(len(res) > 490)

        # Check some specific keys
        assert 'drugbank' in res
        assert 'pubchem' in res
        assert 'ginas' in res
        assert 'aeolus' in res
        assert 'drugcentral' in res

    def test_fetch_all(self):
        q = 'drugbank.name:acid&fields=drugbank.name&fetch_all=TRUE'
        res = self.request('query?q=' + q).json()
        assert '_scroll_id' in res
        assert 'hits' in res

        # get one set of results
        res2 = self.request('query?scroll_id=' + res['_scroll_id']).json()
        assert 'hits' in res2

    def test_msgpack(self):
        res = self.request('drug/' + self.inchikey_id).json()
        res2 = self.msgpack_ok(self.request(
            'drug/{}?msgpack=true'.format(self.inchikey_id)).content)
        ok_(res, res2)

        res = self.request('query?q=drugbank.id:{}&size=1'.format(self.drugbank_id)).json()
        res2 = self.msgpack_ok(self.request(
            'query?q=drugbank.id:{}&size=1&msgpack=true'.format(self.drugbank_id)).content)
        ok_(res, res2)

        res = self.request('metadata').json()
        res2 = self.msgpack_ok(self.request('metadata?msgpack=true').content)
        ok_(res, res2)

    def test_licenses(self):
        # cadd license
        res = self.request('drug/' + self.inchikey_id).json()
        if 'aeolus' in res:
            assert '_license' in res['aeolus']
            assert res['aeolus']['_license']
        if 'chebi' in res:
            assert '_license' in res['chebi']
            assert res['chebi']['_license']
        if 'chembl' in res:
            assert '_license' in res['chembl']
            assert res['chembl']['_license']
        if 'drugbank' in res:
            assert '_license' in res['drugbank']
            assert res['drugbank']['_license']
        if 'drugcentral' in res:
            assert '_license' in res['drugcentral']
            assert res['drugcentral']['_license']
        if 'ginas' in res:
            assert '_license' in res['ginas']
            assert res['ginas']['_license']
        if 'pubchem' in res:
            assert '_license' in res['pubchem']
            assert res['pubchem']['_license']

    def test_jsonld(self):
        pass

    def test_status_endpoint(self):
        self.request(self.host + '/status')
        # (testing failing status would require actually loading tornado app from there
        #  and deal with config params...)

    def test_all_fields(self):
        alls = [{"q": "DB01076", "fields": "drugbank.id"},
                {"q": "Siltuximab", "fields": "drugbank.name"},
                {"q": "IBUPROFEN", "fields": "ndc.substancename"},
                {"q": "fospropofol", "fields": "aeolus.drug_name"},
                {"q": "TOOSENDANIN", "fields": "chembl.pref_name"},
                {"q": "FLUPROPADINE", "fields": "ginas.preferred_name"},
                {"q": "DIMETHYNUR", "fields": "unii.preferred_term"},
                ]
        for d in alls:
            res = self.request('query?q=%(q)s&fields=%(fields)s&dotfield=true' % d).json()
            foundone = False
            for e in res["hits"]:
                if d["fields"] in e and e[d["fields"]] == d["q"]:
                    foundone = True
                    break
            assert foundone, "Expecting at least one result with q=%(q)s&fields=%(fields)s" % d


if __name__ == '__main__':
    print()
    print('MyChem Remote Test:', MyChemTest.host)
    print('-'*70 + '\n')
    runmodule(argv=['', '--logging-level=INFO', '-v'])
