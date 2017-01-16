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
    LEFT JOIN concept AS outcome_concept ON aeolus.standard_drug_outcome_statistics.outcome_concept_id=aeolus.outcome_concept.concept_id
;" |
mysql aeolus -u root --password=$MYSQL_PASS > aeolus.tsv