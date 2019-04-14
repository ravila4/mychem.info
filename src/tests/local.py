'''
    MyChem Data-Aware Tests
'''

from nose.core import run

from biothings.tests import TornadoTestServerMixin
from tests.remote import MyChemTest
from web.settings import MyDrugWebSettings


class MyChemLocalTest(TornadoTestServerMixin, MyChemTest):
    '''
        Self contained test class, can be used for CI tools such as Travis
        Starts a Tornado server on its own and perform tests against this server.
    '''
    __test__ = True

    # Override - Read Settings from config.py
    settings = MyDrugWebSettings(config='config')


if __name__ == '__main__':
    print()
    print('MyChem Local Test')
    print('-'*70 + '\n')
    run(argv=['', '--logging-level=INFO', '-v'], defaultTest='__main__.MyChemLocalTest')
