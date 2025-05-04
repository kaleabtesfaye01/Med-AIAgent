import os
from dotenv import load_dotenv
import streamlit as st
from agent import generate_treatment_plan

# Load environment variables
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

# Page configuration
st.set_page_config(
    page_title="AI Treatment Plan Generator",
    layout="wide"
)

# Sidebar: Tech Stack information
with st.sidebar:
    st.markdown("## 🛠️ Tech Stack")
    st.markdown(
        """
        - 🐍 **Python 3.x**
        - ⚡ **Streamlit**
        - 🤖 **OpenAI API**
        - 🌱 **python-dotenv**
        - 🗺️ **googlemaps**
        - 📍 **geopy**
        """
    )
# Initialize session state for inputs and plan
for key in ['symptoms', 'allergies', 'medications', 'preexisting', 'family_history', 'other_details']:
    st.session_state.setdefault(key, [])
st.session_state.setdefault('plan', None)

# Tag-input helper
def tag_input(label: str, key: str, placeholder: str):
    st.subheader(label)
    def add_tag():
        val = st.session_state.get(f"{key}_input", "").strip()
        if val and val not in st.session_state[key]:
            st.session_state[key].append(val)
        st.session_state[f"{key}_input"] = ""
    st.text_input(
        f"{label} (press Enter to add)",
        key=f"{key}_input",
        placeholder=placeholder,
        label_visibility='collapsed',
        on_change=add_tag
    )
    if st.session_state[key]:
        tags_html = " ".join(
            f"<span style='background:#4CAF50; color:white; padding:4px 8px; margin:2px; border-radius:12px; display:inline-block'>{t}</span>"
            for t in st.session_state[key]
        )
        st.markdown(tags_html, unsafe_allow_html=True)

# Determine which page to show: Form if no plan, else Plan
if st.session_state['plan'] is None:
    # --- Form Page ---
    st.title("🩺 AI Treatment Plan Generator")
    st.write("Fill out the sections below and click **Generate Plan**.")

    # Symptoms
    with st.expander("1. Symptoms", expanded=True):
        tag_input("Symptoms", 'symptoms', "e.g. headache, nausea...")

    # Physical Condition
    with st.expander("2. Physical Condition", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30)
            tag_input("Allergies", 'allergies', "e.g. penicillin...")
            tag_input("Medications", 'medications', "e.g. aspirin...")
        with col2:
            tag_input("Pre-existing Conditions", 'preexisting', "e.g. asthma...")
            tag_input("Family History", 'family_history', "e.g. hypertension...")
            tag_input("Other Details", 'other_details', "Any other details...")

    # Location
    with st.expander("3. Location", expanded=True):
        addr_c1, addr_c2 = st.columns([2,1])
        with addr_c1:
            addr1 = st.text_input("Address Line 1", placeholder="123 Main St")
            addr2 = st.text_input("Address Line 2 (optional)")
            city = st.text_input("City")
        with addr_c2:
            state = st.text_input("State/Region")
            country = st.text_input("Country")
            zip_code = st.text_input("ZIP Code")
            postal_code = st.text_input("Postal Code (optional)")

    st.divider()
    if st.button("Generate Plan", type="primary"):
        # Validations
        if not st.session_state['symptoms']:
            st.error("Please add at least one symptom.")
        elif not (addr1 and city and state and country):
            st.error("Please fill in Address Line 1, City, State, and Country.")
        else:
            # Assemble inputs
            location_text = ", ".join(filter(None, [addr1, addr2, city, state, country, zip_code, postal_code]))
            condition = {
                "age": age,
                "allergies": st.session_state['allergies'],
                "medications": st.session_state['medications'],
                "pre_existing_conditions": st.session_state['preexisting'],
                "family_history": st.session_state['family_history'],
                "other_details": st.session_state['other_details'],
            }
            symptoms_text = "; ".join(st.session_state['symptoms'])
            raw_input = {"symptoms": symptoms_text, "condition": condition, "location": location_text}
            with st.spinner("Generating treatment plan..."):
                try:
                    st.session_state['plan'] = generate_treatment_plan(raw_input)
                    st.success("✅ Treatment plan generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating plan: {e}")

else:
    # --- Plan Page ---
    st.title("📋 Preliminary Treatment Plan")
    st.write(st.session_state['plan'])
    if st.button("← Back to Form"):
        # Reset state and show form
        st.session_state['plan'] = None
        for k in ['symptoms','allergies','medications','preexisting','family_history','other_details']:
            st.session_state[k] = []
        st.rerun()
