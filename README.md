# Med_AIAgent

A sophisticated medical-advice AI assistant that generates structured, location-aware preliminary treatment plans from patient symptoms and medical history. Includes a comprehensive evaluation framework for measuring response quality.

![Medical AI](https://img.shields.io/badge/Medical-AI-blue)
![Python 3.x](https://img.shields.io/badge/Python-3.x-green)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI-orange)

---

## Overview

Med_AIAgent combines large language models with geolocation capabilities to produce customized preliminary medical treatment plans. The system considers patient symptoms, physical condition, and geographical location to recommend appropriate actions and medical facilities.

**Important**: This tool is designed for educational purposes only and does not replace professional medical advice.

---

## Demo

<div>
    <a href="https://www.loom.com/share/5911ec8eea2641a5bf7b2401d0bbc3af">
      <p>AI Treatment Plan Generator - 3 May 2025 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/5911ec8eea2641a5bf7b2401d0bbc3af">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/5911ec8eea2641a5bf7b2401d0bbc3af-9894ff2442a07b37-full-play.gif">
    </a>
</div>

---

## Features

- **Intelligent Treatment Plan Generation**:

  - **Immediate Action & Urgency Assessment**: Provides time-sensitive recommendations based on symptom severity
  - **Recommended Medical Actions**: Suggests tests, procedures, and over-the-counter medications
  - **Potential Diagnostic Procedures**: Recommends relevant diagnostics with rationale
  - **Specialist Referrals**: Suggests appropriate specialist consultations
  - **Location-Specific Considerations**: Integrates real-time nearby hospital information

- **Geolocation Integration**:

  - Uses Google Places API to identify nearby medical facilities
  - Geocodes patient addresses using Nominatim and Google Geocoding API

- **Comprehensive Evaluation Suite**:

  - **Text Similarity Metrics**: BLEU & ROUGE-L for comparing with gold-standard responses
  - **Structural Completeness Checks**: Validates presence of required sections
  - **Domain-Specific Validation**: Maps symptoms to appropriate urgency levels

- **Streamlit Web Interface**: User-friendly form for inputting patient data

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-org/Med_AIAgent.git
   cd Med_AIAgent
   ```

2. **Set Up Python Environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root with:

   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_PLACES_API_KEY=your_google_places_api_key
   ```

---

## Usage

### Web Interface

Start the Streamlit application:

```bash
streamlit run app.py
```

### Python API

```python
from agent import generate_treatment_plan

# Prepare patient data
payload = {
  "symptoms": "fever, persistent headache, sensitivity to light",
  "condition": {
    "age": "34",
    "allergies": ["penicillin", "shellfish"],
    "medications": ["lisinopril"],
    "pre_existing_conditions": ["hypertension"]
  },
  "location": "Columbus, OH, USA"
}

# Generate treatment plan
plan = generate_treatment_plan(payload)
print(plan)
```

---

## Testing and Evaluation

### Run Automated Tests

```bash
pytest --maxfail=1 --disable-warnings -q
```

### Evaluate Agent Performance

```bash
python -m agent_evaluation.evaluate_agent
```

Results will be displayed in the console and saved to `agent_evaluation/results.csv`.

---

## Project Structure

```
Med_AIAgent/
├── agent.py                # Main treatment plan generator
├── app.py                  # Streamlit web interface
├── utils/                  # Utility functions
│   ├── location_service.py # Geolocation services
│   └── input_parser.py     # Input validation and normalization
├── prompts/                # LLM prompt templates
│   └── treatment_plan_template.txt
├── agent_evaluation/       # Evaluation framework
│   ├── metrics.py          # Evaluation metrics implementation
│   ├── evaluate_agent.py   # Test runner
│   ├── test_cases.yaml     # Test scenarios
│   └── results.csv         # Evaluation results
├── tests/                  # Automated tests
│   └── test_evaluation.py
└── requirements.txt        # Project dependencies
```
