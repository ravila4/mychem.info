#!/usr/bin/env bash

if [ -z ${MYSQL_PASS+x} ]; then echo "MYSQL_PASS is unset"; exit 1; fi

echo "SELECT aeolus.standard_drug_outcome_statistics.*,
drug_concept.vocabulary_id AS 'drug_vocabulary',
drug_concept.concept_code AS 'drug_concept_code',
drug_concept.concept_name AS 'drug_name',
outcome_concept.vocabulary_id AS 'outcome_vocabulary',
outcome_concept.concept_code AS 'outcome_concept_code',
outcome_concept.concept_name AS 'outcome_name'
FROM aeolus.standard_drug_outcome_statistics
    LEFT JOIN concept AS drug_concept ON aeolus.standard_drug_outcome_statistics.drug_concept_id=aeolus.drug_concept.concept_id
    LEFT JOIN concept AS outcome_concept ON aeolus.standard_drug_outcome_statistics.outcome_concept_id=aeolus.outcome_concept.concept_id;" |
mysql aeolus -u root --password=$MYSQL_PASS > aeolus.tsv

echo "
SELECT
    concept.concept_id,
    indication_concept_id,
    indication_concept.vocabulary_id AS 'indication_vocabulary',
    indication_concept.concept_code AS 'indication_concept_code',
    indication_concept.concept_name AS 'indication_name',
    COUNT(indi_pt) AS 'indication_count'
FROM
    standard_case_indication
        LEFT JOIN
    standard_case_drug ON standard_case_drug.primaryid = standard_case_indication.primaryid
        AND standard_case_indication.indi_drug_seq = standard_case_drug.drug_seq
        LEFT JOIN
    concept ON standard_case_drug.standard_concept_id = concept.concept_id
        LEFT JOIN
    concept AS indication_concept ON standard_case_indication.indication_concept_id = indication_concept.concept_id
WHERE
    standard_case_drug.role_cod = ('PS')
        #AND concept.concept_id = 723013
GROUP BY concept.concept_id , indication_concept_id
ORDER BY concept.concept_id, indication_count DESC;
" |
mysql aeolus -u root --password=$MYSQL_PASS > aeolus_indications.tsv