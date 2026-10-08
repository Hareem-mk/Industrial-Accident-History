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

,

    "Chevron Richmond Refinery Fire (USA, 2012)": {

        "schema_version": 2,

        "metadata": {
            "date": "6 August 2012",
            "location": "Richmond, California, USA",
            "type": "Refinery pipe rupture and fire",
            "fatalities": 0,
            "injuries":
                "19 workers endangered by the vapor cloud; approximately "
                "15,000 community members sought medical treatment",
            "investigation_agency":
                "U.S. Chemical Safety and Hazard Investigation Board (CSB)",
            "report_title":
                "Chevron Richmond Refinery Investigation Report",
            "report_number":
                "2012-03-I-CA",
            "report_date":
                "28 January 2015"
        },

        "event_sequence": [
            "The incident occurred in the #4 Crude Unit at the Chevron Richmond Refinery.",
            "A leak developed in the 4-sidecut piping.",
            "The crude unit continued operating while personnel investigated the leak.",
            "A severely thinned carbon steel piping component ruptured.",
            "The pipe failure released hot flammable hydrocarbon process fluid.",
            "A portion of the released hydrocarbon vaporized and formed a large flammable vapor cloud.",
            "Nineteen Chevron employees were engulfed by the vapor cloud but escaped.",
            "The released hydrocarbon ignited and produced a major refinery fire."
        ],

        "contributing_factors": [
            "The failed piping component had experienced severe wall thinning caused by sulfidation corrosion.",
            "The failed carbon steel piping component had low silicon content and was particularly susceptible to accelerated sulfidation corrosion.",
            "Existing inspection practices did not adequately identify the highly corroded low-silicon piping component before failure.",
            "Damage mechanism hazards associated with sulfidation corrosion were not adequately identified and evaluated.",
            "The crude unit was not shut down when the initial leak was detected.",
            "Opportunities to replace susceptible carbon steel piping with more corrosion-resistant material had not been effectively implemented."
        ],

        "system_causes": [
            "The mechanical integrity program did not adequately control the risk from sulfidation corrosion in susceptible piping components.",
            "The process hazard analysis approach did not adequately identify corrosion damage mechanisms as potential causes of loss of containment.",
            "The refinery did not effectively apply inherently safer design principles to eliminate or reduce the sulfidation corrosion hazard.",
            "Management systems did not ensure timely implementation of recommendations concerning susceptible piping and corrosion hazards."
        ],

        "consequences": [
            "Nineteen Chevron employees were engulfed by the flammable vapor cloud but escaped without serious injury.",
            "The hydrocarbon release ignited and resulted in a major refinery fire.",
            "A large plume of combustion products traveled across the surrounding area.",
            "Approximately 15,000 people from the surrounding community sought medical treatment in the weeks following the incident.",
            "Approximately 20 people were admitted to hospitals for treatment."
        ],

        "investigation_findings": [
            "The U.S. Chemical Safety Board investigated the pipe rupture and fire.",
            "The pipe failure resulted from extreme wall thinning caused by sulfidation corrosion.",
            "The CSB identified deficiencies in identifying and evaluating damage mechanism hazards.",
            "The CSB identified missed opportunities to use inherently safer, more corrosion-resistant piping materials.",
            "The CSB examined mechanical integrity practices and refinery process safety management requirements.",
            "The CSB issued recommendations addressing damage mechanism hazard reviews, mechanical integrity, inherently safer design, industry standards, and regulatory oversight."
        ],

        "lessons": [
            "Refinery piping circuits susceptible to sulfidation corrosion require systematic damage mechanism assessment.",
            "Inspection programs must account for component-to-component variations in corrosion susceptibility, including low-silicon carbon steel components.",
            "Material verification and appropriate inspection strategies are necessary where susceptible piping materials may be present.",
            "More corrosion-resistant materials should be considered as an inherently safer means of controlling credible corrosion hazards.",
            "Process hazard analysis should systematically consider applicable damage mechanisms and their potential loss-of-containment consequences.",
            "A hydrocarbon leak from operating process equipment must trigger a conservative assessment of whether continued operation is safe.",
            "Mechanical integrity recommendations involving safety-critical degradation must be tracked and completed in a timely manner."
        ]
    }

,

    "Philadelphia Energy Solutions Refinery Fire and Explosions (USA, 2019)": {

        "schema_version": 2,

        "metadata": {
            "date": "21 June 2019",
            "location": "Philadelphia, Pennsylvania, USA",
            "type": "Refinery fire and explosions following loss of containment",
            "fatalities": 0,
            "injuries":
                "Five workers and one firefighter experienced minor injuries",
            "investigation_agency":
                "U.S. Chemical Safety and Hazard Investigation Board (CSB)",
            "report_title":
                "Fire and Explosions at Philadelphia Energy Solutions Refinery",
            "report_number":
                "2019-04-I-PA",
            "report_date":
                "11 October 2022"
        },

        "event_sequence": [
            "The incident occurred in the hydrofluoric acid alkylation unit at the Philadelphia Energy Solutions refinery.",
            "A pipe elbow in the alkylation unit ruptured after significant corrosion-related wall thinning.",
            "Process fluid containing hydrocarbons and hydrofluoric acid was released.",
            "The release formed a large flammable vapor cloud within the unit.",
            "The flammable vapor cloud ignited and caused a large fire.",
            "Three explosions subsequently occurred in the alkylation unit.",
            "The largest explosion involved the violent rupture of the V-1 Treater Feed Surge Drum.",
            "A large fragment from the ruptured vessel was propelled off-site across the Schuylkill River."
        ],

        "contributing_factors": [
            "The failed pipe elbow experienced accelerated corrosion in hydrofluoric acid service.",
            "The failed carbon steel elbow contained higher nickel and copper content than other piping in the unit, making it more susceptible to accelerated corrosion.",
            "The thickness of the elbow that ultimately failed had not been directly monitored for corrosion.",
            "The mechanical integrity program did not adequately identify and control the corrosion risk associated with the susceptible elbow.",
            "Critical components used to remotely activate hydrofluoric acid mitigation water pumps were damaged by the fire and explosions.",
            "Remotely operated emergency isolation capability was inadequate for rapidly isolating hazardous inventories during the incident."
        ],

        "system_causes": [
            "The refinery mechanical integrity program did not adequately manage the corrosion hazard associated with hydrofluoric acid alkylation service.",
            "Management systems did not adequately verify equipment safety when relevant recognized and generally accepted good engineering practice information changed or became available.",
            "Safeguards important to hydrofluoric acid release mitigation were not sufficiently protected from fire and explosion hazards.",
            "The facility and applicable industry practices did not provide adequate remotely operated emergency isolation capability for hazardous process inventories.",
            "Existing requirements did not ensure systematic evaluation of inherently safer alternatives for hydrofluoric acid alkylation technology."
        ],

        "consequences": [
            "Five workers and one firefighter experienced minor injuries.",
            "Approximately 676,000 pounds of hydrocarbons were released.",
            "More than 5,200 pounds of hydrofluoric acid were released.",
            "The hydrofluoric acid alkylation unit was severely damaged.",
            "The estimated property damage loss was approximately 750 million U.S. dollars.",
            "A vessel fragment weighing approximately 38,000 pounds was propelled off-site across the Schuylkill River.",
            "Philadelphia Energy Solutions subsequently announced that the refining complex would shut down."
        ],

        "investigation_findings": [
            "The U.S. Chemical Safety Board investigated the fire and explosions.",
            "The CSB determined that the pipe elbow failure resulted from corrosion-related wall thinning.",
            "The CSB identified mechanical integrity as a major safety issue.",
            "The CSB identified the need to verify equipment safety when new information or changes to recognized good engineering practices become available.",
            "The CSB identified deficiencies in safeguard reliability in hydrofluoric acid alkylation service.",
            "The CSB identified the need for remotely operated emergency isolation capability.",
            "The CSB identified inherently safer design as an important safety issue for hydrofluoric acid alkylation technology."
        ],

        "lessons": [
            "Mechanical integrity programs must identify and monitor individual components that may have greater susceptibility to corrosion than surrounding piping.",
            "Material composition can significantly affect corrosion behavior and should be considered when managing hydrofluoric acid service piping.",
            "Inspection strategies must ensure that susceptible fittings and components are directly assessed rather than relying only on nearby piping measurements.",
            "Facilities must evaluate new or revised recognized and generally accepted good engineering practice information and determine whether existing equipment remains safe.",
            "Critical mitigation safeguards and their control systems should be protected from credible fire and explosion hazards.",
            "Hazardous process inventories should have effective emergency isolation capability that can be operated from a safe location where appropriate.",
            "Facilities using highly hazardous chemicals should systematically evaluate practicable inherently safer technologies and alternatives."
        ]
    }

,

    'Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)': {'schema_version': 2,
 'metadata': {'date': '11 December 2005',
              'location': 'Hemel Hempstead, Hertfordshire, UK',
              'type': 'Fuel storage tank overfill, vapor cloud explosion and major fire',
              'fatalities': 0,
              'injuries': 'More than 40 people were injured',
              'investigation_agency': 'Buncefield Major Incident Investigation Board (MIIB), '
                                      'supported by the HSE and Environment Agency',
              'report_title': 'Buncefield Major Incident Investigation',
              'report_number': None,
              'report_date': 'Investigation reports issued in multiple stages'},
 'event_sequence': ['The incident occurred at the Buncefield Oil Storage Depot in Hemel Hempstead.',
                    'A gasoline storage tank continued filling and overfilled.',
                    'Gasoline escaped from the overfilled tank.',
                    'The sustained release generated a large flammable gasoline vapor cloud.',
                    'The vapor cloud spread across the site and beyond the site boundary.',
                    'The flammable vapor cloud ignited.',
                    'A series of major explosions occurred.',
                    'Large fires subsequently engulfed a significant proportion of the storage '
                    'depot.'],
 'contributing_factors': ['The tank filling operation was not stopped before the tank overfilled.',
                          'The normal tank level measurement arrangements did not prevent the '
                          'overfill.',
                          'The independent high-level overfill protection did not successfully '
                          'prevent the loss of containment.',
                          'The overfill continued long enough to generate a very large flammable '
                          'vapor cloud.',
                          'The potential consequences of a large vapor cloud explosion at a fuel '
                          'storage depot had not been adequately controlled.',
                          'The incident demonstrated weaknesses in the reliability and management '
                          'of safety-critical overfill protection systems.'],
 'system_causes': ['Management of safety-critical tank level and overfill protection systems was '
                   'inadequate.',
                   'Arrangements for inspection, testing and maintenance of overfill protection '
                   'required improvement.',
                   'Process safety management did not adequately control the major-accident risk '
                   'associated with tank overfilling.',
                   'Major-hazard assessment and emergency planning needed to address severe vapor '
                   'cloud explosions and multi-tank fires.',
                   'Containment and emergency-response arrangements required strengthening for '
                   'credible major fuel-storage incidents.'],
 'consequences': ['There were no fatalities.',
                  'More than 40 people were injured.',
                  'A large proportion of the Buncefield storage depot was destroyed or severely '
                  'damaged.',
                  'Commercial and residential properties surrounding the depot sustained '
                  'significant damage.',
                  'A large surrounding area was evacuated on emergency-service advice.',
                  'The fire continued for several days.',
                  'Large quantities of smoke were released to the atmosphere.',
                  'The incident caused major business interruption and wider economic '
                  'consequences.'],
 'investigation_findings': ['The Health and Safety Executive and Environment Agency investigated '
                            'the incident.',
                            'The Buncefield Major Incident Investigation Board published findings '
                            'and recommendations arising from the incident.',
                            'The investigation established tank overfilling as the initiating '
                            'loss-of-containment event.',
                            'The investigation highlighted the importance of reliable high-level '
                            'overfill protection.',
                            'Post-incident work established stronger expectations for overfill '
                            'prevention and automatic shutdown systems.',
                            'Recommendations addressed secondary and tertiary containment.',
                            'Recommendations also addressed process safety leadership, emergency '
                            'planning and major-hazard management.'],
 'lessons': ['Bulk fuel storage tanks require reliable independent protection against overfilling.',
             'Safety-critical level alarms, trips and shutdown systems require appropriate design, '
             'installation, testing and maintenance.',
             'Independent overfill protection should not depend on the same failure mechanisms as '
             'normal level measurement and control.',
             'Tank transfer operations require clear operating limits and effective response to '
             'abnormal level conditions.',
             'Major-hazard assessments for volatile fuels must consider the possibility of large '
             'flammable vapor-cloud formation following sustained loss of containment.',
             'Secondary and tertiary containment must be capable of limiting the environmental '
             'consequences of major releases and firefighting operations.',
             'Emergency plans for large fuel-storage facilities should consider severe vapor cloud '
             'explosions and multi-tank fires.',
             'Process safety leadership must ensure that safety-critical protective systems remain '
             'effective throughout their operating life.']}
,

    'Deepwater Horizon / Macondo Blowout (Gulf of Mexico, 2010)': {'schema_version': 2,
 'metadata': {'date': '20 April 2010',
              'location': 'Macondo well, Gulf of Mexico',
              'type': 'Offshore well blowout, explosions, fire and oil spill',
              'fatalities': 11,
              'injuries': '17 workers were seriously injured',
              'investigation_agency': 'U.S. Chemical Safety Board (CSB), with separate '
                                      'investigations also conducted by other U.S. authorities',
              'report_title': 'Macondo Investigation Report',
              'report_number': None,
              'report_date': 'CSB investigation volumes issued in multiple stages'},
 'event_sequence': ['The Deepwater Horizon was conducting temporary abandonment operations at the '
                    'Macondo well.',
                    'The cement barrier intended to isolate hydrocarbons from the wellbore did not '
                    'provide an effective seal.',
                    'A negative pressure test was interpreted as indicating that the well was '
                    'adequately sealed.',
                    'Hydrocarbons subsequently flowed into the well.',
                    'The developing well-control event was not detected and controlled before '
                    'hydrocarbons had traveled high in the well toward the rig.',
                    'Oil and gas reached the Deepwater Horizon drilling rig.',
                    'The hydrocarbon release resulted in explosions and a major fire.',
                    'The blowout preventer did not ultimately seal the well.',
                    'The Deepwater Horizon rig sank two days after the accident.',
                    'Oil and gas continued flowing from the Macondo well into the Gulf of Mexico '
                    'for 87 days.'],
 'contributing_factors': ['The cement barrier did not successfully isolate the hydrocarbon-bearing '
                          'formation.',
                          'The negative pressure test did not identify that the well was not '
                          'effectively sealed.',
                          'There were no written procedures defining how to conduct the negative '
                          'pressure test and no written criteria or safe limits for determining '
                          'whether the test was successful.',
                          'The developing influx was not detected and controlled sufficiently '
                          'early.',
                          'Major-accident hazard controls relied significantly on correct and '
                          'timely manual intervention.',
                          'The blowout preventer experienced failures that prevented it from '
                          'reliably sealing the well during the emergency.'],
 'system_causes': ['Management systems did not adequately control the major-accident risks '
                   'associated with temporary abandonment and loss of well control.',
                   'Safety management did not provide sufficiently robust control of '
                   'safety-critical barriers.',
                   'Management of change and hazard assessment arrangements did not adequately '
                   'address changes associated with the temporary abandonment plan.',
                   'Process safety performance management did not sufficiently emphasize '
                   'major-accident prevention.',
                   'Safety-critical BOP systems were not managed with sufficient assurance of '
                   'emergency reliability.'],
 'consequences': ['Eleven workers were killed.',
                  'Seventeen workers were seriously injured.',
                  'The Deepwater Horizon drilling rig was destroyed and sank two days after the '
                  'accident.',
                  'Oil and gas flowed uncontrolled from the Macondo well into the Gulf of Mexico '
                  'for 87 days.',
                  'The incident resulted in a major offshore environmental disaster.'],
 'investigation_findings': ['The U.S. Chemical Safety Board conducted a major process-safety '
                            'investigation of the Macondo blowout and explosion.',
                            'The CSB investigation examined failures of physical, operational and '
                            'organizational safety barriers.',
                            'The CSB examined the failure of the blowout preventer as a '
                            'safety-critical barrier.',
                            'The CSB identified deficiencies in management of safety-critical '
                            'equipment and major-accident risk.',
                            'The CSB examined weaknesses in process safety performance indicators '
                            'and hazard assessment.',
                            'The CSB investigation was published through multiple report volumes '
                            'addressing technical, regulatory and organizational issues.'],
 'lessons': ['Well integrity requires multiple effective and independently verified barriers '
             'against uncontrolled hydrocarbon flow.',
             'Negative pressure tests require clear procedures, acceptance criteria and competent '
             'interpretation.',
             'Early detection and response to well influx are critical to preventing escalation to '
             'a blowout.',
             'Safety-critical blowout prevention equipment must be capable of performing its '
             'required emergency functions under credible accident conditions.',
             'Testing and maintenance programs must identify latent failures in emergency safety '
             'systems.',
             'Major-accident hazard assessments should not rely excessively on timely human '
             'intervention as the principal protective layer.',
             'Management of change must evaluate safety implications of changes to well plans and '
             'temporary abandonment activities.',
             'Process safety indicators should measure the health of major-accident prevention '
             'barriers, not only personal safety performance.']}
,

    'Montara Wellhead Platform Blowout (Timor Sea, 2009)': {'schema_version': 2,
 'metadata': {'date': '21 August 2009',
              'location': 'Montara oil field, Timor Sea, Australia',
              'type': 'Offshore well blowout and uncontrolled oil and gas release',
              'fatalities': 0,
              'injuries': 'Not included in current verified dataset',
              'investigation_agency': 'Australian Government Montara Commission of Inquiry',
              'report_title': 'Report of the Montara Commission of Inquiry',
              'report_number': None,
              'report_date': 'June 2010'},
 'event_sequence': ['Problems occurred during cementing of the 9 5/8-inch casing shoe in the H1 '
                    'well.',
                    'The cemented casing shoe was likely compromised and did not provide a '
                    'reliable primary well-control barrier.',
                    'The 9 5/8-inch cemented casing shoe was not adequately pressure-tested to '
                    'verify its integrity.',
                    'Secondary well-control barriers were also inadequate, missing or not properly '
                    'verified.',
                    'The 9 5/8-inch pressure-containing anti-corrosion cap was removed and was not '
                    'reinstalled before subsequent operations.',
                    'The H1 well was therefore left relying on an unverified primary well-control '
                    'barrier.',
                    'Hydrocarbons entered the H1 well through the failed 9 5/8-inch cemented '
                    'casing shoe.',
                    'Hydrocarbons flowed up the well and an uncontrolled blowout developed.',
                    'Oil and gas were released from the Montara well into the Timor Sea.',
                    'The uncontrolled flow was stopped on 3 November 2009 after intervention '
                    'through a relief well.'],
 'contributing_factors': ['Significant problems occurred during the original cementing operation.',
                          'The cement in the casing shoe was likely compromised by substantial '
                          'over-displacement of fluid, resulting in a wet shoe.',
                          'The significance of the cementing problems was not adequately '
                          'recognized and evaluated.',
                          'The primary cemented casing-shoe barrier was not properly '
                          'pressure-tested after the cementing problems.',
                          'Only one of the two planned pressure-containing anti-corrosion caps was '
                          'installed.',
                          'The installed pressure-containing anti-corrosion cap was not adequately '
                          'tested and verified in situ.',
                          'The installed 9 5/8-inch pressure-containing anti-corrosion cap was '
                          'later removed without establishing a verified replacement barrier.'],
 'system_causes': ["PTTEP Australasia's well-control practices and procedures were deficient.",
                   'Management systems did not ensure that safety-critical well barriers were '
                   'properly installed, verified and maintained.',
                   'Information indicating serious cementing problems was not adequately '
                   'recognized or acted upon by responsible personnel.',
                   "Well construction activities did not consistently comply with the company's "
                   'own Well Construction Standards.',
                   "The company's procedural and operational shortcomings were widespread and "
                   'systemic.',
                   'Regulatory oversight of the Montara well activities was not sufficiently '
                   'diligent.'],
 'consequences': ['There were no fatalities during the initial blowout and evacuation.',
                  'All 69 personnel on the West Atlas drilling rig and Montara wellhead platform '
                  'were safely evacuated.',
                  'Oil and gas were released uncontrollably into the Timor Sea.',
                  'The uncontrolled release continued from 21 August until 3 November 2009.',
                  'The incident required a major offshore oil-spill response.',
                  'The remote location and limitations in baseline and monitoring information made '
                  'the full environmental consequences difficult to determine.'],
 'investigation_findings': ['The Australian Government established the Montara Commission of '
                            'Inquiry to investigate the incident.',
                            'The Inquiry found that hydrocarbons most likely entered the H1 well '
                            'through the 9 5/8-inch cemented casing shoe.',
                            'The Inquiry found that the 9 5/8-inch cemented casing shoe, the '
                            'primary well-control barrier, failed.',
                            'The Inquiry found that the primary barrier had not been adequately '
                            'pressure-tested despite significant problems during cementing.',
                            'The Inquiry identified deficiencies in the installation and '
                            'verification of secondary well-control barriers.',
                            'The Inquiry found widespread and systemic shortcomings in PTTEP '
                            "Australasia's procedures and practices.",
                            'The Inquiry also identified deficiencies in regulatory oversight.',
                            'The Montara Commission of Inquiry made 105 recommendations.'],
 'lessons': ['Every safety-critical well barrier must be positively verified before it is relied '
             'upon for well control.',
             'Abnormal cementing results must trigger formal evaluation, pressure testing and '
             'appropriate remedial action.',
             'A well should not be left dependent on an unverified primary barrier.',
             'Secondary well-control barriers must be suitable for their intended safety function '
             'and independently verified.',
             'Removal of a verified well barrier requires confirmation that adequate alternative '
             'barriers are established.',
             'Well-construction records and abnormal operating information must be reviewed by '
             'competent personnel who understand their process-safety significance.',
             'Well-control procedures must comply with approved well-construction standards and '
             'established good oilfield practice.',
             'Major-accident prevention requires effective organizational assurance as well as '
             'competent field execution.',
             'Regulatory oversight must provide effective assurance that operators are controlling '
             'major well-integrity hazards.']}
,

'Alexander L. Kielland Offshore Platform Disaster (North Sea, 1980)': {'schema_version': 2,
 'metadata': {'date': '27 March 1980',
              'location': 'Ekofisk area, Norwegian North Sea',
              'type': 'Offshore structural failure, loss of stability and capsize',
              'fatalities': 123,
              'injuries': 'Not included in current verified dataset',
              'investigation_agency': 'Norwegian Government Commission of Inquiry',
              'report_title': 'Alexander L. Kielland-ulykken',
              'report_number': 'NOU 1981:11',
              'report_date': '1981'},
 'event_sequence': ['Alexander L. Kielland was operating as an accommodation platform in the '
                    'Ekofisk area of the Norwegian North Sea.',
                    'A fatigue crack had developed in structural brace D-6 at the attachment for a '
                    'hydrophone support.',
                    'The fatigue crack propagated until brace D-6 fractured.',
                    'Following failure of D-6, five other braces connecting column D to the '
                    'platform failed due to overload.',
                    'Column D was lost from the platform structure.',
                    'Loss of column D and its buoyancy caused the platform to develop a severe '
                    'list of approximately 30 to 35 degrees.',
                    'Water entered other columns and deck volumes through openings as the platform '
                    'remained heavily listed.',
                    "Progressive flooding further reduced the platform's stability and buoyancy.",
                    'Alexander L. Kielland capsized approximately 20 minutes after the initial '
                    'structural failure.'],
 'contributing_factors': ['The fatigue crack initiated in the area where a hydrophone support had '
                          'been attached to brace D-6.',
                          'The hydrophone-support attachment incorporated a low-quality fillet '
                          'weld.',
                          'The hydrophone-support detail created a significant stress '
                          'concentration in the load-carrying brace.',
                          'The fatigue crack propagated in the D-6 brace until structural fracture '
                          'occurred.',
                          'The remaining braces connected to column D were unable to withstand the '
                          'redistributed loads after D-6 failed.',
                          'Loss of column D caused a major loss of buoyancy and a severe platform '
                          'list.',
                          'Openings in the structure permitted progressive flooding after the '
                          'platform developed the severe list.',
                          'Severe weather, cold water and the rapid development of the accident '
                          'complicated evacuation and rescue.'],
 'system_causes': ['Deficiencies associated with the design and fabrication of the '
                   'hydrophone-support attachment contributed to fatigue-crack initiation.',
                   'The structural arrangement lacked sufficient redundancy to prevent a local '
                   'brace failure from escalating into loss of an entire column.',
                   'Structural integrity arrangements did not prevent the fatigue crack from '
                   'developing into a catastrophic structural failure.',
                   'The accident demonstrated the need for stronger control of fatigue-critical '
                   'structural details, welding quality and inspection.',
                   'Emergency preparedness and lifesaving arrangements were inadequate for a '
                   'rapidly developing capsize scenario.',
                   'The accident exposed weaknesses in the offshore safety and regulatory '
                   'framework that subsequently required significant improvement.'],
 'consequences': ['There were 212 people aboard Alexander L. Kielland when the accident occurred.',
                  'One hundred and twenty-three people died.',
                  'Eighty-nine people survived.',
                  'The platform capsized approximately 20 minutes after the initial structural '
                  'failure.',
                  'Cold water, severe weather and the rapid capsize greatly complicated evacuation '
                  'and rescue.',
                  'The accident became a major turning point in Norwegian offshore safety.'],
 'investigation_findings': ['The Norwegian Government established a Commission of Inquiry '
                            'following the accident.',
                            'The Commission concluded that the triggering cause of the accident '
                            'was fatigue fracture of structural brace D-6.',
                            'The fatigue crack developed where a hydrophone support had been '
                            'welded to brace D-6.',
                            'The Commission linked development of the fatigue crack to '
                            'deficiencies associated with planning and construction of the '
                            'platform.',
                            'Failure of D-6 caused overload failure of the remaining braces '
                            'connecting column D to the platform.',
                            'Loss of column D caused loss of buoyancy and severe listing.',
                            'Flooding through openings contributed to the rapid loss of stability '
                            'and capsize.',
                            'The official investigation report was published as NOU 1981:11.',
                            'A later review by the Norwegian Office of the Auditor General found '
                            "broad support for the original Commission's conclusion that D-6 "
                            'failed due to fatigue.'],
 'lessons': ['Fatigue-critical structural details require rigorous design assessment throughout '
             'the operating life of an offshore installation.',
             'Attachments welded to primary load-carrying members must be assessed for stress '
             'concentration and fatigue effects.',
             'Welding quality on safety-critical structural members requires effective fabrication '
             'control and inspection.',
             'Structural inspection programs must be capable of detecting fatigue cracking before '
             'it develops into catastrophic fracture.',
             'Offshore structures require adequate redundancy so that a local structural failure '
             'does not readily escalate into global collapse.',
             'Damage-stability assessments must consider progressive flooding following severe '
             'structural damage and loss of buoyancy.',
             'Openings that can contribute to progressive flooding require appropriate design and '
             'control.',
             'Emergency evacuation systems must remain usable during severe list, high waves and '
             'rapidly developing structural emergencies.',
             'Personnel require effective personal survival equipment appropriate for cold '
             'offshore environments.',
             'Major offshore accidents require integrated management of structural integrity, '
             'emergency preparedness and regulatory assurance.']}
,
'Bhopal Gas Disaster (India, 1984)': {'schema_version': 2,
                                       'metadata': {'date': 'Night of 2-3 December 1984',
                                                    'location': 'Bhopal, Madhya Pradesh, India',
                                                    'type': 'Major toxic chemical release '
                                                            'following an uncontrolled exothermic '
                                                            'reaction in methyl isocyanate storage',
                                                    'fatalities': 'Reported fatality totals vary '
                                                                  'by source and reporting period',
                                                    'injuries': 'Large-scale acute exposure '
                                                                'occurred; a single definitive '
                                                                'injury count is not included in '
                                                                'the current verified dataset',
                                                    'investigation_agency': 'Multiple Indian '
                                                                            'government, '
                                                                            'scientific and '
                                                                            'medical bodies',
                                                    'report_title': 'Multiple official technical, '
                                                                    'medical and governmental '
                                                                    'reports',
                                                    'report_number': None,
                                                    'report_date': None},
                                       'event_sequence': ['Methyl isocyanate (MIC) was stored at '
                                                          'the Union Carbide India Limited '
                                                          'pesticide plant in Bhopal.',
                                                          'Water entered MIC storage tank 610.',
                                                          'The water contamination initiated '
                                                          'uncontrolled exothermic reactions in '
                                                          'the MIC-containing tank.',
                                                          'The reaction caused a rapid increase in '
                                                          'temperature and pressure inside tank '
                                                          '610.',
                                                          'The increasing tank pressure resulted '
                                                          'in discharge of toxic material through '
                                                          'the pressure-relief and vent system.',
                                                          'Available mitigation systems did not '
                                                          'prevent the major toxic release from '
                                                          'reaching the atmosphere.',
                                                          'A toxic gas cloud dispersed beyond the '
                                                          'plant boundary into surrounding '
                                                          'populated areas.',
                                                          'Large numbers of people in the '
                                                          'surrounding community were exposed '
                                                          'during the night of 2-3 December 1984.'],
                                       'contributing_factors': ['A substantial inventory of '
                                                                'hazardous methyl isocyanate was '
                                                                'stored at the facility.',
                                                                'The MIC refrigeration system was '
                                                                'not providing its intended '
                                                                'protective function at the time '
                                                                'of the accident.',
                                                                'The vent-gas scrubber did not '
                                                                'provide effective control of the '
                                                                'major release.',
                                                                'The flare system was unavailable '
                                                                'to provide its intended '
                                                                'mitigation function during the '
                                                                'incident.',
                                                                'The combination of unavailable or '
                                                                'ineffective safeguards allowed '
                                                                'the consequences of the runaway '
                                                                'reaction and toxic release to '
                                                                'escalate.',
                                                                'Emergency warning and '
                                                                'community-protection arrangements '
                                                                'were inadequate for a rapidly '
                                                                'developing major toxic release.',
                                                                'The plant was located close to '
                                                                'densely populated communities, '
                                                                'greatly increasing the potential '
                                                                'consequences of an off-site toxic '
                                                                'release.'],
                                       'system_causes': ['Process-safety management arrangements '
                                                         'did not adequately control the major '
                                                         'hazards associated with storage of a '
                                                         'large inventory of highly hazardous MIC.',
                                                         'Safety-critical safeguards were not '
                                                         'maintained in a condition that could '
                                                         'reliably provide their intended '
                                                         'protection.',
                                                         'Management of hazardous chemical '
                                                         'inventory and storage conditions was '
                                                         'inadequate for the potential severity of '
                                                         'an MIC release.',
                                                         'Emergency preparedness was insufficient '
                                                         'for a major off-site toxic-release '
                                                         'scenario.',
                                                         'Community warning, communication and '
                                                         'protective arrangements were inadequate '
                                                         'for the surrounding population.',
                                                         'The accident demonstrated major '
                                                         'weaknesses in management of process '
                                                         'safety, maintenance, emergency '
                                                         'preparedness and major-hazard risk '
                                                         'control.'],
                                       'consequences': ['A large toxic release affected '
                                                        'communities surrounding the Bhopal '
                                                        'pesticide plant.',
                                                        'Thousands of people died, although '
                                                        'reported fatality totals vary '
                                                        'substantially depending on the source and '
                                                        'the period over which deaths are counted.',
                                                        'Large numbers of people experienced acute '
                                                        'toxic exposure and required medical '
                                                        'attention.',
                                                        'Survivors experienced significant '
                                                        'respiratory, ocular and other health '
                                                        'effects.',
                                                        'Long-term health consequences were '
                                                        'documented among exposed populations.',
                                                        'The accident produced severe social, '
                                                        'environmental, medical and economic '
                                                        'consequences for the affected community.',
                                                        'Bhopal became one of the most '
                                                        'consequential industrial chemical '
                                                        'disasters in history.'],
                                       'investigation_findings': ['Official, scientific and '
                                                                  'medical investigations examined '
                                                                  'the causes and consequences of '
                                                                  'the Bhopal disaster.',
                                                                  'Water contamination of MIC '
                                                                  'storage tank 610 was central to '
                                                                  'initiation of the uncontrolled '
                                                                  'chemical reaction.',
                                                                  'The reaction generated a rapid '
                                                                  'increase in temperature and '
                                                                  'pressure in the MIC storage '
                                                                  'system.',
                                                                  'The pressure-relief and vent '
                                                                  'system provided a release path '
                                                                  'for toxic material from the '
                                                                  'pressurized tank.',
                                                                  'Protective and mitigation '
                                                                  'systems did not prevent the '
                                                                  'major toxic release from '
                                                                  'reaching the surrounding '
                                                                  'community.',
                                                                  'The disaster demonstrated '
                                                                  'serious deficiencies in '
                                                                  'major-hazard prevention, '
                                                                  'safety-system availability and '
                                                                  'emergency preparedness.',
                                                                  'Medical investigations '
                                                                  'documented extensive acute and '
                                                                  'long-term health consequences '
                                                                  'among exposed populations.',
                                                                  'The precise route by which '
                                                                  'water entered tank 610 has been '
                                                                  'disputed in published accounts '
                                                                  'and is not asserted as '
                                                                  'conclusively established in '
                                                                  'this verified dataset.'],
                                       'lessons': ['Highly hazardous chemical inventories should '
                                                   'be minimized where practicable to reduce '
                                                   'major-accident potential.',
                                                   'Reactive chemical storage requires strict '
                                                   'prevention of contamination by incompatible '
                                                   'materials such as water.',
                                                   'Safety-critical temperature, pressure and '
                                                   'containment conditions must be continuously '
                                                   'controlled and monitored.',
                                                   'Safety-critical refrigeration and other '
                                                   'preventive safeguards must remain available '
                                                   'and reliable when required by the '
                                                   'process-safety design.',
                                                   'Vent-gas treatment and flare systems must be '
                                                   'designed, maintained and available for '
                                                   'credible major-release scenarios.',
                                                   'Multiple independent protection layers are '
                                                   'required for highly hazardous chemical storage '
                                                   'and processing.',
                                                   'Management of change must evaluate the '
                                                   'process-safety consequences of disabling, '
                                                   'reducing or altering safety-critical systems.',
                                                   'Major-hazard facilities require effective '
                                                   'mechanical-integrity, inspection and '
                                                   'maintenance programs.',
                                                   'Emergency planning must address credible '
                                                   'off-site toxic releases and provide rapid '
                                                   'warning to potentially affected communities.',
                                                   'Communities surrounding major-hazard '
                                                   'facilities require appropriate hazard '
                                                   'communication and emergency-response '
                                                   'arrangements.',
                                                   'Process-safety decisions must consider both '
                                                   'the probability of an initiating event and the '
                                                   'potential severity of off-site consequences.']}
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

