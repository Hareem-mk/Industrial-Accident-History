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

        "schema_version": 2,

        "metadata": {
            "date": "23 March 2005",
            "location": "Texas City, Texas, USA",
            "type": "Refinery fire and explosions",
            "fatalities": 15,
            "injuries": 180,
            "investigation_agency":
                "U.S. Chemical Safety and Hazard Investigation Board (CSB)",
            "report_title":
                "BP Texas City Final Investigation Report",
            "report_number":
                "2005-04-I-TX",
            "report_date":
                "20 March 2007"
        },

        "event_sequence": [
            "The incident occurred during startup of the ISOM unit.",
            "The raffinate splitter tower became severely overfilled with hydrocarbons.",
            "Pressure increased in the raffinate splitter tower.",
            "Pressure relief valves opened and discharged hydrocarbons toward the blowdown system.",
            "The blowdown drum and atmospheric vent stack were overwhelmed.",
            "Flammable hydrocarbon liquid and vapor were released to the atmosphere.",
            "The released hydrocarbons formed a flammable vapor cloud that ignited.",
            "The resulting explosions and fire caused multiple fatalities and injuries."
        ],

        "contributing_factors": [
            "Key level instrumentation and alarms did not provide operators with reliable warning of the abnormal tower condition.",
            "The raffinate splitter startup proceeded despite known problems with important level instrumentation.",
            "Previous abnormal startups were not adequately investigated as near-miss events.",
            "The atmospheric blowdown system provided an unsafe means of handling a major flammable hydrocarbon release.",
            "Occupied temporary trailers were located too close to the hazardous process area."
        ],

        "system_causes": [
            "Process safety management systems at the refinery were deficient.",
            "Mechanical integrity and preventive maintenance deficiencies contributed to unsafe equipment conditions.",
            "Management systems did not adequately identify and correct recurring abnormal startup conditions.",
            "The refinery did not adequately address the hazards associated with the atmospheric blowdown system.",
            "Organizational and safety deficiencies existed at multiple levels of the company."
        ],

        "consequences": [
            "Fifteen workers were killed.",
            "Approximately 180 people were injured.",
            "Occupied temporary trailers near the process unit were severely damaged or destroyed.",
            "The incident caused extensive physical damage at the refinery."
        ],

        "investigation_findings": [
            "The U.S. Chemical Safety Board conducted a root-cause investigation of the accident.",
            "The CSB identified organizational and safety deficiencies at multiple levels of BP.",
            "The CSB identified unsafe trailer siting as an important factor that increased the severity of the consequences.",
            "The CSB identified the atmospheric blowdown system as an unsafe design that should be replaced by safer alternatives.",
            "The CSB issued recommendations addressing refinery process safety, corporate oversight, trailer siting, blowdown systems, and regulatory oversight."
        ],

        "lessons": [
            "Startup is a safety-critical operating mode and requires strict control of process conditions and operating procedures.",
            "Safety-critical instruments, alarms, and protective systems must be functional before startup.",
            "Repeated abnormal operating events and near misses must be investigated and their causes corrected.",
            "Atmospheric discharge of large quantities of flammable hydrocarbons should be eliminated in favor of appropriately engineered safer disposal systems.",
            "Occupied temporary buildings and trailers must be located using appropriate process-hazard and facility-siting assessments.",
            "Process safety performance requires effective management oversight, adequate resources, mechanical integrity, competent operations, and learning from previous incidents."
        ]
    },

    "Piper Alpha Offshore Platform Disaster (UK North Sea, 1988)": {

        "schema_version": 2,

        "metadata": {
            "date": "6 July 1988",
            "location": "UK North Sea",
            "type": "Offshore fire and explosions",
            "fatalities": 167,
            "injuries": "Not included in current verified dataset",
            "investigation_agency":
                "UK Government Public Inquiry chaired by Lord Cullen",
            "report_title":
                "The Public Inquiry into the Piper Alpha Disaster",
            "report_date": "1990"
        },

        "event_sequence": [
            "Maintenance work was being carried out on process equipment before the accident.",
            "Permit-to-work failures were important in the sequence of events leading to the disaster.",
            "A hydrocarbon release occurred and ignited.",
            "The event escalated into major fires and explosions.",
            "The Piper Alpha offshore installation was destroyed."
        ],

        "contributing_factors": [
            "Deficiencies existed in the permit-to-work system.",
            "Information concerning maintenance work was not adequately communicated between relevant personnel.",
            "The permit-to-work arrangements did not reliably ensure that process operating staff could readily identify equipment that was under maintenance and unavailable for operation.",
            "Competence in the operation and supervision of the permit-to-work system was inadequate."
        ],

        "system_causes": [
            "Management and control of the permit-to-work system were inadequate.",
            "Maintenance and operations coordination was insufficient.",
            "The management system did not provide sufficiently robust control of safety-critical maintenance information."
        ],

        "consequences": [
            "The disaster resulted in 167 fatalities.",
            "The Piper Alpha offshore production platform was destroyed."
        ],

        "investigation_findings": [
            "The UK Government established a Public Inquiry chaired by Lord Cullen.",
            "The inquiry examined the causes of the disaster and the offshore safety regime.",
            "The Cullen Report resulted in major changes to offshore safety regulation and management in the UK."
        ],

        "lessons": [
            "Permit-to-work systems must provide effective control and communication of safety-critical maintenance activities.",
            "Shift handover must communicate equipment status and outstanding maintenance clearly.",
            "Operations personnel must be able to identify equipment that is unavailable because of maintenance.",
            "Personnel responsible for permit-to-work control require appropriate competence and supervision.",
            "Major-hazard management should not depend on administrative controls alone."
        ]
    }

}



# ---------------------------------------------------------
# BUILD GROUNDED PROMPT
# ---------------------------------------------------------
def build_grounded_prompt(industry, accident):
    """
    Build a grounded prompt from verified accident data.

    Supports:
    - Schema Version 1: legacy flat verified_facts structure
    - Schema Version 2: rich structured evidence
    """

    accident_data = VERIFIED_ACCIDENT_DATA.get(accident)

    if accident_data is None:
        return None

    schema_version = accident_data.get("schema_version", 1)

    # =====================================================
    # SCHEMA VERSION 2 — RICH STRUCTURED DATA
    # =====================================================
    if schema_version == 2:

        metadata = accident_data["metadata"]

        def format_numbered_list(items):
            return "\n".join(
                f"{number}. {item}"
                for number, item in enumerate(items, start=1)
            )

        event_text = format_numbered_list(
            accident_data.get("event_sequence", [])
        )

        contributing_text = format_numbered_list(
            accident_data.get("contributing_factors", [])
        )

        system_text = format_numbered_list(
            accident_data.get("system_causes", [])
        )

        consequences_text = format_numbered_list(
            accident_data.get("consequences", [])
        )

        findings_text = format_numbered_list(
            accident_data.get("investigation_findings", [])
        )

        lessons_text = format_numbered_list(
            accident_data.get("lessons", [])
        )

        metadata_lines = [
            f'Date: {metadata["date"]}',
            f'Location: {metadata["location"]}',
            f'Accident Type: {metadata["type"]}',
            f'Fatalities: {metadata["fatalities"]}',
            f'Injuries: {metadata["injuries"]}',
            f'Investigation Agency: {metadata["investigation_agency"]}',
            f'Investigation Report: {metadata["report_title"]}'
        ]

        # Optional metadata fields appear only when actually supplied.
        if metadata.get("report_number"):
            metadata_lines.append(
                f'Report Number: {metadata["report_number"]}'
            )

        if metadata.get("report_date"):
            metadata_lines.append(
                f'Report Date: {metadata["report_date"]}'
            )

        metadata_text = "\n".join(metadata_lines)

        prompt = f"""
Prepare a technical accident-history case study.

Industry: {industry}
Accident: {accident}

VERIFIED ACCIDENT INFORMATION:

{metadata_text}

VERIFIED EVENT SEQUENCE:

{event_text}

VERIFIED CONTRIBUTING FACTORS:

{contributing_text}

VERIFIED SYSTEM / MANAGEMENT CAUSES:

{system_text}

VERIFIED CONSEQUENCES:

{consequences_text}

VERIFIED INVESTIGATION INFORMATION:

{findings_text}

VERIFIED LESSONS:

{lessons_text}

OUTPUT REQUIREMENTS:

# {accident}

## Verified Accident Information

Display every metadata field supplied above.

Do not create metadata fields that were not supplied.
In particular, do not create a Report Number unless one appears
in VERIFIED ACCIDENT INFORMATION.

## 1. Type of Accident

Describe the accident using the verified information.

## 2. What Went Wrong

### Event Sequence

Incorporate every item supplied under VERIFIED EVENT SEQUENCE.

### Immediate Causes

Identify immediate causes only where supported by the supplied
verified information.

Do not invent detailed equipment failure mechanisms.

### Contributing Factors

Incorporate ALL items supplied under VERIFIED CONTRIBUTING FACTORS.

### Root / System Causes

Incorporate ALL items supplied under VERIFIED SYSTEM / MANAGEMENT CAUSES.

## 3. Effects and Consequences

Use the supplied VERIFIED CONSEQUENCES.

Do not invent casualty or injury information.

## 4. Investigation Report and Recommendations

### Investigation

Use the supplied VERIFIED INVESTIGATION INFORMATION.

### Major Findings

Clearly distinguish verified investigation information from
engineering interpretation.

### Key Recommendations / Lessons Learned

Incorporate ALL items supplied under VERIFIED LESSONS.

## Key Process Safety Lesson

Summarize the principal process-safety lesson in 2-4 sentences.

GROUNDING REQUIREMENTS:

- Treat the supplied information as the factual basis of the report.
- Do not contradict supplied verified information.
- Do not invent casualty figures, dates, locations, report numbers,
  equipment details, investigation findings, recommendations,
  or legal conclusions.
- If additional historical detail is required, explicitly state that
  further verification from the official investigation report is required.
- Clearly distinguish verified historical information from
  engineering interpretation.
"""
        return prompt

    # =====================================================
    # SCHEMA VERSION 1 — LEGACY DATA
    # =====================================================

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
case study in an appropriate section.

Do not silently omit a verified fact.
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

