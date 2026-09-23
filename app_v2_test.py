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
# VERIFIED ACCIDENT DATA
# ---------------------------------------------------------
# Version 2:
# This database contains verified information used to ground
# the AI analysis.
#
# IMPORTANT:
# The accident names must exactly match the names used in
# the ACCIDENTS dropdown database.

VERIFIED_ACCIDENT_DATA = {

    "BP Texas City Refinery Explosion (USA, 2005)": {
        "date": "23 March 2005",
        "location": "Texas City, Texas, USA",
        "type": "Fire and explosion",
        "fatalities": 15,
        "injuries": 180,

        "investigation_agency": "U.S. Chemical Safety Board (CSB)",
        "report_title": "BP Texas City Final Investigation Report",
        "report_number": "2005-04-I-TX",
        "report_date": "March 2007",

        "official_source": "https://www.csb.gov/bp-america-texas-city-refinery-explosion/",
        "official_report": "https://www.csb.gov/assets/1/20/CSBFinalReportBP.pdf",

        "verified_facts": [
            "The incident occurred during startup of the ISOM unit.",
            "The raffinate splitter tower became overfilled with hydrocarbons.",
            "Pressure relief devices opened during the event.",
            "Flammable liquid and vapor were released from an atmospheric blowdown stack.",
            "The released hydrocarbons formed a flammable vapor cloud that ignited.",
            "Many victims were located in or around temporary work trailers near the process unit."
        ]
    },

    "Piper Alpha Offshore Platform Disaster (UK North Sea, 1988)": {
        "date": "6 July 1988",
        "location": "UK North Sea",
        "type": "Offshore fire and explosions",
        "fatalities": 167,
        "injuries": "Not included in current verified dataset",

        "investigation_agency": "UK Government Public Inquiry chaired by Lord Cullen",
        "report_title": "The Public Inquiry into the Piper Alpha Disaster",
        "report_number": "Not assigned in current dataset",
        "report_date": "1990",

        "official_source": "https://www.hse.gov.uk/",
        "official_report": "The Public Inquiry into the Piper Alpha Disaster (Cullen Report)",

        "verified_facts": [
            "The Piper Alpha disaster occurred on 6 July 1988.",
            "The disaster resulted in 167 fatalities.",
            "The Piper Alpha offshore production platform was destroyed.",
            "Failures in the permit-to-work system were important in the sequence of events leading to the disaster.",
            "The UK Government established a public inquiry chaired by Lord Cullen.",
            "The Cullen Report led to major changes in the UK offshore safety regime, including the offshore safety case approach."
        ]
    }
}



# ---------------------------------------------------------
# BUILD GROUNDED PROMPT
# ---------------------------------------------------------
def build_grounded_prompt(industry, accident):
    """
    Builds a grounded AI prompt using verified accident data.

    Returns:
        A formatted prompt if verified data exists.
        None if verified data is not yet available.
    """

    accident_data = VERIFIED_ACCIDENT_DATA.get(accident)

    if accident_data is None:
        return None

    facts_text = "\n".join(
        f"{number}. {fact}"
        for number, fact in enumerate(
            accident_data["verified_facts"],
            start=1
        )
    )

    prompt = f"""
Prepare a technical accident-history case study.

Industry: {industry}
Accident: {accident}

VERIFIED INFORMATION:

Date: {accident_data["date"]}
Location: {accident_data["location"]}
Accident Type: {accident_data["type"]}
Fatalities: {accident_data["fatalities"]}
Injuries: {accident_data["injuries"]}

Investigation Agency:
{accident_data["investigation_agency"]}

Investigation Report:
{accident_data["report_title"]}

Report Number:
{accident_data["report_number"]}

Report Date:
{accident_data["report_date"]}

VERIFIED FACTS:

{facts_text}

REQUIRED CASE STUDY STRUCTURE:

# {accident}

## Verified Accident Information

Display ALL of the following verified fields exactly as supplied above:

- Date
- Location
- Accident Type
- Fatalities
- Injuries
- Investigation Agency
- Investigation Report
- Report Number
- Report Date

Do not omit any of these fields.

IMPORTANT:
Every item listed under VERIFIED FACTS must be incorporated into the
case study in an appropriate section. Do not silently omit a verified fact.
Do not change the meaning of a verified fact.

## 1. Type of Accident

## 2. What Went Wrong
### Immediate Causes
### Contributing Factors
### Root / System Causes

Clearly distinguish verified historical facts from
process-safety interpretation.

## 3. Effects and Consequences
### Fatalities and Injuries
### Asset / Production Damage
### Environmental Impact
### Community / Business Impact

Do not invent consequence information that is not supported
by the verified information supplied above.

## 4. Investigation Report and Recommendations
### Investigation
### Major Findings
### Key Recommendations / Lessons Learned

If a specific historical finding or recommendation is not supported
by the verified information above, state that additional verification
from the official investigation report is required.

## Key Process Safety Lesson

Write 2-4 sentences explaining the principal process-safety lesson.
"""

    return prompt


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
    """
    Generates a grounded accident case study.

    The function only calls Groq when verified accident
    data is available in VERIFIED_ACCIDENT_DATA.
    """

    api_key = get_api_key()

    if not api_key:
        st.error(
            "Groq API key not found. Add GROQ_API_KEY to Streamlit Secrets "
            "or set it as an environment variable."
        )
        return None

    # Build the prompt from verified accident data.
    user_prompt = build_grounded_prompt(industry, accident)

    # Stop if this accident has not yet been verified.
    if user_prompt is None:
        st.warning(
            "Verified accident data is not yet available for this case. "
            "The AI analysis was not generated."
        )
        return None

    client = Groq(api_key=api_key)

    system_prompt = """
You are a Senior Process Safety Engineer and industrial accident investigator.

Your task is to analyze historical industrial accidents using the verified
information supplied by the application.

GROUNDING RULES:

1. Treat the supplied VERIFIED INFORMATION and VERIFIED FACTS as the
   primary factual basis for the case study.

2. Do not contradict the supplied verified information.

3. Do not invent casualty figures, dates, locations, investigation agencies,
   report numbers, investigation findings, recommendations, or legal conclusions.

4. Clearly distinguish:
   - Immediate causes
   - Contributing factors
   - Root / systemic causes

5. If an important historical detail is not supported by the supplied
   information, state that additional verification is required rather
   than inventing it.

6. You may provide process-safety interpretation based on established
   engineering principles, but clearly separate interpretation from
   verified historical facts.

7. Use clear, professional technical English suitable for engineers,
   operators, students, and HSE/process-safety professionals.

8. Do not add fictional citations, references, or web links.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
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

