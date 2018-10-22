{
    "script": {
        "lang": "painless",
        "source": "
            /*
                Script to truncate fields.

                Format of 'params' variable passed into script:

                params
                --------------
                doc --> org.elasticsearch.search.lookup.LeafDocLookup
                _source --> org.elasticsearch.search.lookup.SourceLookup
                _doc --> org.elasticsearch.search.lookup.LeafDocLookup
                _fields --> org.elasticsearch.search.lookup.LeafFieldsLookup
                truncate_rules --> painless_class: HashMap
                
                RULES
                ------
                chebi.uniprot_database_links--> remove if > 1000
                chebi.intenz_database_links --> remove if > 2000
                chebi.rhea_database_links -- > remove if > 1000
                chebi.sabio_rk_database_links --> remove if > 1000
                chebi.patent_database_links --> remove if > 1000
                chebi.reactome_database_links --> remove if > 1000
                aeolus.outcomes --> cap to 5000   (temp, need to address this later)
                drugbank.products --> cap to 5000   (temp, need to address this later)
                drugbank.mixtures --> cap to 5000    (temp, need to address this later)
            */
            Map truncated = new HashMap();
            Map ret = new HashMap();
            /* chebi docs */
            if (params._source.containsKey('chebi') && (params._source.chebi.containsKey('xref'))) {
                if (params._source.chebi.xref.containsKey('uniprot')) {
                    def chebiUniprot = params._source.chebi.xref.uniprot;
                    if ((chebiUniprot instanceof List) && (chebiUniprot.length > 1000)) {
                        List newChebiUniprot = new ArrayList();
                        for (int i=0; i<1000; i++) {newChebiUniprot.add(chebiUniprot[i]);}
                        params._source.chebi.xref.uniprot = newChebiUniprot;
                        truncated.put('chebi.xref.uniprot', true);
                    }
                }
                if (params._source.chebi.xref.containsKey('intenz')) {
                    def chebiIntenz = params._source.chebi.xref.intenz;
                    if ((chebiIntenz instanceof List) && (chebiIntenz.length > 2000)) {
                        List newChebiIntenz = new ArrayList();
                        for (int i=0; i<2000; i++) {newChebiIntenz.add(chebiIntenz[i]);}
                        params._source.chebi.xref.intenz = newChebiIntenz;
                        truncated.put('chebi.xref.intenz', true);
                    }
                }
                if (params._source.chebi.xref.containsKey('rhea')) {
                    def chebiRHEA = params._source.chebi.xref.rhea;
                    if ((chebiRHEA instanceof List) && (chebiRHEA.length > 1000)) {
                        List newChebiRHEA = new ArrayList();
                        for (int i=0; i<1000; i++) {newChebiRHEA.add(chebiRHEA[i]);}
                        params._source.chebi.xref.rhea = newChebiRHEA;
                        truncated.put('chebi.xref.rhea', true);
                    }
                }
                if (params._source.chebi.xref.containsKey('sabio_rk')) {
                    def chebiSabio = params._source.chebi.xref.sabio_rk;
                    if ((chebiSabio instanceof List) && (chebiSabio.length > 1000)) {
                        List newChebiSabio = new ArrayList();
                        for (int i=0; i<1000; i++) {newChebiSabio.add(chebiSabio[i]);}
                        params._source.chebi.xref.sabio_rk = newChebiSabio;
                        truncated.put('chebi.xref.sabio_rk', true);
                    }
                }
                if (params._source.chebi.xref.containsKey('patent')) {
                    def chebiPatent = params._source.chebi.xref.patent;
                    if ((chebiPatent instanceof List) && (chebiPatent.length > 1000)) {
                        List newChebiPatent = new ArrayList();
                        for (int i=0; i<1000; i++) {newChebiPatent.add(chebiPatent[i]);}
                        params._source.chebi.xref.patent = newChebiPatent;
                        truncated.put('chebi.xref.patent', true);
                    }
                }
                if (params._source.chebi.xref.containsKey('reactome')) {
                    def chebiReactome = params._source.chebi.xref.reactome;
                    if ((chebiReactome instanceof List) && (chebiReactome.length > 1000)) {
                        List newChebiReactome = new ArrayList();
                        for (int i=0; i<1000; i++) {newChebiReactome.add(chebiReactome[i]);}
                        params._source.chebi.xref.reactome = newChebiReactome;
                        truncated.put('chebi.xref.reactome', true);
                    }
                }
            }
            if (params._source.containsKey('aeolus') && (params._source.aeolus.containsKey('outcomes')) && (params._source.aeolus.outcomes instanceof List) && (params._source.aeolus.outcomes.length > 5000))  {
                def aeolusOutcomes = params._source.aeolus.outcomes;
                List newAeolusOutcomes = new ArrayList();
                for (int i=0; i<5000; i++) {newAeolusOutcomes.add(aeolusOutcomes[i]);}
                params._source.aeolus.outcomes = newAeolusOutcomes;
                truncated.put('aeolus.outcomes', true);
            }
            if (params._source.containsKey('drugbank')) {
                if  ((params._source.drugbank.containsKey('products')) && (params._source.drugbank.products instanceof List) && (params._source.drugbank.products.length > 5000))  {
                    def drugbankProducts = params._source.drugbank.products;
                    List newDrugbankProducts = new ArrayList();
                    for (int i=0; i<5000; i++) {newDrugbankProducts.add(drugbankProducts[i]);}
                    params._source.drugbank.products = newDrugbankProducts;
                    truncated.put('drugbank.products', true);
                }
                if  ((params._source.drugbank.containsKey('mixtures')) && (params._source.drugbank.mixtures instanceof List) && (params._source.drugbank.mixtures.length > 5000))  {
                    def drugbankMixtures = params._source.drugbank.mixtures;
                    List newDrugbankMixtures = new ArrayList();
                    for (int i=0; i<5000; i++) {newDrugbankMixtures.add(drugbankMixtures[i]);}
                    params._source.drugbank.mixtures = newDrugbankMixtures;
                    truncated.put('drugbank.mixtures', true);
                }
            }
            if (truncated.isEmpty()) {
                return params._source;
            }
            else {
                ret.put('_truncated', truncated);
                ret.putAll(params._source);
                return ret;
            }
        "
    }
}
