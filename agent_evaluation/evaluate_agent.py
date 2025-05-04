import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
import pandas as pd
from agent import generate_treatment_plan
from agent_evaluation.metrics import bleu_score, rouge_l_score, completeness_score, urgency_validation

def load_cases(path='agent_evaluation/test_cases.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

def evaluate_case(case):
    symptoms = case['symptoms']

    # Normalize condition into a dict
    cond_raw = case['condition']
    if isinstance(cond_raw, str):
        parts = [p.strip() for p in cond_raw.split(';') if ':' in p]
        condition = {k.strip(): v.strip() for k, v in (p.split(':', 1) for p in parts)}
    else:
        condition = cond_raw

    location = case['location']
    reference = case['gold_plan']

    # Build payload for the agent
    payload = {
        "symptoms": symptoms,
        "condition": condition,
        "location": location
    }

    hypothesis = generate_treatment_plan(payload)
    return {
        'id': case['id'],
        'BLEU': bleu_score(reference, hypothesis),
        'ROUGE-L': rouge_l_score(reference, hypothesis),
        'Completeness': completeness_score(hypothesis),
        'UrgencyValid': urgency_validation(hypothesis, symptoms)
    }

def main():
    cases = load_cases()
    results = [evaluate_case(c) for c in cases]
    df = pd.DataFrame(results)
    print(df.describe())
    df.to_csv('agent_evaluation/results.csv', index=False)

if __name__ == '__main__':
    main()
