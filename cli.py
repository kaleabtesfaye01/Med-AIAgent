from dotenv import load_dotenv

load_dotenv()

import ast
from agent import generate_treatment_plan


def parse_condition(condition_raw: str) -> dict:
    """
    Turn semicolon-separated key:value pairs into a dict.
    Supports Python literals for list/tuple values.
    """
    condition = {}
    for segment in condition_raw.split(";"):
        if ":" not in segment:
            print(f"⚠️ Skipping malformed segment: {segment!r}")
            continue
        key, val = (s.strip() for s in segment.split(":", 1))
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, (list, tuple)):
                condition[key] = list(parsed)
                continue
        except (ValueError, SyntaxError):
            pass
        if "," in val:
            condition[key] = [v.strip() for v in val.split(",") if v.strip()]
        else:
            condition[key] = val
    return condition


def prompt_patient_info() -> None:
    """
    Interactive prompt to gather patient information and generate a treatment plan.
    """
    symptoms = input(
        "\nEnter patient symptoms (include onset, duration, severity, character, alleviating/aggravating factors): "
    ).strip()

    condition_raw = input(
        "Enter physical condition details as key:value pairs separated by ';' (e.g. age:65; allergies:['penicillin']; medications:['aspirin','ibuprofen']): "
    ).strip()
    condition = parse_condition(condition_raw)

    location = input(
        "Enter geographic location (City, State/Region, Country): "
    ).strip()

    raw_input = {
        "symptoms": symptoms,
        "condition": condition,
        "location": location
    }

    try:
        plan = generate_treatment_plan(raw_input)
        print("\nGenerated Treatment Plan:\n")
        print(plan)
    except Exception as e:
        print(f"Error generating treatment plan: {e}")

if __name__ == "__main__":
    prompt_patient_info()