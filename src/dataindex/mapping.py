import importlib

def get_mapping(sources=None):
    if sources is None:
        sources = sources or ['drugbank', 'chembl','pubchem','chebi','ndc','pharmgkb','sider']
        extra_mapping_li = []
    else:
        extra_mapping_li = []

    if isinstance(sources, str):
        sources = [sources]
    m = {
        "drug": {
            "include_in_all": False,
            "dynamic": False,
            "properties": {}
        }
    }

    for src in sources:
        src_m = importlib.import_module('dataload.contrib.' + src + '.__init__')
        _m = src_m.get_mapping()
        m['drug']['properties'].update(_m)

    for extra_mapping in extra_mapping_li:
        m['drug']['properties'].update(extra_mapping)
    return m
