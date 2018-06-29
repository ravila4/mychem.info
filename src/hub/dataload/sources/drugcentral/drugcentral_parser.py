from collections import defaultdict

def process_pharmacology_action(file_path_pharma_class):
    df_drugcentral_pharma_class = pd.read_csv(file_path_pharma_class, sep=",", names=['_id', 'struc_id', 'role', 'description', 'code', 'source'])
    df_drugcentral_pharma_class['source_name'] = df_drugcentral_pharma_class.apply(lambda row: row.source + '_' + row.role, axis=1)
    d = []
    for strucid, subdf in df_drugcentral_pharma_class.groupby('struc_id'):
        records = subdf.to_dict(orient="records")
        pharm_class_related = defaultdict(list)
        for _record in records:
            pharm_class_related[_record['source_name'].lower().replace("chebi_has role", "chebi")].append({'description': _record['description'], 'code': _record['code']})
        drecord = {"_id": strucid, "pharmacology_class": pharm_class_related}
        d.append(drecord)
    return {x['_id']: x['pharmacology_class'] for x in d}