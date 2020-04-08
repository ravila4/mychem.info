from collections import defaultdict
from biothings_client import get_client
import os
import copy
import time

CHEM_CLIENT = get_client('chem')
# list of UMLS semantic types belonging to chemical is based on
# https://www.nlm.nih.gov/research/umls/META3_current_semantic_types.html
UMLS_CHEMICAL_SEMANTIC_TYPES = [
    'Pharmacologic Substance',
    'Antibiotic',
    'Biomedical or Dental Material',
    'Biologically Active Substance',
    'Hormone',
    'Enzyme',
    'Vitamin',
    'Immunologic Factor',
    'Receptor',
    'Indicator, Reagent, or Diagnostic Acid',
    'Hazardous or Poisonous Substance',
    'Organic Chemical',
    'Nucleic Acid, Nucleoside, or Nucleotide',
    'Amino Acid, Peptide, or Protein',
    'Inorganic Chemical',
    'Element, Ion, or Isotope',
    'Body Substance',
    'Food'
]

def fetch_chemical_umls_cuis(mrsty_file):
    """Fetch all UMLS CUI IDs belonging to chemical semantic types
    
    :param: mrsty_file: the file path of MRSTY.RRF file
    """
    chem_set = set()
    with open(mrsty_file, "r") as fin:
        for line in fin:
            vals = line.rstrip("\n").split("|")
            if vals[3] in UMLS_CHEMICAL_SEMANTIC_TYPES:
                chem_set.add(vals[0])
    return chem_set

def query_mesh(mesh_ids: list) -> dict:
    """Use biothings_client.py to query mesh ids and get back '_id' in mychem.info
    
    :param: mesh_ids: list of mesh ids
    """
    res = CHEM_CLIENT.querymany(mesh_ids, scopes='drugcentral.xrefs.mesh_supplemental_record_ui,ginas.xrefs.MESH,pharmgkb.xrefs.mesh', fields='_id')
    new_res = defaultdict(list)
    for item in res:
        if not "notfound" in item:
            new_res[item['query']].append(item['_id'])
    return new_res

def query_drug_name(names: list) -> dict:
    """Use biothings_client.py to query drug names and get back '_id' in mychem.info
    
    :param: names: list of drug names
    """
    res = CHEM_CLIENT.querymany(names, scopes='ginas.preferred_name, pharmgkb.name, chebi.name, chembl.pref_name, drugbank.name', fields='_id')
    new_res = defaultdict(list)
    for item in res:
        if not item.get("notfound"):
            new_res[item['query']].append(new_res['_id'])
    return new_res

def parse_umls(rrf_file, chem_umls):
    """Parse the UMLS to determine the HGNC identifier of each gene CUI.
    The relevant files are in the archive <version>-1-meta.nlm (a zip file)
    within <version>/META/MRCONSO.RRF.*.gz
    Concatenate the unzipped versions of the MRCONSO files together to get the
    final MRCONSO.RRF file, which is a | delimited text file without a header.
    """

    res = defaultdict(list)
    mesh_ids = set()
    names = set()
    with open(rrf_file, "r") as fin:
        for line in fin:
            if "|MSH|" in line:
                vals = line.rstrip("\n").split("|")
                cui = vals[0]
                if cui in chem_umls:
                    if vals[1] == 'ENG' and vals[2] == 'P':
                        mesh_id = vals[vals.index('MSH') - 1]
                        res[cui].append({'cui': cui,
                                        'mesh': mesh_id,
                                        'name': vals[-5]})
                        mesh_ids.add(mesh_id)
                        if ',' not in vals[-5]:
                            names.add('"' + vals[-5] + '"')
    return (res, list(mesh_ids), list(names))

def load_data(data_folder):
    mrsat_file = os.path.join(data_folder, 'MRSTY.RRF')
    mrconso_file = os.path.join(data_folder, 'MRCONSO.RRF') 
    chem_umls = fetch_chemical_umls_cuis(mrsat_file) 
    cui_map, mesh_ids, names = parse_umls(mrconso_file, chem_umls)
    name_mapping = query_drug_name(names)
    time.sleep(200)
    mesh_id_mapping = query_mesh(mesh_ids)
    res = []
    for cui, info in cui_map.items():
        for rec in info:
            mesh = rec.get('mesh')
            if mesh_id_mapping.get(mesh):
                for _id in mesh_id_mapping.get(mesh):
                    res.append({
                        "_id": _id,
                        "umls": rec
                    })
                continue
            name = rec.get("name")
            if name_mapping.get(name):
                for _id in name_mapping.get(name):
                    res.append({
                        "_id": _id,
                        "umls": rec
                    })
                continue
            res.append({
                "_id": cui,
                "umls": rec
            })
    return res