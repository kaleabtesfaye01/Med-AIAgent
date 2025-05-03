import os
from pathlib import Path
from typing import Any, Dict
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI
from utils.input_parser import parse_patient_input
from utils.location_service import geocode, find_nearby_hospitals

class TreatmentPlanAgent:
    def __init__(
        self,
        model_name: str = os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature: float = 0.7
    ):
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)
        template_path = Path(__file__).parent / "prompts" / "treatment_plan_template.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found at {template_path}")
        template_str = template_path.read_text()
        prompt = PromptTemplate(
            input_variables=["symptoms", "condition", "location"],
            template=template_str
        )
        self.pipeline: RunnableSequence = prompt | self.llm

    def generate(
        self,
        raw_input: Dict[str, Any],
        k: int = 3
    ) -> str:
        patient = parse_patient_input(raw_input)
        coords = geocode(patient["location"])
        hospitals = find_nearby_hospitals(coords["lat"], coords["lng"], k=k)

        hospitals_str = ", ".join(
            f"{h['name']} ({h.get('rating', 'N/A')}⭐) - {h['address']}" for h in hospitals
        )

        filled = {
            "symptoms": patient["symptoms"],
            "condition": ", ".join(f"{key}: {val}" for key, val in patient["condition"].items()),
            "location": f"{patient['location']} — Nearest: {hospitals_str}"
        }

        response = self.pipeline.invoke(input=filled)
        return response.content

# Singleton agent instance
_agent = TreatmentPlanAgent()

def generate_treatment_plan(raw_input: Dict[str, Any]) -> str:
    return _agent.generate(raw_input)