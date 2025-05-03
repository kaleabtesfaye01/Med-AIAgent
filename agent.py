from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI

from utils.input_parser import parse_patient_input
from utils.location_service import geocode, nearest_facilities

load_dotenv()

# 1) Configure the LLM
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")

# 2) Load your prompt template
template_str = open("./prompts/treatment_plan_template.txt").read()
prompt = PromptTemplate.from_template(template_str)

# 3) Compose them: prompt → llm
sequence: RunnableSequence = prompt | llm

def generate_treatment_plan(raw_input: dict) -> str:
    # Parse & geocode
    patient = parse_patient_input(raw_input)
    coords  = geocode(patient["location"])
    nearby  = nearest_facilities(coords)

    # Build the filled template variables
    filled = {
        "symptoms": ", ".join(patient["symptoms"]),
        "condition": ", ".join(f"{k}: {v}" for k, v in patient["condition"].items()),
        "location": f"{patient['location']} ({'; '.join(f['name'] for f in nearby)})"
    }

    # 4) Invoke the prompt+LLM pipeline
    result = sequence.invoke(input = filled)
    
    return result.content

if __name__ == "__main__":
    example = {
        "symptoms": ["chest pain", "shortness of breath"],
        "condition": {"age": 68, "mobility": "limited", "allergies": ["aspirin"]},
        "location": "Covington, KY"
    }
    print(generate_treatment_plan(example))
