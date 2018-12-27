from biothings.hub.datatransform import DataTransformMDB
from biothings.hub.datatransform import RegExEdge
from biothings.hub.datatransform.datatransform_api import MyChemInfoEdge
import networkx as nx


graph_mychem = nx.DiGraph()

###############################################################################
# PharmGKB Nodes and Edges
###############################################################################
graph_mychem.add_node('inchi')
graph_mychem.add_node('chebi')
graph_mychem.add_node('chembl')
graph_mychem.add_node('drugbank')
graph_mychem.add_node('drugname')
graph_mychem.add_node('pubchem')
graph_mychem.add_node('rxnorm')
graph_mychem.add_node('unii')
graph_mychem.add_node('inchikey')
graph_mychem.add_node('pharmgkb')

################################################################################
# MyChem.Info API based lookup
################################################################################

graph_mychem.add_edge('drugbank', 'pubchem',
                      object=MyChemInfoEdge('drugbank.drugbank_id', 'pubchem.cid'))

graph_mychem.add_edge('pharmgkb', 'drugbank',
                      object=MyChemInfoEdge('pharmgkb.id', 'pharmgkb.xrefs.drugbank'))


####################
# Inchi
####################

graph_mychem.add_edge('inchi', 'pubchem',
                      object=MyChemInfoEdge('pubchem.inchi', 'pubchem.cid', weight=1.0))

graph_mychem.add_edge('inchi', 'drugbank',
                      object=MyChemInfoEdge('drugbank.inchi', 'drugbank.drugbank_id', weight=1.1))

graph_mychem.add_edge('inchi', 'chembl',
                      object=MyChemInfoEdge('chembl.inchi', 'chembl.molecule_chembl_id', weight=1.2))

####################
# InchiKey
####################
inchi_fields = [
    'pubchem.inchi',
    'drugbank.inchi',
    'chembl.inchi'
]
inchikey_fields = [
    'pubchem.inchi_key',
    'drugbank.inchi_key',
    'chembl.inchi_key'
]

# inchi to inchikey (direct route)
graph_mychem.add_edge('inchi', 'inchikey',
                      object=MyChemInfoEdge(inchi_fields, inchikey_fields, weight=0.5))

# indirect route
graph_mychem.add_edge('pubchem', 'inchikey',
                      object=MyChemInfoEdge('pubchem.cid', inchikey_fields))

graph_mychem.add_edge('drugbank', 'inchikey',
                      object=MyChemInfoEdge('drugbank.drugbank_id', inchikey_fields))

graph_mychem.add_edge('chembl', 'inchikey',
                      object=MyChemInfoEdge('chembl.molecule_chembl_id', inchikey_fields))

# self-loops to check looked-up values exist in official collection
graph_mychem.add_edge('drugbank', 'drugbank',
                      object=MyChemInfoEdge('drugbank.drugbank_id', 'drugbank.drugbank_id'))

####################
# Sider
####################
graph_mychem.add_node('stitch')

graph_mychem.add_edge('stitch', 'pubchem',
                      object=RegExEdge('CID10*', ''))


class MyChemKeyLookup(DataTransformMDB):

    def __init__(self, input_types, *args, **kwargs):
        super(MyChemKeyLookup, self).__init__(graph_mychem,
                input_types,
                output_types=['inchikey', 'unii', 'rxnorm', 'drugbank',
                              'chebi', 'chembl', 'pubchem', 'drugname'],
                *args, **kwargs)
