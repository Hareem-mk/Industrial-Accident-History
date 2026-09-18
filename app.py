import os
import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Industrial Accident History Explorer",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------------
# ACCIDENT DATABASE
# ---------------------------------------------------------
# This list controls what appears in the dropdown menus.
# You can add more industries and accidents later.

ACCIDENTS = {
    "Refinery / Downstream Oil & Gas": [
        "BP Texas City Refinery Explosion (USA, 2005)",
        "Chevron Richmond Refinery Fire (USA, 2012)",
        "Philadelphia Energy Solutions Refinery Fire and Explosions (USA, 2019)",
        "Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)"
    ],

    "Upstream Oil & Gas / Offshore": [
        "Piper Alpha Offshore Platform Disaster (UK North Sea, 1988)",
        "Deepwater Horizon / Macondo Blowout (Gulf of Mexico, 2010)",
        "Montara Wellhead Platform Blowout (Timor Sea, 2009)",
        "Alexander L. Kielland Offshore Platform Disaster (North Sea, 1980)"
    ],

    "Chemical Process Industry": [
        "Bhopal Gas Disaster (India, 1984)",
        "Flixborough Chemical Plant Explosion (UK, 1974)",
        "Seveso Chemical Accident (Italy, 1976)",
        "Toulouse AZF Fertilizer Plant Explosion (France, 2001)",
        "West Fertilizer Company Explosion (USA, 2013)"
    ],

    "Petrochemical Industry": [
        "Phillips Petroleum Pasadena Explosion (USA, 1989)",
        "Formosa Plastics Point Comfort Explosion (USA, 2005)",
        "Williams Olefins Geismar Explosion (USA, 2013)"
    ],

    "Storage Tanks / Terminals": [
        "Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)",
        "Jaipur Indian Oil Depot Fire (India, 2009)",
        "ITC Deer Park Tank Farm Fire (USA, 2019)"
    ]
}

# ---------------------------------------------------------
# GET GROQ API KEY
# ---------------------------------------------------------
def get_api_key():
    """
    Tries Streamlit Secrets first.
    If not found, tries the GROQ_API_KEY environment variable.
    """
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


# ---------------------------------------------------------
# CALL GROQ
# ---------------------------------------------------------
def analyze_accident(industry, accident):
    api_key = get_api_key()

    if not api_key:
        st.error(
            "Groq API key not found. Add GROQ_API_KEY to Streamlit Secrets "
            "or set it as an environment variable."
        )
        return None

    client = Groq(api_key=api_key)

    system_prompt = """
You are a Senior Process Safety Engineer and industrial accident investigator.

Your job is to explain historical major industrial accidents accurately,
clearly, and professionally for engineers, operators, HSE personnel, and students.

IMPORTANT RULES:
1. Do not invent facts.
2. If a fact, fatality number, financial loss, or technical detail is uncertain,
   clearly state that it should be verified from the official investigation report.
3. Distinguish immediate causes, contributing causes, and underlying/root causes.
4. Use simple technical English.
5. Focus on process safety lessons.
6. Mention the official investigation organization/report where reliably known
   (for example CSB, HSE, OSHA, NTSB, BOEM/BSEE, Presidential Commission, etc.).
7. Do not fabricate report titles, recommendations, casualty figures, or legal findings.
8. Keep the answer structured and educational.
"""

    user_prompt = f"""
Prepare a technical accident-history case study for:

Industry: {industry}
Accident: {accident}

Use exactly the following main structure:

# {accident}

## 1. Type of Accident
Explain:
- accident category
- major hazardous event involved
- relevant process or equipment
Examples may include explosion, fire, BLEVE, toxic release, blowout,
loss of containment, structural failure, vapor cloud explosion, etc.

## 2. What Went Wrong
Explain the accident sequence step-by-step.

Separate the discussion into:
### Immediate Causes
### Contributing Factors
### Root / System Causes

Address relevant topics such as:
- equipment or mechanical failure
- process deviation
- instrumentation / alarm failure
- isolation failure
- operating procedure
- maintenance
- permit to work
- management of change
- training / competency
- supervision
- safety culture
- design deficiencies
- emergency response

Only include factors that are applicable to this accident.

## 3. Effects and Consequences

Use these subheadings:

### Fatalities and Injuries
Give verified figures when confidently known.
If figures differ by source, say so rather than guessing.

### Asset / Production Damage
Explain major equipment and production consequences.

### Environmental Impact
Describe air, soil, water, marine, fire-water, hydrocarbon,
chemical, or ecological impact where applicable.

### Community / Business Impact
Explain off-site effects, evacuation, public concern,
business interruption, regulatory or reputational impact where applicable.

## 4. Investigation Report and Recommendations

### Investigation
Identify the principal official investigation body or authoritative report
when reliably known.

### Major Findings
Summarize the principal investigation findings.

### Key Recommendations / Lessons Learned
Give 6-10 concise engineering and process-safety lessons.
Where appropriate cover:
- inherently safer design
- safeguards / instrumentation
- alarms and trips
- relief / venting
- mechanical integrity
- inspection and maintenance
- operating procedures
- permit to work / isolation
- management of change
- process hazard analysis
- competency
- emergency response
- leadership and process safety management

Finish with:

## Key Process Safety Lesson
Write 2-4 sentences explaining the single most important lesson from this accident.

Do not add fictional citations or web links.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error while calling Groq API: {e}")
        return None


# ---------------------------------------------------------
# USER INTERFACE
# ---------------------------------------------------------
st.title("🏭 Industrial Accident History Explorer")
st.caption(
    "Explore major accidents from refineries, upstream oil & gas, "
    "petrochemical plants, chemical industries, and storage terminals."
)

st.info(
    "This is an educational AI application. Important casualty figures, "
    "legal conclusions, and technical findings should be verified against "
    "official investigation reports before professional use."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    selected_industry = st.selectbox(
        "1. Select Industry",
        list(ACCIDENTS.keys())
    )

with col2:
    selected_accident = st.selectbox(
        "2. Select Major Accident",
        ACCIDENTS[selected_industry]
    )

st.write("")
generate_button = st.button(
    "Generate Accident Case Study",
    type="primary",
    use_container_width=True
)

if generate_button:
    with st.spinner("Generating the accident case study..."):
        answer = analyze_accident(selected_industry, selected_accident)

    if answer:
        st.divider()
        st.markdown(answer)

        st.download_button(
            label="Download Case Study as Markdown",
            data=answer,
            file_name="industrial_accident_case_study.md",
            mime="text/markdown",
            use_container_width=True
        )

st.divider()

with st.expander("How this app works"):
    st.markdown(
        """
        1. The user selects an industry.
        2. The second dropdown shows relevant historical accidents.
        3. The selected accident is inserted into a structured prompt.
        4. Groq sends the prompt to the LLM.
        5. The model returns a formatted process-safety case study.
        """
    )

