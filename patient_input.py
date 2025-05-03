import ast
from agent import generate_treatment_plan

def prompt_cli():
    # 1) Gather
    symptoms = input("Enter patient symptoms (comma-separated): ")
    # turn into list
    symptoms_list = [s.strip() for s in symptoms.split(",") if s.strip()]

    condition_raw = input(
        "Enter physical condition details as key:value pairs (e.g. age:65; allergies:penicillin, sulfa; medications:aspirin,ibuprofen): "
    )
    # turn into dict
    condition = {}
    for pair in condition_raw.split(";"):
        if ":" not in pair:
            print(f"⚠️ Skipping malformed entry {pair!r}")
            continue

        key, val = pair.split(":", 1)
        key = key.strip()
        val = val.strip()
        
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, (list, tuple)):
                condition[key] = list(parsed)
                continue
        except (ValueError, SyntaxError):
            pass

        # Split on semicolons or pipes
        if "," in val:
            condition[key] = [v.strip() for v in val.split(",") if v.strip()]
        else:
            condition[key] = val

    print(f"Parsed condition: {condition}")
    
    location = input("Enter geographic location (City, State/Region, Country): ")

    # 2) Build
    raw_input = {
        "symptoms": symptoms_list,
        "condition": condition,
        "location": location,
    }

    # 3) Call & display
    plan = generate_treatment_plan(raw_input)
    print("\n" + plan)

if __name__ == "__main__":
    prompt_cli()
