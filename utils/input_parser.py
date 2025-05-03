from typing import Any, Dict

def parse_patient_input(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize patient input.
    Ensures:
      - symptoms is a descriptive string including onset, duration, severity, character, alleviating/aggravating factors
      - condition is a dict of pre-existing conditions, allergies, medications, and relevant history
      - location is a non-empty string
    """
    symptoms = raw.get("symptoms")
    if not isinstance(symptoms, str) or not symptoms.strip():
        raise ValueError("`symptoms` must be a non-empty description string")

    condition = raw.get("condition")
    if not isinstance(condition, dict):
        raise ValueError("`condition` must be a dict of key:value pairs describing the patient's condition")

    location = raw.get("location")
    if not isinstance(location, str) or not location.strip():
        raise ValueError("`location` must be a non-empty string")

    return {"symptoms": symptoms.strip(), "condition": condition, "location": location.strip()}