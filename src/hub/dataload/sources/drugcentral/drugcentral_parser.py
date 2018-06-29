import pandas as pd
from collections import defaultdict

def process_pharmacology_action(file_path_pharma_class):
    df_drugcentral_pharma_class = pd.read_csv(file_path_pharma_class, sep=",", names=['_id', 'struc_id', 'role', 'description', 'code', 'source'])
    df_drugcentral_pharma_class['source_name'] = df_drugcentral_pharma_class.apply(lambda row: row.source + '_' + row.role, axis=1)
    df_drugcentral_pharma_class = df_drugcentral_pharma_class.where((pd.notnull(df_drugcentral_pharma_class)), None)
    d = []
    for strucid, subdf in df_drugcentral_pharma_class.groupby('struc_id'):
        records = subdf.to_dict(orient="records")
        pharm_class_related = defaultdict(list)
        for _record in records:
            pharm_class_related[_record['source_name'].lower().replace("chebi_has role", "chebi")].append({'description': _record['description'], 'code': _record['code']})
        drecord = {"_id": strucid, "pharmacology_class": pharm_class_related}
        d.append(drecord)
    return {x['_id']: x['pharmacology_class'] for x in d}

def process_faers(file_path_faers):
    """
    # TODO: JSON field naming needs to be confirmed
    """
    df_drugcentral_faers = pd.read_csv(file_path_faers, sep=",", names=['_id', 'struc_id', 'meddra_term', 'meddra_code', 'level', 'llr', 'llr_threshold', 'drug_ae', 'drug_no_ae', 'no_drug_ae', 'no_drug_no_ar'])
    df_drugcentral_faers = df_drugcentral_faers.where((pd.notnull(df_drugcentral_faers)), None)    
    d = []
    for strucid, subdf in df_drugcentral_faers.groupby('struc_id'):
        records = subdf.to_dict(orient="records")
        faers_related = [{k: v for k, v in record.items() if k not in {'struc_id', '_id'}} for record in records]
        drecord = {"_id": strucid, "fda_adverse_event": faers_related}
        d.append(drecord)
    return {x['_id']: x['fda_adverse_event'] for x in d}

def process_act(file_path_act):
    df_drugcentral_act = pd.read_csv(file_path_act, sep=",", names=["act_id", "struct_id", "target_id", "target_name", "target_class", "accession", "gene", "swissprot", "act_value", "act_unit", "act_type", "act_comment", "act_source", "relation", "moa", "moa_source", "act_source_url", "moa_source_url", "action_type", "first_in_class", "tdl", "act_ref_id", "moa_ref_id", "organism"])
    df_drugcentral_act = df_drugcentral_act.where((pd.notnull(df_drugcentral_act)), None)
    d = []
    for strucid, subdf in df_drugcentral_act.groupby('struct_id'):
        records = subdf.to_dict(orient="records")
        pharm_class_related = []
        for _record in records:
            _summary = {'uniprot': []}
            if _record['accession']:
                accession = _record['accession'].split('|')
            else:
                accession = [None for i in range(10)]
            if _record['gene']:
                gene = _record['gene'].split('|')
            else:
                gene = [None for i in range(10)]
            if _record['swissprot']:
                swissprot = _record['swissprot'].split('|')
            else:
                swissprot = [None for i in range(10)]
            if not len(accession) == len(gene) == len(swissprot):
                continue
            for i in range(len(accession)):
                _summary['uniprot'].append({'uniprot_id': accession[i], 'gene_symbol': gene[i], 'swissprot_entry': swissprot[i]})
            for k, v in _record.items():
                if k not in ['uniprot', 'act_id', 'struct_id', 'target_id', 'accession', 'gene', 'swissprot', 'tdl', 'act_comment', "act_source_url", "moa_source_url", 'relation', "act_ref_id", "moa_ref_id", 'first_in_class']:
                    _summary[k] = v
            pharm_class_related.append(_summary)
        drecord = {"_id": strucid, "bioactivity": pharm_class_related}
        d.append(drecord)
    return {x['_id']: x['bioactivity'] for x in d}

def process_omop(file_path_omop):
    df_drugcentral_omop = pd.read_csv(file_path_omop, sep=",", names=['_id', 'struct_id', 'concept_id', 'relationship_name', 'concept_name', 'umls_cui', 'snomed_full_name', 'cui_semantic_type', 'snomed_conceptid'])
    df_drugcentral_omop = df_drugcentral_omop.where((pd.notnull(df_drugcentral_omop)), None)
    d = []
    for strucid, subdf in df_drugcentral_omop.groupby('struct_id'):
        records = subdf.to_dict(orient="records")
        omop_related = defaultdict(list)
        for _record in records:
            if _record['snomed_conceptid']:
                _record['snomed_conceptid'] = int(_record['snomed_conceptid'])
            omop_related[_record['relationship_name'].lower()].append({'umls_cui': _record['umls_cui'], 'concept_name': _record['concept_name'], 'snomed_full_name': _record['snomed_full_name'], 'cui_semantic_type': _record['cui_semantic_type'], 'snomed_concept_id': _record['snomed_conceptid']})
        drecord = {"_id": strucid, "drug_use": omop_related}
        d.append(drecord)
    return {x['_id']: x['drug_use'] for x in d}

def process_approval(file_path_approval):
    df_drugcentral_approval = pd.read_csv(file_path_approval, sep=",", names=['_id', 'struct_id', 'date', 'agency', 'company', 'orphan'])
    df_drugcentral_approval = df_drugcentral_approval.where((pd.notnull(df_drugcentral_approval)), None)
    d = []
    for strucid, subdf in df_drugcentral_approval.groupby('struct_id'):
        records = subdf.to_dict(orient="records")
        approval_related = [{k: v for k, v in record.items() if k not in {'struct_id', '_id'}} for record in records]
        drecord = {"_id": strucid, "approval": approval_related}
        d.append(drecord)
    return {x['_id']: x['approval'] for x in d}

def process_drug_dosage(file_path_drug_dosage):
    df_drugcentral_drug_dosage = pd.read_csv(file_path_drug_dosage, sep=",", names=['_id', 'atc_code', 'dosage', 'unit', 'route', 'comment', 'struct_id'])
    df_drugcentral_drug_dosage = df_drugcentral_drug_dosage.where((pd.notnull(df_drugcentral_drug_dosage)), None)
    d = []
    for strucid, subdf in df_drugcentral_drug_dosage.groupby('struct_id'):
        records = subdf.to_dict(orient="records")
        drug_dosage_related = [{k: v for k, v in record.items() if k not in {'struct_id', '_id', 'atc_code', 'comment'}} for record in records]
        drecord = {"_id": strucid, "drug_dosage": drug_dosage_related}
        d.append(drecord)
    return {x['_id']: x['drug_dosage'] for x in d}

