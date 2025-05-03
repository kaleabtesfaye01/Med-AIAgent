from typing import Dict, Any

def parse_patient_input(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expect raw = {
      "symptoms": ["fever", "cough"],
      "condition": {"age": 70, "mobility": "wheelchair", "allergies": ["penicillin"]},
      "location": "Covington, KY"
    }
    Return same structure (with validation).
    """
    
    return {
        "symptoms": raw.get("symptoms", []),
        "condition": raw.get("condition", {}),
        "location": raw.get("location", "")
    }