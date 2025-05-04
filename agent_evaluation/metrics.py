import nltk
nltk.download('punkt',   quiet=True)
nltk.download('punkt_tab',quiet=True)
from rouge_score import rouge_scorer
import re

# 1) Text‐similarity metrics
def bleu_score(reference: str, hypothesis: str) -> float:
    ref_tokens = [nltk.word_tokenize(reference.lower())]
    hyp_tokens = nltk.word_tokenize(hypothesis.lower())
    return nltk.translate.bleu_score.sentence_bleu(ref_tokens, hyp_tokens)

def rouge_l_score(reference: str, hypothesis: str) -> float:
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return scores['rougeL'].fmeasure

# 2) Rubric: checks for presence of required sections and minimum length
REQUIRED_SECTIONS = [
    r"Immediate Action and Urgency Assessment",
    r"Recommended Medical Actions"
]
def completeness_score(plan_text: str) -> float:
    hits = sum(bool(re.search(section, plan_text, re.IGNORECASE)) for section in REQUIRED_SECTIONS)
    return hits / len(REQUIRED_SECTIONS)

# 3) Medical‐knowledge check: simple rule‐based urgency validator
SYMPTOM_SEVERITY_MAP = {
    'chest pain': 'immediate',
    'shortness of breath': 'immediate',
    'fever': '24h',
    'headache': '48h'
}
def urgency_validation(plan_text: str, symptoms: str) -> float:
    """
    Returns fraction of symptoms whose recommended urgency in plan
    matches our mapping.
    """
    symptoms_list = [s.strip().lower() for s in symptoms.split(',')]
    correct = 0
    for sym in symptoms_list:
        expected = SYMPTOM_SEVERITY_MAP.get(sym)
        if expected and expected in plan_text.lower():
            correct += 1
    return correct / len(symptoms_list) if symptoms_list else 1.0
