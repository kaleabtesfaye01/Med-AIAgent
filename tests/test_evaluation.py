import pytest
from agent import generate_treatment_plan
from agent_evaluation.metrics import completeness_score, urgency_validation

@pytest.mark.parametrize("symptoms", [
    "chest pain",
])
def test_generate_not_empty(symptoms):
    payload = {
        "symptoms": symptoms,
        "condition": {
            "age": "50",
            "allergy": "none"
        },
        "location": "NY, NY, USA"
    }
    plan = generate_treatment_plan(payload)
    assert "Immediate Action" in plan

def test_completeness_sections():
    sample = (
        "Immediate Action and Urgency Assessment: ...\n"
        "Recommended Medical Actions: ..."
    )
    assert completeness_score(sample) == 1.0

def test_urgency_validation():
    plan = "Urgency: seek immediate medical attention due to chest pain."
    assert urgency_validation(plan, "chest pain") == 1.0
