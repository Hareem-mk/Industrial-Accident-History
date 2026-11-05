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


st.markdown(
    """
    <div style="
        width: 100%;
        text-align: right;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: -20px;
        margin-bottom: 5px;
    ">
        MKU
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# ACCIDENT DATABASE
# ---------------------------------------------------------
# This list controls what appears in the dropdown menus.
# You can add more industries and accidents later.

ACCIDENTS = {'Refinery / Downstream Oil & Gas': ['BP Texas City Refinery Explosion (USA, 2005)',
                                     'Chevron Richmond Refinery Fire (USA, 2012)',
                                     'Philadelphia Energy Solutions Refinery Fire and Explosions (USA, 2019)',
                                     'Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)',
                                     'Husky Energy Superior Refinery Explosion and Fire (USA, 2018)',
                                     'ExxonMobil Baton Rouge Refinery Chemical Release and Fire (USA, 2016)',
                                     'Tesoro Anacortes Refinery Fatal Explosion and Fire (USA, 2010)',
                                     'Silver Eagle Refinery Flash Fire and Catastrophic Pipe Explosion (USA, '
                                     '2009)',
                                     'Tosco Avon Refinery Petroleum Naphtha Fire (USA, 1999)'],
 'Upstream Oil & Gas / Offshore': ['Piper Alpha Offshore Platform Disaster (UK North Sea, 1988)',
                                   'Deepwater Horizon / Macondo Blowout (Gulf of Mexico, 2010)',
                                   'Montara Wellhead Platform Blowout (Timor Sea, 2009)',
                                   'Alexander L. Kielland Offshore Platform Disaster (North Sea, 1980)'],
 'Chemical Process Industry': ['Bhopal Gas Disaster (India, 1984)',
                               'Flixborough Chemical Plant Explosion (UK, 1974)',
                               'Seveso Chemical Accident (Italy, 1976)',
                               'Toulouse AZF Fertilizer Plant Explosion (France, 2001)',
                               'West Fertilizer Company Explosion (USA, 2013)'],
 'Petrochemical Industry': ['Phillips Petroleum Pasadena Explosion (USA, 1989)',
                            'Formosa Plastics Point Comfort Explosion (USA, 2005)',
                            'Williams Olefins Geismar Explosion (USA, 2013)',
                            'Shell Polymers Furnace Explosion and Fire (USA, 2025)'],
 'Storage Tanks / Terminals': ['Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)',
                               'Jaipur Indian Oil Depot Fire (India, 2009)',
                               'ITC Deer Park Tank Farm Fire (USA, 2019)',
                               'Caribbean Petroleum Corporation (CAPECO) Tank Explosion and Fire (Puerto '
                               'Rico, 2009)']}

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

VERIFIED_ACCIDENT_DATA = {'BP Texas City Refinery Explosion (USA, 2005)': {'schema_version': 2,
                                                  'metadata': {'date': '23 March 2005',
                                                               'location': 'Texas City, Texas, USA',
                                                               'type': 'Refinery fire and '
                                                                       'explosions',
                                                               'fatalities': 15,
                                                               'injuries': 180,
                                                               'investigation_agency': 'U.S. '
                                                                                       'Chemical '
                                                                                       'Safety and '
                                                                                       'Hazard '
                                                                                       'Investigation '
                                                                                       'Board '
                                                                                       '(CSB)',
                                                               'report_title': 'BP Texas City '
                                                                               'Final '
                                                                               'Investigation '
                                                                               'Report',
                                                               'report_number': '2005-04-I-TX',
                                                               'report_date': '20 March 2007'},
                                                  'event_sequence': ['The incident occurred during '
                                                                     'startup of the ISOM unit.',
                                                                     'The raffinate splitter tower '
                                                                     'became severely overfilled '
                                                                     'with hydrocarbons.',
                                                                     'Pressure increased in the '
                                                                     'raffinate splitter tower.',
                                                                     'Pressure relief valves '
                                                                     'opened and discharged '
                                                                     'hydrocarbons toward the '
                                                                     'blowdown system.',
                                                                     'The blowdown drum and '
                                                                     'atmospheric vent stack were '
                                                                     'overwhelmed.',
                                                                     'Flammable hydrocarbon liquid '
                                                                     'and vapor were released to '
                                                                     'the atmosphere.',
                                                                     'The released hydrocarbons '
                                                                     'formed a flammable vapor '
                                                                     'cloud that ignited.',
                                                                     'The resulting explosions and '
                                                                     'fire caused multiple '
                                                                     'fatalities and injuries.'],
                                                  'contributing_factors': ['Key level '
                                                                           'instrumentation and '
                                                                           'alarms did not provide '
                                                                           'operators with '
                                                                           'reliable warning of '
                                                                           'the abnormal tower '
                                                                           'condition.',
                                                                           'The raffinate splitter '
                                                                           'startup proceeded '
                                                                           'despite known problems '
                                                                           'with important level '
                                                                           'instrumentation.',
                                                                           'Previous abnormal '
                                                                           'startups were not '
                                                                           'adequately '
                                                                           'investigated as '
                                                                           'near-miss events.',
                                                                           'The atmospheric '
                                                                           'blowdown system '
                                                                           'provided an unsafe '
                                                                           'means of handling a '
                                                                           'major flammable '
                                                                           'hydrocarbon release.',
                                                                           'Occupied temporary '
                                                                           'trailers were located '
                                                                           'too close to the '
                                                                           'hazardous process '
                                                                           'area.'],
                                                  'system_causes': ['Process safety management '
                                                                    'systems at the refinery were '
                                                                    'deficient.',
                                                                    'Mechanical integrity and '
                                                                    'preventive maintenance '
                                                                    'deficiencies contributed to '
                                                                    'unsafe equipment conditions.',
                                                                    'Management systems did not '
                                                                    'adequately identify and '
                                                                    'correct recurring abnormal '
                                                                    'startup conditions.',
                                                                    'The refinery did not '
                                                                    'adequately address the '
                                                                    'hazards associated with the '
                                                                    'atmospheric blowdown system.',
                                                                    'Organizational and safety '
                                                                    'deficiencies existed at '
                                                                    'multiple levels of the '
                                                                    'company.'],
                                                  'consequences': ['Fifteen workers were killed.',
                                                                   'Approximately 180 people were '
                                                                   'injured.',
                                                                   'Occupied temporary trailers '
                                                                   'near the process unit were '
                                                                   'severely damaged or destroyed.',
                                                                   'The incident caused extensive '
                                                                   'physical damage at the '
                                                                   'refinery.'],
                                                  'investigation_findings': ['The U.S. Chemical '
                                                                             'Safety Board '
                                                                             'conducted a '
                                                                             'root-cause '
                                                                             'investigation of the '
                                                                             'accident.',
                                                                             'The CSB identified '
                                                                             'organizational and '
                                                                             'safety deficiencies '
                                                                             'at multiple levels '
                                                                             'of BP.',
                                                                             'The CSB identified '
                                                                             'unsafe trailer '
                                                                             'siting as an '
                                                                             'important factor '
                                                                             'that increased the '
                                                                             'severity of the '
                                                                             'consequences.',
                                                                             'The CSB identified '
                                                                             'the atmospheric '
                                                                             'blowdown system as '
                                                                             'an unsafe design '
                                                                             'that should be '
                                                                             'replaced by safer '
                                                                             'alternatives.',
                                                                             'The CSB issued '
                                                                             'recommendations '
                                                                             'addressing refinery '
                                                                             'process safety, '
                                                                             'corporate oversight, '
                                                                             'trailer siting, '
                                                                             'blowdown systems, '
                                                                             'and regulatory '
                                                                             'oversight.'],
                                                  'lessons': ['Startup is a safety-critical '
                                                              'operating mode and requires strict '
                                                              'control of process conditions and '
                                                              'operating procedures.',
                                                              'Safety-critical instruments, '
                                                              'alarms, and protective systems must '
                                                              'be functional before startup.',
                                                              'Repeated abnormal operating events '
                                                              'and near misses must be '
                                                              'investigated and their causes '
                                                              'corrected.',
                                                              'Atmospheric discharge of large '
                                                              'quantities of flammable '
                                                              'hydrocarbons should be eliminated '
                                                              'in favor of appropriately '
                                                              'engineered safer disposal systems.',
                                                              'Occupied temporary buildings and '
                                                              'trailers must be located using '
                                                              'appropriate process-hazard and '
                                                              'facility-siting assessments.',
                                                              'Process safety performance requires '
                                                              'effective management oversight, '
                                                              'adequate resources, mechanical '
                                                              'integrity, competent operations, '
                                                              'and learning from previous '
                                                              'incidents.'],
                                                  'official_sources': [{'organization': 'U.S. '
                                                                                        'Chemical '
                                                                                        'Safety '
                                                                                        'Board',
                                                                        'title': 'BP America '
                                                                                 'Refinery '
                                                                                 'Explosion',
                                                                        'url': 'https://www.csb.gov/bp-america-texas-city-refinery-explosion/',
                                                                        'source_type': 'official_investigation_page',
                                                                        'verified': True},
                                                                       {'organization': 'U.S. '
                                                                                        'Chemical '
                                                                                        'Safety '
                                                                                        'Board',
                                                                        'title': 'Refinery '
                                                                                 'Explosion and '
                                                                                 'Fire — Final '
                                                                                 'Report',
                                                                        'url': 'https://www.csb.gov/assets/1/20/csbfinalreportbp.pdf',
                                                                        'source_type': 'official_investigation_report',
                                                                        'verified': True}]},
 'Piper Alpha Offshore Platform Disaster (UK North Sea, 1988)': {'schema_version': 2,
                                                                 'metadata': {'date': '6 July 1988',
                                                                              'location': 'UK '
                                                                                          'North '
                                                                                          'Sea',
                                                                              'type': 'Offshore '
                                                                                      'fire and '
                                                                                      'explosions',
                                                                              'fatalities': 167,
                                                                              'injuries': 'Not '
                                                                                          'included '
                                                                                          'in '
                                                                                          'current '
                                                                                          'verified '
                                                                                          'dataset',
                                                                              'investigation_agency': 'UK '
                                                                                                      'Government '
                                                                                                      'Public '
                                                                                                      'Inquiry '
                                                                                                      'chaired '
                                                                                                      'by '
                                                                                                      'Lord '
                                                                                                      'Cullen',
                                                                              'report_title': 'The '
                                                                                              'Public '
                                                                                              'Inquiry '
                                                                                              'into '
                                                                                              'the '
                                                                                              'Piper '
                                                                                              'Alpha '
                                                                                              'Disaster',
                                                                              'report_date': '1990'},
                                                                 'event_sequence': ['Maintenance '
                                                                                    'work was '
                                                                                    'being carried '
                                                                                    'out on '
                                                                                    'process '
                                                                                    'equipment '
                                                                                    'before the '
                                                                                    'accident.',
                                                                                    'Permit-to-work '
                                                                                    'failures were '
                                                                                    'important in '
                                                                                    'the sequence '
                                                                                    'of events '
                                                                                    'leading to '
                                                                                    'the disaster.',
                                                                                    'A hydrocarbon '
                                                                                    'release '
                                                                                    'occurred and '
                                                                                    'ignited.',
                                                                                    'The event '
                                                                                    'escalated '
                                                                                    'into major '
                                                                                    'fires and '
                                                                                    'explosions.',
                                                                                    'The Piper '
                                                                                    'Alpha '
                                                                                    'offshore '
                                                                                    'installation '
                                                                                    'was '
                                                                                    'destroyed.'],
                                                                 'contributing_factors': ['Deficiencies '
                                                                                          'existed '
                                                                                          'in the '
                                                                                          'permit-to-work '
                                                                                          'system.',
                                                                                          'Information '
                                                                                          'concerning '
                                                                                          'maintenance '
                                                                                          'work '
                                                                                          'was not '
                                                                                          'adequately '
                                                                                          'communicated '
                                                                                          'between '
                                                                                          'relevant '
                                                                                          'personnel.',
                                                                                          'The '
                                                                                          'permit-to-work '
                                                                                          'arrangements '
                                                                                          'did not '
                                                                                          'reliably '
                                                                                          'ensure '
                                                                                          'that '
                                                                                          'process '
                                                                                          'operating '
                                                                                          'staff '
                                                                                          'could '
                                                                                          'readily '
                                                                                          'identify '
                                                                                          'equipment '
                                                                                          'that '
                                                                                          'was '
                                                                                          'under '
                                                                                          'maintenance '
                                                                                          'and '
                                                                                          'unavailable '
                                                                                          'for '
                                                                                          'operation.',
                                                                                          'Competence '
                                                                                          'in the '
                                                                                          'operation '
                                                                                          'and '
                                                                                          'supervision '
                                                                                          'of the '
                                                                                          'permit-to-work '
                                                                                          'system '
                                                                                          'was '
                                                                                          'inadequate.'],
                                                                 'system_causes': ['Management and '
                                                                                   'control of the '
                                                                                   'permit-to-work '
                                                                                   'system were '
                                                                                   'inadequate.',
                                                                                   'Maintenance '
                                                                                   'and operations '
                                                                                   'coordination '
                                                                                   'was '
                                                                                   'insufficient.',
                                                                                   'The management '
                                                                                   'system did not '
                                                                                   'provide '
                                                                                   'sufficiently '
                                                                                   'robust control '
                                                                                   'of '
                                                                                   'safety-critical '
                                                                                   'maintenance '
                                                                                   'information.'],
                                                                 'consequences': ['The disaster '
                                                                                  'resulted in 167 '
                                                                                  'fatalities.',
                                                                                  'The Piper Alpha '
                                                                                  'offshore '
                                                                                  'production '
                                                                                  'platform was '
                                                                                  'destroyed.'],
                                                                 'investigation_findings': ['The '
                                                                                            'UK '
                                                                                            'Government '
                                                                                            'established '
                                                                                            'a '
                                                                                            'Public '
                                                                                            'Inquiry '
                                                                                            'chaired '
                                                                                            'by '
                                                                                            'Lord '
                                                                                            'Cullen.',
                                                                                            'The '
                                                                                            'inquiry '
                                                                                            'examined '
                                                                                            'the '
                                                                                            'causes '
                                                                                            'of '
                                                                                            'the '
                                                                                            'disaster '
                                                                                            'and '
                                                                                            'the '
                                                                                            'offshore '
                                                                                            'safety '
                                                                                            'regime.',
                                                                                            'The '
                                                                                            'Cullen '
                                                                                            'Report '
                                                                                            'resulted '
                                                                                            'in '
                                                                                            'major '
                                                                                            'changes '
                                                                                            'to '
                                                                                            'offshore '
                                                                                            'safety '
                                                                                            'regulation '
                                                                                            'and '
                                                                                            'management '
                                                                                            'in '
                                                                                            'the '
                                                                                            'UK.'],
                                                                 'lessons': ['Permit-to-work '
                                                                             'systems must provide '
                                                                             'effective control '
                                                                             'and communication of '
                                                                             'safety-critical '
                                                                             'maintenance '
                                                                             'activities.',
                                                                             'Shift handover must '
                                                                             'communicate '
                                                                             'equipment status and '
                                                                             'outstanding '
                                                                             'maintenance clearly.',
                                                                             'Operations personnel '
                                                                             'must be able to '
                                                                             'identify equipment '
                                                                             'that is unavailable '
                                                                             'because of '
                                                                             'maintenance.',
                                                                             'Personnel '
                                                                             'responsible for '
                                                                             'permit-to-work '
                                                                             'control require '
                                                                             'appropriate '
                                                                             'competence and '
                                                                             'supervision.',
                                                                             'Major-hazard '
                                                                             'management should '
                                                                             'not depend on '
                                                                             'administrative '
                                                                             'controls alone.']},
 'Chevron Richmond Refinery Fire (USA, 2012)': {'schema_version': 2,
                                                'metadata': {'date': '6 August 2012',
                                                             'location': 'Richmond, California, '
                                                                         'USA',
                                                             'type': 'Refinery pipe rupture and '
                                                                     'fire',
                                                             'fatalities': 0,
                                                             'injuries': '19 workers endangered by '
                                                                         'the vapor cloud; '
                                                                         'approximately 15,000 '
                                                                         'community members sought '
                                                                         'medical treatment',
                                                             'investigation_agency': 'U.S. '
                                                                                     'Chemical '
                                                                                     'Safety and '
                                                                                     'Hazard '
                                                                                     'Investigation '
                                                                                     'Board (CSB)',
                                                             'report_title': 'Chevron Richmond '
                                                                             'Refinery '
                                                                             'Investigation Report',
                                                             'report_number': '2012-03-I-CA',
                                                             'report_date': '28 January 2015'},
                                                'event_sequence': ['The incident occurred in the '
                                                                   '#4 Crude Unit at the Chevron '
                                                                   'Richmond Refinery.',
                                                                   'A leak developed in the '
                                                                   '4-sidecut piping.',
                                                                   'The crude unit continued '
                                                                   'operating while personnel '
                                                                   'investigated the leak.',
                                                                   'A severely thinned carbon '
                                                                   'steel piping component '
                                                                   'ruptured.',
                                                                   'The pipe failure released hot '
                                                                   'flammable hydrocarbon process '
                                                                   'fluid.',
                                                                   'A portion of the released '
                                                                   'hydrocarbon vaporized and '
                                                                   'formed a large flammable vapor '
                                                                   'cloud.',
                                                                   'Nineteen Chevron employees '
                                                                   'were engulfed by the vapor '
                                                                   'cloud but escaped.',
                                                                   'The released hydrocarbon '
                                                                   'ignited and produced a major '
                                                                   'refinery fire.'],
                                                'contributing_factors': ['The failed piping '
                                                                         'component had '
                                                                         'experienced severe wall '
                                                                         'thinning caused by '
                                                                         'sulfidation corrosion.',
                                                                         'The failed carbon steel '
                                                                         'piping component had low '
                                                                         'silicon content and was '
                                                                         'particularly susceptible '
                                                                         'to accelerated '
                                                                         'sulfidation corrosion.',
                                                                         'Existing inspection '
                                                                         'practices did not '
                                                                         'adequately identify the '
                                                                         'highly corroded '
                                                                         'low-silicon piping '
                                                                         'component before '
                                                                         'failure.',
                                                                         'Damage mechanism hazards '
                                                                         'associated with '
                                                                         'sulfidation corrosion '
                                                                         'were not adequately '
                                                                         'identified and '
                                                                         'evaluated.',
                                                                         'The crude unit was not '
                                                                         'shut down when the '
                                                                         'initial leak was '
                                                                         'detected.',
                                                                         'Opportunities to replace '
                                                                         'susceptible carbon steel '
                                                                         'piping with more '
                                                                         'corrosion-resistant '
                                                                         'material had not been '
                                                                         'effectively '
                                                                         'implemented.'],
                                                'system_causes': ['The mechanical integrity '
                                                                  'program did not adequately '
                                                                  'control the risk from '
                                                                  'sulfidation corrosion in '
                                                                  'susceptible piping components.',
                                                                  'The process hazard analysis '
                                                                  'approach did not adequately '
                                                                  'identify corrosion damage '
                                                                  'mechanisms as potential causes '
                                                                  'of loss of containment.',
                                                                  'The refinery did not '
                                                                  'effectively apply inherently '
                                                                  'safer design principles to '
                                                                  'eliminate or reduce the '
                                                                  'sulfidation corrosion hazard.',
                                                                  'Management systems did not '
                                                                  'ensure timely implementation of '
                                                                  'recommendations concerning '
                                                                  'susceptible piping and '
                                                                  'corrosion hazards.'],
                                                'consequences': ['Nineteen Chevron employees were '
                                                                 'engulfed by the flammable vapor '
                                                                 'cloud but escaped without '
                                                                 'serious injury.',
                                                                 'The hydrocarbon release ignited '
                                                                 'and resulted in a major refinery '
                                                                 'fire.',
                                                                 'A large plume of combustion '
                                                                 'products traveled across the '
                                                                 'surrounding area.',
                                                                 'Approximately 15,000 people from '
                                                                 'the surrounding community sought '
                                                                 'medical treatment in the weeks '
                                                                 'following the incident.',
                                                                 'Approximately 20 people were '
                                                                 'admitted to hospitals for '
                                                                 'treatment.'],
                                                'investigation_findings': ['The U.S. Chemical '
                                                                           'Safety Board '
                                                                           'investigated the pipe '
                                                                           'rupture and fire.',
                                                                           'The pipe failure '
                                                                           'resulted from extreme '
                                                                           'wall thinning caused '
                                                                           'by sulfidation '
                                                                           'corrosion.',
                                                                           'The CSB identified '
                                                                           'deficiencies in '
                                                                           'identifying and '
                                                                           'evaluating damage '
                                                                           'mechanism hazards.',
                                                                           'The CSB identified '
                                                                           'missed opportunities '
                                                                           'to use inherently '
                                                                           'safer, more '
                                                                           'corrosion-resistant '
                                                                           'piping materials.',
                                                                           'The CSB examined '
                                                                           'mechanical integrity '
                                                                           'practices and refinery '
                                                                           'process safety '
                                                                           'management '
                                                                           'requirements.',
                                                                           'The CSB issued '
                                                                           'recommendations '
                                                                           'addressing damage '
                                                                           'mechanism hazard '
                                                                           'reviews, mechanical '
                                                                           'integrity, inherently '
                                                                           'safer design, industry '
                                                                           'standards, and '
                                                                           'regulatory oversight.'],
                                                'lessons': ['Refinery piping circuits susceptible '
                                                            'to sulfidation corrosion require '
                                                            'systematic damage mechanism '
                                                            'assessment.',
                                                            'Inspection programs must account for '
                                                            'component-to-component variations in '
                                                            'corrosion susceptibility, including '
                                                            'low-silicon carbon steel components.',
                                                            'Material verification and appropriate '
                                                            'inspection strategies are necessary '
                                                            'where susceptible piping materials '
                                                            'may be present.',
                                                            'More corrosion-resistant materials '
                                                            'should be considered as an inherently '
                                                            'safer means of controlling credible '
                                                            'corrosion hazards.',
                                                            'Process hazard analysis should '
                                                            'systematically consider applicable '
                                                            'damage mechanisms and their potential '
                                                            'loss-of-containment consequences.',
                                                            'A hydrocarbon leak from operating '
                                                            'process equipment must trigger a '
                                                            'conservative assessment of whether '
                                                            'continued operation is safe.',
                                                            'Mechanical integrity recommendations '
                                                            'involving safety-critical degradation '
                                                            'must be tracked and completed in a '
                                                            'timely manner.']},
 'Philadelphia Energy Solutions Refinery Fire and Explosions (USA, 2019)': {'schema_version': 2,
                                                                            'metadata': {'date': '21 '
                                                                                                 'June '
                                                                                                 '2019',
                                                                                         'location': 'Philadelphia, '
                                                                                                     'Pennsylvania, '
                                                                                                     'USA',
                                                                                         'type': 'Refinery '
                                                                                                 'fire '
                                                                                                 'and '
                                                                                                 'explosions '
                                                                                                 'following '
                                                                                                 'loss '
                                                                                                 'of '
                                                                                                 'containment',
                                                                                         'fatalities': 0,
                                                                                         'injuries': 'Five '
                                                                                                     'workers '
                                                                                                     'and '
                                                                                                     'one '
                                                                                                     'firefighter '
                                                                                                     'experienced '
                                                                                                     'minor '
                                                                                                     'injuries',
                                                                                         'investigation_agency': 'U.S. '
                                                                                                                 'Chemical '
                                                                                                                 'Safety '
                                                                                                                 'and '
                                                                                                                 'Hazard '
                                                                                                                 'Investigation '
                                                                                                                 'Board '
                                                                                                                 '(CSB)',
                                                                                         'report_title': 'Fire '
                                                                                                         'and '
                                                                                                         'Explosions '
                                                                                                         'at '
                                                                                                         'Philadelphia '
                                                                                                         'Energy '
                                                                                                         'Solutions '
                                                                                                         'Refinery',
                                                                                         'report_number': '2019-04-I-PA',
                                                                                         'report_date': '11 '
                                                                                                        'October '
                                                                                                        '2022'},
                                                                            'event_sequence': ['The '
                                                                                               'incident '
                                                                                               'occurred '
                                                                                               'in '
                                                                                               'the '
                                                                                               'hydrofluoric '
                                                                                               'acid '
                                                                                               'alkylation '
                                                                                               'unit '
                                                                                               'at '
                                                                                               'the '
                                                                                               'Philadelphia '
                                                                                               'Energy '
                                                                                               'Solutions '
                                                                                               'refinery.',
                                                                                               'A '
                                                                                               'pipe '
                                                                                               'elbow '
                                                                                               'in '
                                                                                               'the '
                                                                                               'alkylation '
                                                                                               'unit '
                                                                                               'ruptured '
                                                                                               'after '
                                                                                               'significant '
                                                                                               'corrosion-related '
                                                                                               'wall '
                                                                                               'thinning.',
                                                                                               'Process '
                                                                                               'fluid '
                                                                                               'containing '
                                                                                               'hydrocarbons '
                                                                                               'and '
                                                                                               'hydrofluoric '
                                                                                               'acid '
                                                                                               'was '
                                                                                               'released.',
                                                                                               'The '
                                                                                               'release '
                                                                                               'formed '
                                                                                               'a '
                                                                                               'large '
                                                                                               'flammable '
                                                                                               'vapor '
                                                                                               'cloud '
                                                                                               'within '
                                                                                               'the '
                                                                                               'unit.',
                                                                                               'The '
                                                                                               'flammable '
                                                                                               'vapor '
                                                                                               'cloud '
                                                                                               'ignited '
                                                                                               'and '
                                                                                               'caused '
                                                                                               'a '
                                                                                               'large '
                                                                                               'fire.',
                                                                                               'Three '
                                                                                               'explosions '
                                                                                               'subsequently '
                                                                                               'occurred '
                                                                                               'in '
                                                                                               'the '
                                                                                               'alkylation '
                                                                                               'unit.',
                                                                                               'The '
                                                                                               'largest '
                                                                                               'explosion '
                                                                                               'involved '
                                                                                               'the '
                                                                                               'violent '
                                                                                               'rupture '
                                                                                               'of '
                                                                                               'the '
                                                                                               'V-1 '
                                                                                               'Treater '
                                                                                               'Feed '
                                                                                               'Surge '
                                                                                               'Drum.',
                                                                                               'A '
                                                                                               'large '
                                                                                               'fragment '
                                                                                               'from '
                                                                                               'the '
                                                                                               'ruptured '
                                                                                               'vessel '
                                                                                               'was '
                                                                                               'propelled '
                                                                                               'off-site '
                                                                                               'across '
                                                                                               'the '
                                                                                               'Schuylkill '
                                                                                               'River.'],
                                                                            'contributing_factors': ['The '
                                                                                                     'failed '
                                                                                                     'pipe '
                                                                                                     'elbow '
                                                                                                     'experienced '
                                                                                                     'accelerated '
                                                                                                     'corrosion '
                                                                                                     'in '
                                                                                                     'hydrofluoric '
                                                                                                     'acid '
                                                                                                     'service.',
                                                                                                     'The failed steel elbow contained higher concentrations of nickel and copper than adjacent piping components, causing it to corrode faster in hydrofluoric acid service.',
                                                                                                     'The failed elbow had no designated condition monitoring location (CML), and the inspection program did not inspect all carbon steel piping components susceptible to hydrofluoric acid corrosion.',
                                                                                                     'The '
                                                                                                     'mechanical '
                                                                                                     'integrity '
                                                                                                     'program '
                                                                                                     'did '
                                                                                                     'not '
                                                                                                     'adequately '
                                                                                                     'identify '
                                                                                                     'and '
                                                                                                     'control '
                                                                                                     'the '
                                                                                                     'corrosion '
                                                                                                     'risk '
                                                                                                     'associated '
                                                                                                     'with '
                                                                                                     'the '
                                                                                                     'susceptible '
                                                                                                     'elbow.',
                                                                                                     "Fire rendered the water mitigation system's control and backup systems inoperable, preventing remote activation of the hydrofluoric acid mitigation water pumps.",
                                                                                                     'Remotely '
                                                                                                     'operated '
                                                                                                     'emergency '
                                                                                                     'isolation '
                                                                                                     'capability '
                                                                                                     'was '
                                                                                                     'inadequate '
                                                                                                     'for '
                                                                                                     'rapidly '
                                                                                                     'isolating '
                                                                                                     'hazardous '
                                                                                                     'inventories '
                                                                                                     'during '
                                                                                                     'the '
                                                                                                     'incident.'],
                                                                            'system_causes': ['The '
                                                                                              'refinery '
                                                                                              'mechanical '
                                                                                              'integrity '
                                                                                              'program '
                                                                                              'did '
                                                                                              'not '
                                                                                              'adequately '
                                                                                              'manage '
                                                                                              'the '
                                                                                              'corrosion '
                                                                                              'hazard '
                                                                                              'associated '
                                                                                              'with '
                                                                                              'hydrofluoric '
                                                                                              'acid '
                                                                                              'alkylation '
                                                                                              'service.',
                                                                                              'Management '
                                                                                              'systems '
                                                                                              'did '
                                                                                              'not '
                                                                                              'adequately '
                                                                                              'verify '
                                                                                              'equipment '
                                                                                              'safety '
                                                                                              'when '
                                                                                              'relevant '
                                                                                              'recognized '
                                                                                              'and '
                                                                                              'generally '
                                                                                              'accepted '
                                                                                              'good '
                                                                                              'engineering '
                                                                                              'practice '
                                                                                              'information '
                                                                                              'changed '
                                                                                              'or '
                                                                                              'became '
                                                                                              'available.',
                                                                                              'Safeguards '
                                                                                              'important '
                                                                                              'to '
                                                                                              'hydrofluoric '
                                                                                              'acid '
                                                                                              'release '
                                                                                              'mitigation '
                                                                                              'were '
                                                                                              'not '
                                                                                              'sufficiently '
                                                                                              'protected '
                                                                                              'from '
                                                                                              'fire '
                                                                                              'and '
                                                                                              'explosion '
                                                                                              'hazards.',
                                                                                              'The '
                                                                                              'facility '
                                                                                              'and '
                                                                                              'applicable '
                                                                                              'industry '
                                                                                              'practices '
                                                                                              'did '
                                                                                              'not '
                                                                                              'provide '
                                                                                              'adequate '
                                                                                              'remotely '
                                                                                              'operated '
                                                                                              'emergency '
                                                                                              'isolation '
                                                                                              'capability '
                                                                                              'for '
                                                                                              'hazardous '
                                                                                              'process '
                                                                                              'inventories.',
                                                                                              "The CSB's October 2022 report identified the absence of a federal requirement for petroleum refineries to analyze and implement inherently safer design strategies to reduce serious accidental release risks."],
                                                                            'consequences': ['Five '
                                                                                             'workers '
                                                                                             'and '
                                                                                             'one '
                                                                                             'firefighter '
                                                                                             'experienced '
                                                                                             'minor '
                                                                                             'injuries.',
                                                                                             'Approximately '
                                                                                             '676,000 '
                                                                                             'pounds '
                                                                                             'of '
                                                                                             'hydrocarbons '
                                                                                             'were '
                                                                                             'released.',
                                                                                             'PES estimated that 5,239 pounds of hydrofluoric acid were released from piping and equipment; 1,968 pounds were contained by water spray, while 3,271 pounds were released to the atmosphere without water-spray containment.',
                                                                                             'The '
                                                                                             'hydrofluoric '
                                                                                             'acid '
                                                                                             'alkylation '
                                                                                             'unit '
                                                                                             'was '
                                                                                             'severely '
                                                                                             'damaged.',
                                                                                             'The '
                                                                                             'estimated '
                                                                                             'property '
                                                                                             'damage '
                                                                                             'loss '
                                                                                             'was '
                                                                                             'approximately '
                                                                                             '750 '
                                                                                             'million '
                                                                                             'U.S. '
                                                                                             'dollars.',
                                                                                             'A '
                                                                                             'vessel '
                                                                                             'fragment '
                                                                                             'weighing '
                                                                                             'approximately '
                                                                                             '38,000 '
                                                                                             'pounds '
                                                                                             'was '
                                                                                             'propelled '
                                                                                             'off-site '
                                                                                             'across '
                                                                                             'the '
                                                                                             'Schuylkill '
                                                                                             'River.',
                                                                                             'Philadelphia '
                                                                                             'Energy '
                                                                                             'Solutions '
                                                                                             'subsequently '
                                                                                             'announced '
                                                                                             'that '
                                                                                             'the '
                                                                                             'refining '
                                                                                             'complex '
                                                                                             'would '
                                                                                             'shut '
                                                                                             'down.'],
                                                                            'investigation_findings': ['The '
                                                                                                       'U.S. '
                                                                                                       'Chemical '
                                                                                                       'Safety '
                                                                                                       'Board '
                                                                                                       'investigated '
                                                                                                       'the '
                                                                                                       'fire '
                                                                                                       'and '
                                                                                                       'explosions.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'determined '
                                                                                                       'that '
                                                                                                       'the '
                                                                                                       'pipe '
                                                                                                       'elbow '
                                                                                                       'failure '
                                                                                                       'resulted '
                                                                                                       'from '
                                                                                                       'corrosion-related '
                                                                                                       'wall '
                                                                                                       'thinning.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'identified '
                                                                                                       'mechanical '
                                                                                                       'integrity '
                                                                                                       'as '
                                                                                                       'a '
                                                                                                       'major '
                                                                                                       'safety '
                                                                                                       'issue.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'identified '
                                                                                                       'the '
                                                                                                       'need '
                                                                                                       'to '
                                                                                                       'verify '
                                                                                                       'equipment '
                                                                                                       'safety '
                                                                                                       'when '
                                                                                                       'new '
                                                                                                       'information '
                                                                                                       'or '
                                                                                                       'changes '
                                                                                                       'to '
                                                                                                       'recognized '
                                                                                                       'good '
                                                                                                       'engineering '
                                                                                                       'practices '
                                                                                                       'become '
                                                                                                       'available.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'identified '
                                                                                                       'deficiencies '
                                                                                                       'in '
                                                                                                       'safeguard '
                                                                                                       'reliability '
                                                                                                       'in '
                                                                                                       'hydrofluoric '
                                                                                                       'acid '
                                                                                                       'alkylation '
                                                                                                       'service.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'identified '
                                                                                                       'the '
                                                                                                       'need '
                                                                                                       'for '
                                                                                                       'remotely '
                                                                                                       'operated '
                                                                                                       'emergency '
                                                                                                       'isolation '
                                                                                                       'capability.',
                                                                                                       'The '
                                                                                                       'CSB '
                                                                                                       'identified '
                                                                                                       'inherently '
                                                                                                       'safer '
                                                                                                       'design '
                                                                                                       'as '
                                                                                                       'an '
                                                                                                       'important '
                                                                                                       'safety '
                                                                                                       'issue '
                                                                                                       'for '
                                                                                                       'hydrofluoric '
                                                                                                       'acid '
                                                                                                       'alkylation '
                                                                                                       'technology.'],
                                                                            'lessons': ['Mechanical '
                                                                                        'integrity '
                                                                                        'programs '
                                                                                        'must '
                                                                                        'identify '
                                                                                        'and '
                                                                                        'monitor '
                                                                                        'individual '
                                                                                        'components '
                                                                                        'that may '
                                                                                        'have '
                                                                                        'greater '
                                                                                        'susceptibility '
                                                                                        'to '
                                                                                        'corrosion '
                                                                                        'than '
                                                                                        'surrounding '
                                                                                        'piping.',
                                                                                        'Material '
                                                                                        'composition '
                                                                                        'can '
                                                                                        'significantly '
                                                                                        'affect '
                                                                                        'corrosion '
                                                                                        'behavior '
                                                                                        'and '
                                                                                        'should be '
                                                                                        'considered '
                                                                                        'when '
                                                                                        'managing '
                                                                                        'hydrofluoric '
                                                                                        'acid '
                                                                                        'service '
                                                                                        'piping.',
                                                                                        'Inspection '
                                                                                        'strategies '
                                                                                        'must '
                                                                                        'ensure '
                                                                                        'that '
                                                                                        'susceptible '
                                                                                        'fittings '
                                                                                        'and '
                                                                                        'components '
                                                                                        'are '
                                                                                        'directly '
                                                                                        'assessed '
                                                                                        'rather '
                                                                                        'than '
                                                                                        'relying '
                                                                                        'only on '
                                                                                        'nearby '
                                                                                        'piping '
                                                                                        'measurements.',
                                                                                        'Facilities '
                                                                                        'must '
                                                                                        'evaluate '
                                                                                        'new or '
                                                                                        'revised '
                                                                                        'recognized '
                                                                                        'and '
                                                                                        'generally '
                                                                                        'accepted '
                                                                                        'good '
                                                                                        'engineering '
                                                                                        'practice '
                                                                                        'information '
                                                                                        'and '
                                                                                        'determine '
                                                                                        'whether '
                                                                                        'existing '
                                                                                        'equipment '
                                                                                        'remains '
                                                                                        'safe.',
                                                                                        'Critical '
                                                                                        'mitigation '
                                                                                        'safeguards '
                                                                                        'and their '
                                                                                        'control '
                                                                                        'systems '
                                                                                        'should be '
                                                                                        'protected '
                                                                                        'from '
                                                                                        'credible '
                                                                                        'fire and '
                                                                                        'explosion '
                                                                                        'hazards.',
                                                                                        'Hazardous '
                                                                                        'process '
                                                                                        'inventories '
                                                                                        'should '
                                                                                        'have '
                                                                                        'effective '
                                                                                        'emergency '
                                                                                        'isolation '
                                                                                        'capability '
                                                                                        'that can '
                                                                                        'be '
                                                                                        'operated '
                                                                                        'from a '
                                                                                        'safe '
                                                                                        'location '
                                                                                        'where '
                                                                                        'appropriate.',
                                                                                        'Refiners operating hydrofluoric acid alkylation units should periodically evaluate emerging alternative alkylation technologies that could prevent toxic hydrofluoric acid releases.']},
 'Buncefield Oil Storage Depot Explosion and Fire (UK, 2005)': {'schema_version': 2,
                                                                'metadata': {'date': '11 December '
                                                                                     '2005',
                                                                             'location': 'Hemel '
                                                                                         'Hempstead, '
                                                                                         'Hertfordshire, '
                                                                                         'UK',
                                                                             'type': 'Fuel storage '
                                                                                     'tank '
                                                                                     'overfill, '
                                                                                     'vapor cloud '
                                                                                     'explosion '
                                                                                     'and major '
                                                                                     'fire',
                                                                             'fatalities': 0,
                                                                             'injuries': 'More '
                                                                                         'than 40 '
                                                                                         'people '
                                                                                         'were '
                                                                                         'injured',
                                                                             'investigation_agency': 'Buncefield '
                                                                                                     'Major '
                                                                                                     'Incident '
                                                                                                     'Investigation '
                                                                                                     'Board '
                                                                                                     '(MIIB), '
                                                                                                     'supported '
                                                                                                     'by '
                                                                                                     'the '
                                                                                                     'HSE '
                                                                                                     'and '
                                                                                                     'Environment '
                                                                                                     'Agency',
                                                                             'report_title': 'Buncefield '
                                                                                             'Major '
                                                                                             'Incident '
                                                                                             'Investigation',
                                                                             'report_number': None,
                                                                             'report_date': 'Investigation '
                                                                                            'reports '
                                                                                            'issued '
                                                                                            'in '
                                                                                            'multiple '
                                                                                            'stages'},
                                                                'event_sequence': ['The incident '
                                                                                   'occurred at '
                                                                                   'the Buncefield '
                                                                                   'Oil Storage '
                                                                                   'Depot in Hemel '
                                                                                   'Hempstead.',
                                                                                   'A gasoline '
                                                                                   'storage tank '
                                                                                   'continued '
                                                                                   'filling and '
                                                                                   'overfilled.',
                                                                                   'Gasoline '
                                                                                   'escaped from '
                                                                                   'the overfilled '
                                                                                   'tank.',
                                                                                   'The sustained '
                                                                                   'release '
                                                                                   'generated a '
                                                                                   'large '
                                                                                   'flammable '
                                                                                   'gasoline vapor '
                                                                                   'cloud.',
                                                                                   'The vapor '
                                                                                   'cloud spread '
                                                                                   'across the '
                                                                                   'site and '
                                                                                   'beyond the '
                                                                                   'site boundary.',
                                                                                   'The flammable '
                                                                                   'vapor cloud '
                                                                                   'ignited.',
                                                                                   'A series of '
                                                                                   'major '
                                                                                   'explosions '
                                                                                   'occurred.',
                                                                                   'Large fires '
                                                                                   'subsequently '
                                                                                   'engulfed a '
                                                                                   'significant '
                                                                                   'proportion of '
                                                                                   'the storage '
                                                                                   'depot.'],
                                                                'contributing_factors': ['The tank '
                                                                                         'filling '
                                                                                         'operation '
                                                                                         'was not '
                                                                                         'stopped '
                                                                                         'before '
                                                                                         'the tank '
                                                                                         'overfilled.',
                                                                                         'The '
                                                                                         'normal '
                                                                                         'tank '
                                                                                         'level '
                                                                                         'measurement '
                                                                                         'arrangements '
                                                                                         'did not '
                                                                                         'prevent '
                                                                                         'the '
                                                                                         'overfill.',
                                                                                         'The '
                                                                                         'independent '
                                                                                         'high-level '
                                                                                         'overfill '
                                                                                         'protection '
                                                                                         'did not '
                                                                                         'successfully '
                                                                                         'prevent '
                                                                                         'the loss '
                                                                                         'of '
                                                                                         'containment.',
                                                                                         'The '
                                                                                         'overfill '
                                                                                         'continued '
                                                                                         'long '
                                                                                         'enough '
                                                                                         'to '
                                                                                         'generate '
                                                                                         'a very '
                                                                                         'large '
                                                                                         'flammable '
                                                                                         'vapor '
                                                                                         'cloud.',
                                                                                         'The '
                                                                                         'potential '
                                                                                         'consequences '
                                                                                         'of a '
                                                                                         'large '
                                                                                         'vapor '
                                                                                         'cloud '
                                                                                         'explosion '
                                                                                         'at a '
                                                                                         'fuel '
                                                                                         'storage '
                                                                                         'depot '
                                                                                         'had not '
                                                                                         'been '
                                                                                         'adequately '
                                                                                         'controlled.',
                                                                                         'The '
                                                                                         'incident '
                                                                                         'demonstrated '
                                                                                         'weaknesses '
                                                                                         'in the '
                                                                                         'reliability '
                                                                                         'and '
                                                                                         'management '
                                                                                         'of '
                                                                                         'safety-critical '
                                                                                         'overfill '
                                                                                         'protection '
                                                                                         'systems.'],
                                                                'system_causes': ['Management of '
                                                                                  'safety-critical '
                                                                                  'tank level and '
                                                                                  'overfill '
                                                                                  'protection '
                                                                                  'systems was '
                                                                                  'inadequate.',
                                                                                  'Arrangements '
                                                                                  'for inspection, '
                                                                                  'testing and '
                                                                                  'maintenance of '
                                                                                  'overfill '
                                                                                  'protection '
                                                                                  'required '
                                                                                  'improvement.',
                                                                                  'Process safety '
                                                                                  'management did '
                                                                                  'not adequately '
                                                                                  'control the '
                                                                                  'major-accident '
                                                                                  'risk associated '
                                                                                  'with tank '
                                                                                  'overfilling.',
                                                                                  'Major-hazard '
                                                                                  'assessment and '
                                                                                  'emergency '
                                                                                  'planning needed '
                                                                                  'to address '
                                                                                  'severe vapor '
                                                                                  'cloud '
                                                                                  'explosions and '
                                                                                  'multi-tank '
                                                                                  'fires.',
                                                                                  'Containment and '
                                                                                  'emergency-response '
                                                                                  'arrangements '
                                                                                  'required '
                                                                                  'strengthening '
                                                                                  'for credible '
                                                                                  'major '
                                                                                  'fuel-storage '
                                                                                  'incidents.'],
                                                                'consequences': ['There were no '
                                                                                 'fatalities.',
                                                                                 'More than 40 '
                                                                                 'people were '
                                                                                 'injured.',
                                                                                 'A large '
                                                                                 'proportion of '
                                                                                 'the Buncefield '
                                                                                 'storage depot '
                                                                                 'was destroyed or '
                                                                                 'severely '
                                                                                 'damaged.',
                                                                                 'Commercial and '
                                                                                 'residential '
                                                                                 'properties '
                                                                                 'surrounding the '
                                                                                 'depot sustained '
                                                                                 'significant '
                                                                                 'damage.',
                                                                                 'A large '
                                                                                 'surrounding area '
                                                                                 'was evacuated on '
                                                                                 'emergency-service '
                                                                                 'advice.',
                                                                                 'The fire '
                                                                                 'continued for '
                                                                                 'several days.',
                                                                                 'Large quantities '
                                                                                 'of smoke were '
                                                                                 'released to the '
                                                                                 'atmosphere.',
                                                                                 'The incident '
                                                                                 'caused major '
                                                                                 'business '
                                                                                 'interruption and '
                                                                                 'wider economic '
                                                                                 'consequences.'],
                                                                'investigation_findings': ['The '
                                                                                           'Health '
                                                                                           'and '
                                                                                           'Safety '
                                                                                           'Executive '
                                                                                           'and '
                                                                                           'Environment '
                                                                                           'Agency '
                                                                                           'investigated '
                                                                                           'the '
                                                                                           'incident.',
                                                                                           'The '
                                                                                           'Buncefield '
                                                                                           'Major '
                                                                                           'Incident '
                                                                                           'Investigation '
                                                                                           'Board '
                                                                                           'published '
                                                                                           'findings '
                                                                                           'and '
                                                                                           'recommendations '
                                                                                           'arising '
                                                                                           'from '
                                                                                           'the '
                                                                                           'incident.',
                                                                                           'The '
                                                                                           'investigation '
                                                                                           'established '
                                                                                           'tank '
                                                                                           'overfilling '
                                                                                           'as the '
                                                                                           'initiating '
                                                                                           'loss-of-containment '
                                                                                           'event.',
                                                                                           'The '
                                                                                           'investigation '
                                                                                           'highlighted '
                                                                                           'the '
                                                                                           'importance '
                                                                                           'of '
                                                                                           'reliable '
                                                                                           'high-level '
                                                                                           'overfill '
                                                                                           'protection.',
                                                                                           'Post-incident '
                                                                                           'work '
                                                                                           'established '
                                                                                           'stronger '
                                                                                           'expectations '
                                                                                           'for '
                                                                                           'overfill '
                                                                                           'prevention '
                                                                                           'and '
                                                                                           'automatic '
                                                                                           'shutdown '
                                                                                           'systems.',
                                                                                           'Recommendations '
                                                                                           'addressed '
                                                                                           'secondary '
                                                                                           'and '
                                                                                           'tertiary '
                                                                                           'containment.',
                                                                                           'Recommendations '
                                                                                           'also '
                                                                                           'addressed '
                                                                                           'process '
                                                                                           'safety '
                                                                                           'leadership, '
                                                                                           'emergency '
                                                                                           'planning '
                                                                                           'and '
                                                                                           'major-hazard '
                                                                                           'management.'],
                                                                'lessons': ['Bulk fuel storage '
                                                                            'tanks require '
                                                                            'reliable independent '
                                                                            'protection against '
                                                                            'overfilling.',
                                                                            'Safety-critical level '
                                                                            'alarms, trips and '
                                                                            'shutdown systems '
                                                                            'require appropriate '
                                                                            'design, installation, '
                                                                            'testing and '
                                                                            'maintenance.',
                                                                            'Independent overfill '
                                                                            'protection should not '
                                                                            'depend on the same '
                                                                            'failure mechanisms as '
                                                                            'normal level '
                                                                            'measurement and '
                                                                            'control.',
                                                                            'Tank transfer '
                                                                            'operations require '
                                                                            'clear operating '
                                                                            'limits and effective '
                                                                            'response to abnormal '
                                                                            'level conditions.',
                                                                            'Major-hazard '
                                                                            'assessments for '
                                                                            'volatile fuels must '
                                                                            'consider the '
                                                                            'possibility of large '
                                                                            'flammable vapor-cloud '
                                                                            'formation following '
                                                                            'sustained loss of '
                                                                            'containment.',
                                                                            'Secondary and '
                                                                            'tertiary containment '
                                                                            'must be capable of '
                                                                            'limiting the '
                                                                            'environmental '
                                                                            'consequences of major '
                                                                            'releases and '
                                                                            'firefighting '
                                                                            'operations.',
                                                                            'Emergency plans for '
                                                                            'large fuel-storage '
                                                                            'facilities should '
                                                                            'consider severe vapor '
                                                                            'cloud explosions and '
                                                                            'multi-tank fires.',
                                                                            'Process safety '
                                                                            'leadership must '
                                                                            'ensure that '
                                                                            'safety-critical '
                                                                            'protective systems '
                                                                            'remain effective '
                                                                            'throughout their '
                                                                            'operating life.']},
 'Deepwater Horizon / Macondo Blowout (Gulf of Mexico, 2010)': {'schema_version': 2,
                                                                'metadata': {'date': '20 April '
                                                                                     '2010',
                                                                             'location': 'Macondo '
                                                                                         'well, '
                                                                                         'Gulf of '
                                                                                         'Mexico',
                                                                             'type': 'Offshore '
                                                                                     'well '
                                                                                     'blowout, '
                                                                                     'explosions, '
                                                                                     'fire and oil '
                                                                                     'spill',
                                                                             'fatalities': 11,
                                                                             'injuries': '17 '
                                                                                         'workers '
                                                                                         'were '
                                                                                         'seriously '
                                                                                         'injured',
                                                                             'investigation_agency': 'U.S. '
                                                                                                     'Chemical '
                                                                                                     'Safety '
                                                                                                     'Board '
                                                                                                     '(CSB), '
                                                                                                     'with '
                                                                                                     'separate '
                                                                                                     'investigations '
                                                                                                     'also '
                                                                                                     'conducted '
                                                                                                     'by '
                                                                                                     'other '
                                                                                                     'U.S. '
                                                                                                     'authorities',
                                                                             'report_title': 'Macondo '
                                                                                             'Investigation '
                                                                                             'Report',
                                                                             'report_number': None,
                                                                             'report_date': 'CSB '
                                                                                            'investigation '
                                                                                            'volumes '
                                                                                            'issued '
                                                                                            'in '
                                                                                            'multiple '
                                                                                            'stages'},
                                                                'event_sequence': ['The Deepwater '
                                                                                   'Horizon was '
                                                                                   'conducting '
                                                                                   'temporary '
                                                                                   'abandonment '
                                                                                   'operations at '
                                                                                   'the Macondo '
                                                                                   'well.',
                                                                                   'The cement '
                                                                                   'barrier '
                                                                                   'intended to '
                                                                                   'isolate '
                                                                                   'hydrocarbons '
                                                                                   'from the '
                                                                                   'wellbore did '
                                                                                   'not provide an '
                                                                                   'effective '
                                                                                   'seal.',
                                                                                   'A negative '
                                                                                   'pressure test '
                                                                                   'was '
                                                                                   'interpreted as '
                                                                                   'indicating '
                                                                                   'that the well '
                                                                                   'was adequately '
                                                                                   'sealed.',
                                                                                   'Hydrocarbons '
                                                                                   'subsequently '
                                                                                   'flowed into '
                                                                                   'the well.',
                                                                                   'The developing '
                                                                                   'well-control '
                                                                                   'event was not '
                                                                                   'detected and '
                                                                                   'controlled '
                                                                                   'before '
                                                                                   'hydrocarbons '
                                                                                   'had traveled '
                                                                                   'high in the '
                                                                                   'well toward '
                                                                                   'the rig.',
                                                                                   'Oil and gas '
                                                                                   'reached the '
                                                                                   'Deepwater '
                                                                                   'Horizon '
                                                                                   'drilling rig.',
                                                                                   'The '
                                                                                   'hydrocarbon '
                                                                                   'release '
                                                                                   'resulted in '
                                                                                   'explosions and '
                                                                                   'a major fire.',
                                                                                   'The blowout '
                                                                                   'preventer did '
                                                                                   'not ultimately '
                                                                                   'seal the well.',
                                                                                   'The Deepwater '
                                                                                   'Horizon rig '
                                                                                   'sank two days '
                                                                                   'after the '
                                                                                   'accident.',
                                                                                   'Oil and gas '
                                                                                   'continued '
                                                                                   'flowing from '
                                                                                   'the Macondo '
                                                                                   'well into the '
                                                                                   'Gulf of Mexico '
                                                                                   'for 87 days.'],
                                                                'contributing_factors': ['The '
                                                                                         'cement '
                                                                                         'barrier '
                                                                                         'did not '
                                                                                         'successfully '
                                                                                         'isolate '
                                                                                         'the '
                                                                                         'hydrocarbon-bearing '
                                                                                         'formation.',
                                                                                         'The '
                                                                                         'negative '
                                                                                         'pressure '
                                                                                         'test did '
                                                                                         'not '
                                                                                         'identify '
                                                                                         'that the '
                                                                                         'well was '
                                                                                         'not '
                                                                                         'effectively '
                                                                                         'sealed.',
                                                                                         'There '
                                                                                         'were no '
                                                                                         'written '
                                                                                         'procedures '
                                                                                         'defining '
                                                                                         'how to '
                                                                                         'conduct '
                                                                                         'the '
                                                                                         'negative '
                                                                                         'pressure '
                                                                                         'test and '
                                                                                         'no '
                                                                                         'written '
                                                                                         'criteria '
                                                                                         'or safe '
                                                                                         'limits '
                                                                                         'for '
                                                                                         'determining '
                                                                                         'whether '
                                                                                         'the test '
                                                                                         'was '
                                                                                         'successful.',
                                                                                         'The '
                                                                                         'developing '
                                                                                         'influx '
                                                                                         'was not '
                                                                                         'detected '
                                                                                         'and '
                                                                                         'controlled '
                                                                                         'sufficiently '
                                                                                         'early.',
                                                                                         'Major-accident '
                                                                                         'hazard '
                                                                                         'controls '
                                                                                         'relied '
                                                                                         'significantly '
                                                                                         'on '
                                                                                         'correct '
                                                                                         'and '
                                                                                         'timely '
                                                                                         'manual '
                                                                                         'intervention.',
                                                                                         'The '
                                                                                         'blowout '
                                                                                         'preventer '
                                                                                         'experienced '
                                                                                         'failures '
                                                                                         'that '
                                                                                         'prevented '
                                                                                         'it from '
                                                                                         'reliably '
                                                                                         'sealing '
                                                                                         'the well '
                                                                                         'during '
                                                                                         'the '
                                                                                         'emergency.'],
                                                                'system_causes': ['Management '
                                                                                  'systems did not '
                                                                                  'adequately '
                                                                                  'control the '
                                                                                  'major-accident '
                                                                                  'risks '
                                                                                  'associated with '
                                                                                  'temporary '
                                                                                  'abandonment and '
                                                                                  'loss of well '
                                                                                  'control.',
                                                                                  'Safety '
                                                                                  'management did '
                                                                                  'not provide '
                                                                                  'sufficiently '
                                                                                  'robust control '
                                                                                  'of '
                                                                                  'safety-critical '
                                                                                  'barriers.',
                                                                                  'Management of '
                                                                                  'change and '
                                                                                  'hazard '
                                                                                  'assessment '
                                                                                  'arrangements '
                                                                                  'did not '
                                                                                  'adequately '
                                                                                  'address changes '
                                                                                  'associated with '
                                                                                  'the temporary '
                                                                                  'abandonment '
                                                                                  'plan.',
                                                                                  'Process safety '
                                                                                  'performance '
                                                                                  'management did '
                                                                                  'not '
                                                                                  'sufficiently '
                                                                                  'emphasize '
                                                                                  'major-accident '
                                                                                  'prevention.',
                                                                                  'Safety-critical '
                                                                                  'BOP systems '
                                                                                  'were not '
                                                                                  'managed with '
                                                                                  'sufficient '
                                                                                  'assurance of '
                                                                                  'emergency '
                                                                                  'reliability.'],
                                                                'consequences': ['Eleven workers '
                                                                                 'were killed.',
                                                                                 'Seventeen '
                                                                                 'workers were '
                                                                                 'seriously '
                                                                                 'injured.',
                                                                                 'The Deepwater '
                                                                                 'Horizon drilling '
                                                                                 'rig was '
                                                                                 'destroyed and '
                                                                                 'sank two days '
                                                                                 'after the '
                                                                                 'accident.',
                                                                                 'Oil and gas '
                                                                                 'flowed '
                                                                                 'uncontrolled '
                                                                                 'from the Macondo '
                                                                                 'well into the '
                                                                                 'Gulf of Mexico '
                                                                                 'for 87 days.',
                                                                                 'The incident '
                                                                                 'resulted in a '
                                                                                 'major offshore '
                                                                                 'environmental '
                                                                                 'disaster.'],
                                                                'investigation_findings': ['The '
                                                                                           'U.S. '
                                                                                           'Chemical '
                                                                                           'Safety '
                                                                                           'Board '
                                                                                           'conducted '
                                                                                           'a '
                                                                                           'major '
                                                                                           'process-safety '
                                                                                           'investigation '
                                                                                           'of the '
                                                                                           'Macondo '
                                                                                           'blowout '
                                                                                           'and '
                                                                                           'explosion.',
                                                                                           'The '
                                                                                           'CSB '
                                                                                           'investigation '
                                                                                           'examined '
                                                                                           'failures '
                                                                                           'of '
                                                                                           'physical, '
                                                                                           'operational '
                                                                                           'and '
                                                                                           'organizational '
                                                                                           'safety '
                                                                                           'barriers.',
                                                                                           'The '
                                                                                           'CSB '
                                                                                           'examined '
                                                                                           'the '
                                                                                           'failure '
                                                                                           'of the '
                                                                                           'blowout '
                                                                                           'preventer '
                                                                                           'as a '
                                                                                           'safety-critical '
                                                                                           'barrier.',
                                                                                           'The '
                                                                                           'CSB '
                                                                                           'identified '
                                                                                           'deficiencies '
                                                                                           'in '
                                                                                           'management '
                                                                                           'of '
                                                                                           'safety-critical '
                                                                                           'equipment '
                                                                                           'and '
                                                                                           'major-accident '
                                                                                           'risk.',
                                                                                           'The '
                                                                                           'CSB '
                                                                                           'examined '
                                                                                           'weaknesses '
                                                                                           'in '
                                                                                           'process '
                                                                                           'safety '
                                                                                           'performance '
                                                                                           'indicators '
                                                                                           'and '
                                                                                           'hazard '
                                                                                           'assessment.',
                                                                                           'The '
                                                                                           'CSB '
                                                                                           'investigation '
                                                                                           'was '
                                                                                           'published '
                                                                                           'through '
                                                                                           'multiple '
                                                                                           'report '
                                                                                           'volumes '
                                                                                           'addressing '
                                                                                           'technical, '
                                                                                           'regulatory '
                                                                                           'and '
                                                                                           'organizational '
                                                                                           'issues.'],
                                                                'lessons': ['Well integrity '
                                                                            'requires multiple '
                                                                            'effective and '
                                                                            'independently '
                                                                            'verified barriers '
                                                                            'against uncontrolled '
                                                                            'hydrocarbon flow.',
                                                                            'Negative pressure '
                                                                            'tests require clear '
                                                                            'procedures, '
                                                                            'acceptance criteria '
                                                                            'and competent '
                                                                            'interpretation.',
                                                                            'Early detection and '
                                                                            'response to well '
                                                                            'influx are critical '
                                                                            'to preventing '
                                                                            'escalation to a '
                                                                            'blowout.',
                                                                            'Safety-critical '
                                                                            'blowout prevention '
                                                                            'equipment must be '
                                                                            'capable of performing '
                                                                            'its required '
                                                                            'emergency functions '
                                                                            'under credible '
                                                                            'accident conditions.',
                                                                            'Testing and '
                                                                            'maintenance programs '
                                                                            'must identify latent '
                                                                            'failures in emergency '
                                                                            'safety systems.',
                                                                            'Major-accident hazard '
                                                                            'assessments should '
                                                                            'not rely excessively '
                                                                            'on timely human '
                                                                            'intervention as the '
                                                                            'principal protective '
                                                                            'layer.',
                                                                            'Management of change '
                                                                            'must evaluate safety '
                                                                            'implications of '
                                                                            'changes to well plans '
                                                                            'and temporary '
                                                                            'abandonment '
                                                                            'activities.',
                                                                            'Process safety '
                                                                            'indicators should '
                                                                            'measure the health of '
                                                                            'major-accident '
                                                                            'prevention barriers, '
                                                                            'not only personal '
                                                                            'safety performance.']},
 'Montara Wellhead Platform Blowout (Timor Sea, 2009)': {'schema_version': 2,
                                                         'metadata': {'date': '21 August 2009',
                                                                      'location': 'Montara oil '
                                                                                  'field, Timor '
                                                                                  'Sea, Australia',
                                                                      'type': 'Offshore well '
                                                                              'blowout and '
                                                                              'uncontrolled oil '
                                                                              'and gas release',
                                                                      'fatalities': 0,
                                                                      'injuries': 'Not included in '
                                                                                  'current '
                                                                                  'verified '
                                                                                  'dataset',
                                                                      'investigation_agency': 'Australian '
                                                                                              'Government '
                                                                                              'Montara '
                                                                                              'Commission '
                                                                                              'of '
                                                                                              'Inquiry',
                                                                      'report_title': 'Report of '
                                                                                      'the Montara '
                                                                                      'Commission '
                                                                                      'of Inquiry',
                                                                      'report_number': None,
                                                                      'report_date': 'June 2010'},
                                                         'event_sequence': ['Problems occurred '
                                                                            'during cementing of '
                                                                            'the 9 5/8-inch casing '
                                                                            'shoe in the H1 well.',
                                                                            'The cemented casing '
                                                                            'shoe was likely '
                                                                            'compromised and did '
                                                                            'not provide a '
                                                                            'reliable primary '
                                                                            'well-control barrier.',
                                                                            'The 9 5/8-inch '
                                                                            'cemented casing shoe '
                                                                            'was not adequately '
                                                                            'pressure-tested to '
                                                                            'verify its integrity.',
                                                                            'Secondary '
                                                                            'well-control barriers '
                                                                            'were also inadequate, '
                                                                            'missing or not '
                                                                            'properly verified.',
                                                                            'The 9 5/8-inch '
                                                                            'pressure-containing '
                                                                            'anti-corrosion cap '
                                                                            'was removed and was '
                                                                            'not reinstalled '
                                                                            'before subsequent '
                                                                            'operations.',
                                                                            'The H1 well was '
                                                                            'therefore left '
                                                                            'relying on an '
                                                                            'unverified primary '
                                                                            'well-control barrier.',
                                                                            'Hydrocarbons entered '
                                                                            'the H1 well through '
                                                                            'the failed 9 5/8-inch '
                                                                            'cemented casing shoe.',
                                                                            'Hydrocarbons flowed '
                                                                            'up the well and an '
                                                                            'uncontrolled blowout '
                                                                            'developed.',
                                                                            'Oil and gas were '
                                                                            'released from the '
                                                                            'Montara well into the '
                                                                            'Timor Sea.',
                                                                            'The uncontrolled flow '
                                                                            'was stopped on 3 '
                                                                            'November 2009 after '
                                                                            'intervention through '
                                                                            'a relief well.'],
                                                         'contributing_factors': ['Significant '
                                                                                  'problems '
                                                                                  'occurred during '
                                                                                  'the original '
                                                                                  'cementing '
                                                                                  'operation.',
                                                                                  'The cement in '
                                                                                  'the casing shoe '
                                                                                  'was likely '
                                                                                  'compromised by '
                                                                                  'substantial '
                                                                                  'over-displacement '
                                                                                  'of fluid, '
                                                                                  'resulting in a '
                                                                                  'wet shoe.',
                                                                                  'The '
                                                                                  'significance of '
                                                                                  'the cementing '
                                                                                  'problems was '
                                                                                  'not adequately '
                                                                                  'recognized and '
                                                                                  'evaluated.',
                                                                                  'The primary '
                                                                                  'cemented '
                                                                                  'casing-shoe '
                                                                                  'barrier was not '
                                                                                  'properly '
                                                                                  'pressure-tested '
                                                                                  'after the '
                                                                                  'cementing '
                                                                                  'problems.',
                                                                                  'Only one of the '
                                                                                  'two planned '
                                                                                  'pressure-containing '
                                                                                  'anti-corrosion '
                                                                                  'caps was '
                                                                                  'installed.',
                                                                                  'The installed '
                                                                                  'pressure-containing '
                                                                                  'anti-corrosion '
                                                                                  'cap was not '
                                                                                  'adequately '
                                                                                  'tested and '
                                                                                  'verified in '
                                                                                  'situ.',
                                                                                  'The installed 9 '
                                                                                  '5/8-inch '
                                                                                  'pressure-containing '
                                                                                  'anti-corrosion '
                                                                                  'cap was later '
                                                                                  'removed without '
                                                                                  'establishing a '
                                                                                  'verified '
                                                                                  'replacement '
                                                                                  'barrier.'],
                                                         'system_causes': ["PTTEP Australasia's "
                                                                           'well-control practices '
                                                                           'and procedures were '
                                                                           'deficient.',
                                                                           'Management systems did '
                                                                           'not ensure that '
                                                                           'safety-critical well '
                                                                           'barriers were properly '
                                                                           'installed, verified '
                                                                           'and maintained.',
                                                                           'Information indicating '
                                                                           'serious cementing '
                                                                           'problems was not '
                                                                           'adequately recognized '
                                                                           'or acted upon by '
                                                                           'responsible personnel.',
                                                                           'Well construction '
                                                                           'activities did not '
                                                                           'consistently comply '
                                                                           "with the company's own "
                                                                           'Well Construction '
                                                                           'Standards.',
                                                                           "The company's "
                                                                           'procedural and '
                                                                           'operational '
                                                                           'shortcomings were '
                                                                           'widespread and '
                                                                           'systemic.',
                                                                           'Regulatory oversight '
                                                                           'of the Montara well '
                                                                           'activities was not '
                                                                           'sufficiently '
                                                                           'diligent.'],
                                                         'consequences': ['There were no '
                                                                          'fatalities during the '
                                                                          'initial blowout and '
                                                                          'evacuation.',
                                                                          'All 69 personnel on the '
                                                                          'West Atlas drilling rig '
                                                                          'and Montara wellhead '
                                                                          'platform were safely '
                                                                          'evacuated.',
                                                                          'Oil and gas were '
                                                                          'released uncontrollably '
                                                                          'into the Timor Sea.',
                                                                          'The uncontrolled '
                                                                          'release continued from '
                                                                          '21 August until 3 '
                                                                          'November 2009.',
                                                                          'The incident required a '
                                                                          'major offshore '
                                                                          'oil-spill response.',
                                                                          'The remote location and '
                                                                          'limitations in baseline '
                                                                          'and monitoring '
                                                                          'information made the '
                                                                          'full environmental '
                                                                          'consequences difficult '
                                                                          'to determine.'],
                                                         'investigation_findings': ['The '
                                                                                    'Australian '
                                                                                    'Government '
                                                                                    'established '
                                                                                    'the Montara '
                                                                                    'Commission of '
                                                                                    'Inquiry to '
                                                                                    'investigate '
                                                                                    'the incident.',
                                                                                    'The Inquiry '
                                                                                    'found that '
                                                                                    'hydrocarbons '
                                                                                    'most likely '
                                                                                    'entered the '
                                                                                    'H1 well '
                                                                                    'through the 9 '
                                                                                    '5/8-inch '
                                                                                    'cemented '
                                                                                    'casing shoe.',
                                                                                    'The Inquiry '
                                                                                    'found that '
                                                                                    'the 9 '
                                                                                    '5/8-inch '
                                                                                    'cemented '
                                                                                    'casing shoe, '
                                                                                    'the primary '
                                                                                    'well-control '
                                                                                    'barrier, '
                                                                                    'failed.',
                                                                                    'The Inquiry '
                                                                                    'found that '
                                                                                    'the primary '
                                                                                    'barrier had '
                                                                                    'not been '
                                                                                    'adequately '
                                                                                    'pressure-tested '
                                                                                    'despite '
                                                                                    'significant '
                                                                                    'problems '
                                                                                    'during '
                                                                                    'cementing.',
                                                                                    'The Inquiry '
                                                                                    'identified '
                                                                                    'deficiencies '
                                                                                    'in the '
                                                                                    'installation '
                                                                                    'and '
                                                                                    'verification '
                                                                                    'of secondary '
                                                                                    'well-control '
                                                                                    'barriers.',
                                                                                    'The Inquiry '
                                                                                    'found '
                                                                                    'widespread '
                                                                                    'and systemic '
                                                                                    'shortcomings '
                                                                                    'in PTTEP '
                                                                                    "Australasia's "
                                                                                    'procedures '
                                                                                    'and '
                                                                                    'practices.',
                                                                                    'The Inquiry '
                                                                                    'also '
                                                                                    'identified '
                                                                                    'deficiencies '
                                                                                    'in regulatory '
                                                                                    'oversight.',
                                                                                    'The Montara '
                                                                                    'Commission of '
                                                                                    'Inquiry made '
                                                                                    '105 '
                                                                                    'recommendations.'],
                                                         'lessons': ['Every safety-critical well '
                                                                     'barrier must be positively '
                                                                     'verified before it is relied '
                                                                     'upon for well control.',
                                                                     'Abnormal cementing results '
                                                                     'must trigger formal '
                                                                     'evaluation, pressure testing '
                                                                     'and appropriate remedial '
                                                                     'action.',
                                                                     'A well should not be left '
                                                                     'dependent on an unverified '
                                                                     'primary barrier.',
                                                                     'Secondary well-control '
                                                                     'barriers must be suitable '
                                                                     'for their intended safety '
                                                                     'function and independently '
                                                                     'verified.',
                                                                     'Removal of a verified well '
                                                                     'barrier requires '
                                                                     'confirmation that adequate '
                                                                     'alternative barriers are '
                                                                     'established.',
                                                                     'Well-construction records '
                                                                     'and abnormal operating '
                                                                     'information must be reviewed '
                                                                     'by competent personnel who '
                                                                     'understand their '
                                                                     'process-safety significance.',
                                                                     'Well-control procedures must '
                                                                     'comply with approved '
                                                                     'well-construction standards '
                                                                     'and established good '
                                                                     'oilfield practice.',
                                                                     'Major-accident prevention '
                                                                     'requires effective '
                                                                     'organizational assurance as '
                                                                     'well as competent field '
                                                                     'execution.',
                                                                     'Regulatory oversight must '
                                                                     'provide effective assurance '
                                                                     'that operators are '
                                                                     'controlling major '
                                                                     'well-integrity hazards.']},
 'Alexander L. Kielland Offshore Platform Disaster (North Sea, 1980)': {'schema_version': 2,
                                                                        'metadata': {'date': '27 '
                                                                                             'March '
                                                                                             '1980',
                                                                                     'location': 'Ekofisk '
                                                                                                 'area, '
                                                                                                 'Norwegian '
                                                                                                 'North '
                                                                                                 'Sea',
                                                                                     'type': 'Offshore '
                                                                                             'structural '
                                                                                             'failure, '
                                                                                             'loss '
                                                                                             'of '
                                                                                             'stability '
                                                                                             'and '
                                                                                             'capsize',
                                                                                     'fatalities': 123,
                                                                                     'injuries': 'Not '
                                                                                                 'included '
                                                                                                 'in '
                                                                                                 'current '
                                                                                                 'verified '
                                                                                                 'dataset',
                                                                                     'investigation_agency': 'Norwegian '
                                                                                                             'Government '
                                                                                                             'Commission '
                                                                                                             'of '
                                                                                                             'Inquiry',
                                                                                     'report_title': 'Alexander '
                                                                                                     'L. '
                                                                                                     'Kielland-ulykken',
                                                                                     'report_number': 'NOU '
                                                                                                      '1981:11',
                                                                                     'report_date': '1981'},
                                                                        'event_sequence': ['Alexander '
                                                                                           'L. '
                                                                                           'Kielland '
                                                                                           'was '
                                                                                           'operating '
                                                                                           'as an '
                                                                                           'accommodation '
                                                                                           'platform '
                                                                                           'in the '
                                                                                           'Ekofisk '
                                                                                           'area '
                                                                                           'of the '
                                                                                           'Norwegian '
                                                                                           'North '
                                                                                           'Sea.',
                                                                                           'A '
                                                                                           'fatigue '
                                                                                           'crack '
                                                                                           'had '
                                                                                           'developed '
                                                                                           'in '
                                                                                           'structural '
                                                                                           'brace '
                                                                                           'D-6 at '
                                                                                           'the '
                                                                                           'attachment '
                                                                                           'for a '
                                                                                           'hydrophone '
                                                                                           'support.',
                                                                                           'The '
                                                                                           'fatigue '
                                                                                           'crack '
                                                                                           'propagated '
                                                                                           'until '
                                                                                           'brace '
                                                                                           'D-6 '
                                                                                           'fractured.',
                                                                                           'Following '
                                                                                           'failure '
                                                                                           'of '
                                                                                           'D-6, '
                                                                                           'five '
                                                                                           'other '
                                                                                           'braces '
                                                                                           'connecting '
                                                                                           'column '
                                                                                           'D to '
                                                                                           'the '
                                                                                           'platform '
                                                                                           'failed '
                                                                                           'due to '
                                                                                           'overload.',
                                                                                           'Column '
                                                                                           'D was '
                                                                                           'lost '
                                                                                           'from '
                                                                                           'the '
                                                                                           'platform '
                                                                                           'structure.',
                                                                                           'Loss '
                                                                                           'of '
                                                                                           'column '
                                                                                           'D and '
                                                                                           'its '
                                                                                           'buoyancy '
                                                                                           'caused '
                                                                                           'the '
                                                                                           'platform '
                                                                                           'to '
                                                                                           'develop '
                                                                                           'a '
                                                                                           'severe '
                                                                                           'list '
                                                                                           'of '
                                                                                           'approximately '
                                                                                           '30 to '
                                                                                           '35 '
                                                                                           'degrees.',
                                                                                           'Water '
                                                                                           'entered '
                                                                                           'other '
                                                                                           'columns '
                                                                                           'and '
                                                                                           'deck '
                                                                                           'volumes '
                                                                                           'through '
                                                                                           'openings '
                                                                                           'as the '
                                                                                           'platform '
                                                                                           'remained '
                                                                                           'heavily '
                                                                                           'listed.',
                                                                                           'Progressive '
                                                                                           'flooding '
                                                                                           'further '
                                                                                           'reduced '
                                                                                           'the '
                                                                                           "platform's "
                                                                                           'stability '
                                                                                           'and '
                                                                                           'buoyancy.',
                                                                                           'Alexander '
                                                                                           'L. '
                                                                                           'Kielland '
                                                                                           'capsized '
                                                                                           'approximately '
                                                                                           '20 '
                                                                                           'minutes '
                                                                                           'after '
                                                                                           'the '
                                                                                           'initial '
                                                                                           'structural '
                                                                                           'failure.'],
                                                                        'contributing_factors': ['The '
                                                                                                 'fatigue '
                                                                                                 'crack '
                                                                                                 'initiated '
                                                                                                 'in '
                                                                                                 'the '
                                                                                                 'area '
                                                                                                 'where '
                                                                                                 'a '
                                                                                                 'hydrophone '
                                                                                                 'support '
                                                                                                 'had '
                                                                                                 'been '
                                                                                                 'attached '
                                                                                                 'to '
                                                                                                 'brace '
                                                                                                 'D-6.',
                                                                                                 'The '
                                                                                                 'hydrophone-support '
                                                                                                 'attachment '
                                                                                                 'incorporated '
                                                                                                 'a '
                                                                                                 'low-quality '
                                                                                                 'fillet '
                                                                                                 'weld.',
                                                                                                 'The '
                                                                                                 'hydrophone-support '
                                                                                                 'detail '
                                                                                                 'created '
                                                                                                 'a '
                                                                                                 'significant '
                                                                                                 'stress '
                                                                                                 'concentration '
                                                                                                 'in '
                                                                                                 'the '
                                                                                                 'load-carrying '
                                                                                                 'brace.',
                                                                                                 'The '
                                                                                                 'fatigue '
                                                                                                 'crack '
                                                                                                 'propagated '
                                                                                                 'in '
                                                                                                 'the '
                                                                                                 'D-6 '
                                                                                                 'brace '
                                                                                                 'until '
                                                                                                 'structural '
                                                                                                 'fracture '
                                                                                                 'occurred.',
                                                                                                 'The '
                                                                                                 'remaining '
                                                                                                 'braces '
                                                                                                 'connected '
                                                                                                 'to '
                                                                                                 'column '
                                                                                                 'D '
                                                                                                 'were '
                                                                                                 'unable '
                                                                                                 'to '
                                                                                                 'withstand '
                                                                                                 'the '
                                                                                                 'redistributed '
                                                                                                 'loads '
                                                                                                 'after '
                                                                                                 'D-6 '
                                                                                                 'failed.',
                                                                                                 'Loss '
                                                                                                 'of '
                                                                                                 'column '
                                                                                                 'D '
                                                                                                 'caused '
                                                                                                 'a '
                                                                                                 'major '
                                                                                                 'loss '
                                                                                                 'of '
                                                                                                 'buoyancy '
                                                                                                 'and '
                                                                                                 'a '
                                                                                                 'severe '
                                                                                                 'platform '
                                                                                                 'list.',
                                                                                                 'Openings '
                                                                                                 'in '
                                                                                                 'the '
                                                                                                 'structure '
                                                                                                 'permitted '
                                                                                                 'progressive '
                                                                                                 'flooding '
                                                                                                 'after '
                                                                                                 'the '
                                                                                                 'platform '
                                                                                                 'developed '
                                                                                                 'the '
                                                                                                 'severe '
                                                                                                 'list.',
                                                                                                 'Severe '
                                                                                                 'weather, '
                                                                                                 'cold '
                                                                                                 'water '
                                                                                                 'and '
                                                                                                 'the '
                                                                                                 'rapid '
                                                                                                 'development '
                                                                                                 'of '
                                                                                                 'the '
                                                                                                 'accident '
                                                                                                 'complicated '
                                                                                                 'evacuation '
                                                                                                 'and '
                                                                                                 'rescue.'],
                                                                        'system_causes': ['Deficiencies '
                                                                                          'associated '
                                                                                          'with '
                                                                                          'the '
                                                                                          'design '
                                                                                          'and '
                                                                                          'fabrication '
                                                                                          'of the '
                                                                                          'hydrophone-support '
                                                                                          'attachment '
                                                                                          'contributed '
                                                                                          'to '
                                                                                          'fatigue-crack '
                                                                                          'initiation.',
                                                                                          'The '
                                                                                          'structural '
                                                                                          'arrangement '
                                                                                          'lacked '
                                                                                          'sufficient '
                                                                                          'redundancy '
                                                                                          'to '
                                                                                          'prevent '
                                                                                          'a local '
                                                                                          'brace '
                                                                                          'failure '
                                                                                          'from '
                                                                                          'escalating '
                                                                                          'into '
                                                                                          'loss of '
                                                                                          'an '
                                                                                          'entire '
                                                                                          'column.',
                                                                                          'Structural '
                                                                                          'integrity '
                                                                                          'arrangements '
                                                                                          'did not '
                                                                                          'prevent '
                                                                                          'the '
                                                                                          'fatigue '
                                                                                          'crack '
                                                                                          'from '
                                                                                          'developing '
                                                                                          'into a '
                                                                                          'catastrophic '
                                                                                          'structural '
                                                                                          'failure.',
                                                                                          'The '
                                                                                          'accident '
                                                                                          'demonstrated '
                                                                                          'the '
                                                                                          'need '
                                                                                          'for '
                                                                                          'stronger '
                                                                                          'control '
                                                                                          'of '
                                                                                          'fatigue-critical '
                                                                                          'structural '
                                                                                          'details, '
                                                                                          'welding '
                                                                                          'quality '
                                                                                          'and '
                                                                                          'inspection.',
                                                                                          'Emergency '
                                                                                          'preparedness '
                                                                                          'and '
                                                                                          'lifesaving '
                                                                                          'arrangements '
                                                                                          'were '
                                                                                          'inadequate '
                                                                                          'for a '
                                                                                          'rapidly '
                                                                                          'developing '
                                                                                          'capsize '
                                                                                          'scenario.',
                                                                                          'The '
                                                                                          'accident '
                                                                                          'exposed '
                                                                                          'weaknesses '
                                                                                          'in the '
                                                                                          'offshore '
                                                                                          'safety '
                                                                                          'and '
                                                                                          'regulatory '
                                                                                          'framework '
                                                                                          'that '
                                                                                          'subsequently '
                                                                                          'required '
                                                                                          'significant '
                                                                                          'improvement.'],
                                                                        'consequences': ['There '
                                                                                         'were 212 '
                                                                                         'people '
                                                                                         'aboard '
                                                                                         'Alexander '
                                                                                         'L. '
                                                                                         'Kielland '
                                                                                         'when the '
                                                                                         'accident '
                                                                                         'occurred.',
                                                                                         'One '
                                                                                         'hundred '
                                                                                         'and '
                                                                                         'twenty-three '
                                                                                         'people '
                                                                                         'died.',
                                                                                         'Eighty-nine '
                                                                                         'people '
                                                                                         'survived.',
                                                                                         'The '
                                                                                         'platform '
                                                                                         'capsized '
                                                                                         'approximately '
                                                                                         '20 '
                                                                                         'minutes '
                                                                                         'after '
                                                                                         'the '
                                                                                         'initial '
                                                                                         'structural '
                                                                                         'failure.',
                                                                                         'Cold '
                                                                                         'water, '
                                                                                         'severe '
                                                                                         'weather '
                                                                                         'and the '
                                                                                         'rapid '
                                                                                         'capsize '
                                                                                         'greatly '
                                                                                         'complicated '
                                                                                         'evacuation '
                                                                                         'and '
                                                                                         'rescue.',
                                                                                         'The '
                                                                                         'accident '
                                                                                         'became a '
                                                                                         'major '
                                                                                         'turning '
                                                                                         'point in '
                                                                                         'Norwegian '
                                                                                         'offshore '
                                                                                         'safety.'],
                                                                        'investigation_findings': ['The '
                                                                                                   'Norwegian '
                                                                                                   'Government '
                                                                                                   'established '
                                                                                                   'a '
                                                                                                   'Commission '
                                                                                                   'of '
                                                                                                   'Inquiry '
                                                                                                   'following '
                                                                                                   'the '
                                                                                                   'accident.',
                                                                                                   'The '
                                                                                                   'Commission '
                                                                                                   'concluded '
                                                                                                   'that '
                                                                                                   'the '
                                                                                                   'triggering '
                                                                                                   'cause '
                                                                                                   'of '
                                                                                                   'the '
                                                                                                   'accident '
                                                                                                   'was '
                                                                                                   'fatigue '
                                                                                                   'fracture '
                                                                                                   'of '
                                                                                                   'structural '
                                                                                                   'brace '
                                                                                                   'D-6.',
                                                                                                   'The '
                                                                                                   'fatigue '
                                                                                                   'crack '
                                                                                                   'developed '
                                                                                                   'where '
                                                                                                   'a '
                                                                                                   'hydrophone '
                                                                                                   'support '
                                                                                                   'had '
                                                                                                   'been '
                                                                                                   'welded '
                                                                                                   'to '
                                                                                                   'brace '
                                                                                                   'D-6.',
                                                                                                   'The '
                                                                                                   'Commission '
                                                                                                   'linked '
                                                                                                   'development '
                                                                                                   'of '
                                                                                                   'the '
                                                                                                   'fatigue '
                                                                                                   'crack '
                                                                                                   'to '
                                                                                                   'deficiencies '
                                                                                                   'associated '
                                                                                                   'with '
                                                                                                   'planning '
                                                                                                   'and '
                                                                                                   'construction '
                                                                                                   'of '
                                                                                                   'the '
                                                                                                   'platform.',
                                                                                                   'Failure '
                                                                                                   'of '
                                                                                                   'D-6 '
                                                                                                   'caused '
                                                                                                   'overload '
                                                                                                   'failure '
                                                                                                   'of '
                                                                                                   'the '
                                                                                                   'remaining '
                                                                                                   'braces '
                                                                                                   'connecting '
                                                                                                   'column '
                                                                                                   'D '
                                                                                                   'to '
                                                                                                   'the '
                                                                                                   'platform.',
                                                                                                   'Loss '
                                                                                                   'of '
                                                                                                   'column '
                                                                                                   'D '
                                                                                                   'caused '
                                                                                                   'loss '
                                                                                                   'of '
                                                                                                   'buoyancy '
                                                                                                   'and '
                                                                                                   'severe '
                                                                                                   'listing.',
                                                                                                   'Flooding '
                                                                                                   'through '
                                                                                                   'openings '
                                                                                                   'contributed '
                                                                                                   'to '
                                                                                                   'the '
                                                                                                   'rapid '
                                                                                                   'loss '
                                                                                                   'of '
                                                                                                   'stability '
                                                                                                   'and '
                                                                                                   'capsize.',
                                                                                                   'The '
                                                                                                   'official '
                                                                                                   'investigation '
                                                                                                   'report '
                                                                                                   'was '
                                                                                                   'published '
                                                                                                   'as '
                                                                                                   'NOU '
                                                                                                   '1981:11.',
                                                                                                   'A '
                                                                                                   'later '
                                                                                                   'review '
                                                                                                   'by '
                                                                                                   'the '
                                                                                                   'Norwegian '
                                                                                                   'Office '
                                                                                                   'of '
                                                                                                   'the '
                                                                                                   'Auditor '
                                                                                                   'General '
                                                                                                   'found '
                                                                                                   'broad '
                                                                                                   'support '
                                                                                                   'for '
                                                                                                   'the '
                                                                                                   'original '
                                                                                                   "Commission's "
                                                                                                   'conclusion '
                                                                                                   'that '
                                                                                                   'D-6 '
                                                                                                   'failed '
                                                                                                   'due '
                                                                                                   'to '
                                                                                                   'fatigue.'],
                                                                        'lessons': ['Fatigue-critical '
                                                                                    'structural '
                                                                                    'details '
                                                                                    'require '
                                                                                    'rigorous '
                                                                                    'design '
                                                                                    'assessment '
                                                                                    'throughout '
                                                                                    'the operating '
                                                                                    'life of an '
                                                                                    'offshore '
                                                                                    'installation.',
                                                                                    'Attachments '
                                                                                    'welded to '
                                                                                    'primary '
                                                                                    'load-carrying '
                                                                                    'members must '
                                                                                    'be assessed '
                                                                                    'for stress '
                                                                                    'concentration '
                                                                                    'and fatigue '
                                                                                    'effects.',
                                                                                    'Welding '
                                                                                    'quality on '
                                                                                    'safety-critical '
                                                                                    'structural '
                                                                                    'members '
                                                                                    'requires '
                                                                                    'effective '
                                                                                    'fabrication '
                                                                                    'control and '
                                                                                    'inspection.',
                                                                                    'Structural '
                                                                                    'inspection '
                                                                                    'programs must '
                                                                                    'be capable of '
                                                                                    'detecting '
                                                                                    'fatigue '
                                                                                    'cracking '
                                                                                    'before it '
                                                                                    'develops into '
                                                                                    'catastrophic '
                                                                                    'fracture.',
                                                                                    'Offshore '
                                                                                    'structures '
                                                                                    'require '
                                                                                    'adequate '
                                                                                    'redundancy so '
                                                                                    'that a local '
                                                                                    'structural '
                                                                                    'failure does '
                                                                                    'not readily '
                                                                                    'escalate into '
                                                                                    'global '
                                                                                    'collapse.',
                                                                                    'Damage-stability '
                                                                                    'assessments '
                                                                                    'must consider '
                                                                                    'progressive '
                                                                                    'flooding '
                                                                                    'following '
                                                                                    'severe '
                                                                                    'structural '
                                                                                    'damage and '
                                                                                    'loss of '
                                                                                    'buoyancy.',
                                                                                    'Openings that '
                                                                                    'can '
                                                                                    'contribute to '
                                                                                    'progressive '
                                                                                    'flooding '
                                                                                    'require '
                                                                                    'appropriate '
                                                                                    'design and '
                                                                                    'control.',
                                                                                    'Emergency '
                                                                                    'evacuation '
                                                                                    'systems must '
                                                                                    'remain usable '
                                                                                    'during severe '
                                                                                    'list, high '
                                                                                    'waves and '
                                                                                    'rapidly '
                                                                                    'developing '
                                                                                    'structural '
                                                                                    'emergencies.',
                                                                                    'Personnel '
                                                                                    'require '
                                                                                    'effective '
                                                                                    'personal '
                                                                                    'survival '
                                                                                    'equipment '
                                                                                    'appropriate '
                                                                                    'for cold '
                                                                                    'offshore '
                                                                                    'environments.',
                                                                                    'Major '
                                                                                    'offshore '
                                                                                    'accidents '
                                                                                    'require '
                                                                                    'integrated '
                                                                                    'management of '
                                                                                    'structural '
                                                                                    'integrity, '
                                                                                    'emergency '
                                                                                    'preparedness '
                                                                                    'and '
                                                                                    'regulatory '
                                                                                    'assurance.']},
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
                                                   'potential severity of off-site consequences.']},
 'Flixborough Chemical Plant Explosion (UK, 1974)': {'schema_version': 2,
                                                     'metadata': {'date': '1 June 1974',
                                                                  'location': 'Flixborough, '
                                                                              'England, United '
                                                                              'Kingdom',
                                                                  'type': 'Major loss of '
                                                                          'containment of '
                                                                          'cyclohexane followed by '
                                                                          'a flammable vapour '
                                                                          'cloud explosion and '
                                                                          'fires',
                                                                  'fatalities': '28 workers',
                                                                  'injuries': '36 people were '
                                                                              'injured on site and '
                                                                              '53 injuries were '
                                                                              'reported off site',
                                                                  'investigation_agency': 'Court '
                                                                                          'of '
                                                                                          'Inquiry '
                                                                                          'appointed '
                                                                                          'following '
                                                                                          'the '
                                                                                          'Flixborough '
                                                                                          'disaster',
                                                                  'report_title': 'The Flixborough '
                                                                                  'Disaster: '
                                                                                  'Report of the '
                                                                                  'Court of '
                                                                                  'Inquiry',
                                                                  'report_number': None,
                                                                  'report_date': '1975'},
                                                     'event_sequence': ['A crack was discovered in '
                                                                        'reactor No. 5 in March '
                                                                        '1974, and the reactor was '
                                                                        'removed from service.',
                                                                        'To permit continued '
                                                                        'operation, a temporary '
                                                                        'bypass assembly was '
                                                                        'installed between '
                                                                        'reactors No. 4 and No. 6.',
                                                                        'The temporary bypass '
                                                                        'incorporated '
                                                                        'large-diameter pipework '
                                                                        'and bellows and did not '
                                                                        'receive adequate '
                                                                        'engineering design '
                                                                        'assessment.',
                                                                        'On 1 June 1974, a major '
                                                                        'loss of containment '
                                                                        'occurred involving the '
                                                                        'temporary bypass system.',
                                                                        'A large quantity of hot '
                                                                        'cyclohexane was released '
                                                                        'from the process.',
                                                                        'The released cyclohexane '
                                                                        'formed a large flammable '
                                                                        'vapour cloud.',
                                                                        'The vapour cloud '
                                                                        'encountered an ignition '
                                                                        'source.',
                                                                        'A major vapour cloud '
                                                                        'explosion occurred, '
                                                                        'followed by extensive '
                                                                        'fires.',
                                                                        'The explosion caused '
                                                                        'severe destruction within '
                                                                        'the plant and damage '
                                                                        'beyond the site '
                                                                        'boundary.'],
                                                     'contributing_factors': ['The temporary '
                                                                              'bypass modification '
                                                                              'was introduced '
                                                                              'following removal '
                                                                              'of reactor No. 5.',
                                                                              'The bypass '
                                                                              'arrangement did not '
                                                                              'receive adequate '
                                                                              'mechanical-design '
                                                                              'assessment for the '
                                                                              'loads and movements '
                                                                              'that could occur in '
                                                                              'service.',
                                                                              'The modification '
                                                                              'was implemented '
                                                                              'without a complete '
                                                                              'engineered design '
                                                                              'and associated '
                                                                              'drawing.',
                                                                              'The installed '
                                                                              'bypass was not '
                                                                              'subjected to an '
                                                                              'appropriate '
                                                                              'pressure test '
                                                                              'before operation.',
                                                                              'The use and '
                                                                              'arrangement of '
                                                                              'bellows in the '
                                                                              'temporary bypass '
                                                                              'introduced '
                                                                              'mechanical-integrity '
                                                                              'concerns that were '
                                                                              'not adequately '
                                                                              'assessed.',
                                                                              'The facility '
                                                                              'contained a '
                                                                              'substantial '
                                                                              'inventory of '
                                                                              'flammable process '
                                                                              'material capable of '
                                                                              'producing severe '
                                                                              'consequences '
                                                                              'following loss of '
                                                                              'containment.',
                                                                              'Plant layout and '
                                                                              'occupied-building '
                                                                              'vulnerability '
                                                                              'increased the '
                                                                              'potential '
                                                                              'consequences of a '
                                                                              'major explosion.'],
                                                     'system_causes': ['Management controls for '
                                                                       'temporary plant '
                                                                       'modifications were '
                                                                       'inadequate.',
                                                                       'Engineering design '
                                                                       'assurance for the bypass '
                                                                       'modification was '
                                                                       'insufficient.',
                                                                       'The modification was '
                                                                       'undertaken without '
                                                                       'adequate involvement of '
                                                                       'personnel with appropriate '
                                                                       'mechanical-engineering '
                                                                       'competence for the design '
                                                                       'problem.',
                                                                       'Mechanical-integrity '
                                                                       'requirements for the '
                                                                       'temporary modification '
                                                                       'were not adequately '
                                                                       'demonstrated before '
                                                                       'startup.',
                                                                       'Major-accident hazards '
                                                                       'associated with a large '
                                                                       'cyclohexane release and '
                                                                       'vapour cloud explosion '
                                                                       'were not adequately '
                                                                       'addressed.',
                                                                       'Plant layout and '
                                                                       'occupied-building '
                                                                       'protection did not '
                                                                       'adequately account for the '
                                                                       'consequences of a major '
                                                                       'explosion.'],
                                                     'consequences': ['Twenty-eight workers were '
                                                                      'killed.',
                                                                      'Thirty-six people were '
                                                                      'injured on site.',
                                                                      'Fifty-three injuries were '
                                                                      'reported off site.',
                                                                      'The explosion and '
                                                                      'subsequent fires caused '
                                                                      'extensive destruction '
                                                                      'within the plant.',
                                                                      'Buildings and property '
                                                                      'outside the plant boundary '
                                                                      'were damaged.',
                                                                      'The accident demonstrated '
                                                                      'the catastrophic potential '
                                                                      'of a large flammable '
                                                                      'hydrocarbon release and '
                                                                      'vapour cloud explosion.',
                                                                      'The disaster became a major '
                                                                      'reference case for '
                                                                      'process-safety regulation '
                                                                      'and management of plant '
                                                                      'modifications.'],
                                                     'investigation_findings': ['The Court of '
                                                                                'Inquiry '
                                                                                'investigated the '
                                                                                'Flixborough '
                                                                                'disaster and '
                                                                                'reported in 1975.',
                                                                                'The temporary '
                                                                                'bypass installed '
                                                                                'after removal of '
                                                                                'reactor No. 5 was '
                                                                                'central to the '
                                                                                'investigation of '
                                                                                'the major loss of '
                                                                                'containment.',
                                                                                'The bypass '
                                                                                'modification had '
                                                                                'not been '
                                                                                'supported by '
                                                                                'adequate '
                                                                                'engineering '
                                                                                'design '
                                                                                'calculations and '
                                                                                'assessment.',
                                                                                'A complete '
                                                                                'engineering '
                                                                                'drawing of the '
                                                                                'proposed '
                                                                                'modification had '
                                                                                'not been '
                                                                                'prepared.',
                                                                                'The installed '
                                                                                'bypass had not '
                                                                                'been '
                                                                                'appropriately '
                                                                                'pressure tested '
                                                                                'before operation.',
                                                                                'The mechanical '
                                                                                'behaviour of the '
                                                                                'bypass pipework '
                                                                                'and bellows had '
                                                                                'not been '
                                                                                'adequately '
                                                                                'evaluated.',
                                                                                'The inquiry '
                                                                                'identified '
                                                                                'important '
                                                                                'weaknesses in the '
                                                                                'control and '
                                                                                'engineering '
                                                                                'assessment of '
                                                                                'plant '
                                                                                'modifications.',
                                                                                'The disaster '
                                                                                'demonstrated the '
                                                                                'need to consider '
                                                                                'major fire and '
                                                                                'explosion '
                                                                                'consequences in '
                                                                                'plant layout and '
                                                                                'occupied-building '
                                                                                'design.',
                                                                                'The precise '
                                                                                'circumstances '
                                                                                'leading to '
                                                                                'failure of the '
                                                                                'bypass system '
                                                                                'have been subject '
                                                                                'to technical '
                                                                                'discussion, and '
                                                                                'unsupported '
                                                                                'details should '
                                                                                'not be presented '
                                                                                'as conclusively '
                                                                                'established.'],
                                                     'lessons': ['Temporary process modifications '
                                                                 'require the same disciplined '
                                                                 'engineering control as permanent '
                                                                 'modifications.',
                                                                 'A formal Management of Change '
                                                                 'process should assess '
                                                                 'process-safety consequences '
                                                                 'before a modification is '
                                                                 'implemented.',
                                                                 'Temporary pipework must be '
                                                                 'supported by appropriate '
                                                                 'mechanical-design calculations, '
                                                                 'drawings and engineering review.',
                                                                 'Expansion joints and bellows '
                                                                 'require careful assessment of '
                                                                 'pressure thrust, piping loads, '
                                                                 'movement and structural '
                                                                 'restraint.',
                                                                 'Safety-critical temporary '
                                                                 'modifications require '
                                                                 'appropriate inspection and '
                                                                 'testing before startup.',
                                                                 'Personnel approving '
                                                                 'modifications must have '
                                                                 'competence appropriate to the '
                                                                 'engineering disciplines '
                                                                 'involved.',
                                                                 'Major-hazard assessments must '
                                                                 'consider credible large releases '
                                                                 'of flammable process material.',
                                                                 'Plant layout should reduce '
                                                                 'escalation and limit exposure of '
                                                                 'personnel to major fire and '
                                                                 'explosion hazards.',
                                                                 'Occupied buildings and control '
                                                                 'rooms should be located and '
                                                                 'designed with credible explosion '
                                                                 'hazards in mind.',
                                                                 'Large inventories of flammable '
                                                                 'material require multiple '
                                                                 'independent layers of prevention '
                                                                 'and mitigation.',
                                                                 'Lessons from temporary '
                                                                 'modifications should be '
                                                                 'incorporated into operating '
                                                                 'procedures, mechanical-integrity '
                                                                 'programs and process-safety '
                                                                 'management systems.']},
 'Seveso Chemical Accident (Italy, 1976)': {'schema_version': 2,
                                            'metadata': {'date': '10 July 1976',
                                                         'location': 'Meda, near Seveso, Lombardy, '
                                                                     'Italy',
                                                         'type': 'Uncontrolled exothermic reaction '
                                                                 'during trichlorophenol '
                                                                 'production, resulting in a toxic '
                                                                 'release containing TCDD',
                                                         'fatalities': 'No human deaths directly '
                                                                       'attributed to TCDD in the '
                                                                       'referenced HSE accident '
                                                                       'account',
                                                         'injuries': 'No definitive injury count '
                                                                     'established in the verified '
                                                                     'source information',
                                                         'investigation_agency': 'Italian '
                                                                                 'authorities',
                                                         'report_title': None,
                                                         'report_number': None,
                                                         'report_date': None},
                                            'event_sequence': ['A batch process producing '
                                                               '2,4,5-trichlorophenol was '
                                                               'interrupted.',
                                                               'The reactor contents remained hot '
                                                               'following the interruption.',
                                                               'An uncontrolled exothermic '
                                                               'reaction developed in the reactor.',
                                                               'Reactor temperature and pressure '
                                                               'increased.',
                                                               'The reactor bursting disc ruptured '
                                                               'as pressure increased.',
                                                               'A toxic cloud containing TCDD was '
                                                               'released to the atmosphere.',
                                                               'The release contaminated '
                                                               'surrounding communities and land.',
                                                               'Authorities implemented protective '
                                                               'measures, including evacuations.'],
                                            'contributing_factors': ['Hazards associated with '
                                                                     'interruption of the batch '
                                                                     'process.',
                                                                     'Inadequate control of the '
                                                                     'thermal runaway hazard.',
                                                                     'Insufficient prevention of '
                                                                     'hazardous temperature '
                                                                     'escalation.',
                                                                     'Release of toxic material '
                                                                     'through the reactor relief '
                                                                     'discharge.',
                                                                     'Potential for severe '
                                                                     'off-site consequences from '
                                                                     'toxic contamination.'],
                                            'system_causes': ['Inadequate management of hazardous '
                                                              'batch-interruption conditions.',
                                                              'Insufficient assessment and control '
                                                              'of runaway-reaction hazards.',
                                                              'Inadequate prevention of toxic '
                                                              'off-site release consequences.',
                                                              'Weaknesses in major-accident '
                                                              'prevention and emergency '
                                                              'preparedness.'],
                                            'consequences': ['Release of a toxic chemical cloud '
                                                             'containing TCDD.',
                                                             'Contamination of surrounding '
                                                             'residential and agricultural areas.',
                                                             'Evacuation of affected residents.',
                                                             'Significant environmental '
                                                             'contamination.',
                                                             'Long-term public-health and '
                                                             'environmental concerns.',
                                                             'Major social, economic, and '
                                                             'regulatory consequences.',
                                                             'The accident influenced European '
                                                             'major-accident hazard legislation.'],
                                            'investigation_findings': ['The incident originated '
                                                                       'from an uncontrolled '
                                                                       'exothermic reaction.',
                                                                       'The interrupted batch '
                                                                       'operation was important to '
                                                                       'the causal sequence.',
                                                                       'The reaction caused '
                                                                       'reactor temperature and '
                                                                       'pressure to increase.',
                                                                       'The bursting disc ruptured '
                                                                       'during the pressure '
                                                                       'increase.',
                                                                       'The bursting disc was not '
                                                                       'the initiating cause of '
                                                                       'the runaway reaction.',
                                                                       'The resulting discharge '
                                                                       'released toxic material '
                                                                       'containing TCDD.',
                                                                       'The release caused '
                                                                       'significant off-site '
                                                                       'contamination.',
                                                                       'Specific historical '
                                                                       'equipment settings must '
                                                                       'not be inferred without '
                                                                       'evidence.'],
                                            'lessons': ['Identify runaway-reaction hazards through '
                                                        'appropriate process-hazard analysis.',
                                                        'Evaluate abnormal and interrupted batch '
                                                        'operating conditions.',
                                                        'Establish safe shutdown and restart '
                                                        'criteria for hazardous reactions.',
                                                        'Provide adequate control of reaction '
                                                        'temperature and heat removal.',
                                                        'Evaluate appropriate temperature '
                                                        'monitoring and protective safeguards.',
                                                        'Assess pressure-relief discharge '
                                                        'consequences, not only equipment '
                                                        'protection.',
                                                        'Consider suitable containment or '
                                                        'treatment of hazardous relief discharges.',
                                                        'Evaluate potential off-site toxic-release '
                                                        'consequences.',
                                                        'Provide effective emergency planning and '
                                                        'public communication.',
                                                        'Apply management-of-change controls to '
                                                        'process and operating modifications.',
                                                        'Distinguish verified historical '
                                                        'deficiencies from modern '
                                                        'recommendations.']},
 'West Fertilizer Company Explosion (USA, 2013)': {'schema_version': 2,
                                                   'metadata': {'date': '17 April 2013',
                                                                'location': 'West, Texas, USA',
                                                                'type': 'Ammonium nitrate fire and '
                                                                        'explosion',
                                                                'fatalities': 15,
                                                                'injuries': 'More than 260',
                                                                'investigation_agency': 'U.S. '
                                                                                        'Chemical '
                                                                                        'Safety '
                                                                                        'and '
                                                                                        'Hazard '
                                                                                        'Investigation '
                                                                                        'Board '
                                                                                        '(CSB)',
                                                                'report_title': 'West Fertilizer '
                                                                                'Company Final '
                                                                                'Report',
                                                                'report_date': '28 January 2016'},
                                                   'event_sequence': ['On 17 April 2013, a fire '
                                                                      'developed at the West '
                                                                      'Fertilizer Company storage '
                                                                      'and distribution facility '
                                                                      'in West, Texas.',
                                                                      'The first observed smoke '
                                                                      'and flames originated in or '
                                                                      'above the seed room; the '
                                                                      'initial ignition source was '
                                                                      'not conclusively '
                                                                      'established.',
                                                                      'The fire spread through '
                                                                      'combustible building '
                                                                      'materials and contents near '
                                                                      'stored fertilizer-grade '
                                                                      'ammonium nitrate (FGAN).',
                                                                      'Emergency responders '
                                                                      'attended the developing '
                                                                      'fire without adequate '
                                                                      'information about the '
                                                                      'potential FGAN detonation '
                                                                      'hazard.',
                                                                      'A detonation occurred '
                                                                      'following the fire. Heat '
                                                                      'exposure, confinement, and '
                                                                      'possible contamination were '
                                                                      'examined as factors in the '
                                                                      'detonation mechanism; the '
                                                                      'precise sequence was not '
                                                                      'conclusively established.'],
                                                   'contributing_factors': ['Combustible '
                                                                            'construction '
                                                                            'materials and storage '
                                                                            'bins contributed to '
                                                                            'fire development.',
                                                                            'Combustible materials '
                                                                            'located near stored '
                                                                            'FGAN created fire '
                                                                            'exposure and '
                                                                            'potential '
                                                                            'contamination '
                                                                            'hazards.',
                                                                            'The facility lacked '
                                                                            'automatic fire '
                                                                            'detection and '
                                                                            'sprinkler protection.',
                                                                            'Responders had '
                                                                            'insufficient '
                                                                            'specialized '
                                                                            'information and '
                                                                            'training for FGAN '
                                                                            'fire and explosion '
                                                                            'hazards.'],
                                                   'system_causes': ['Regulatory oversight of '
                                                                     'fertilizer-grade ammonium '
                                                                     'nitrate storage was '
                                                                     'inadequate at the time of '
                                                                     'the incident.',
                                                                     'Applicable storage '
                                                                     'requirements and industry '
                                                                     'safeguards did not '
                                                                     'adequately control '
                                                                     'catastrophic explosion '
                                                                     'risks.',
                                                                     'Emergency planning and '
                                                                     'pre-incident coordination '
                                                                     'were insufficient for the '
                                                                     'hazards present.',
                                                                     'Land-use planning allowed '
                                                                     'vulnerable community '
                                                                     'facilities and residences '
                                                                     'near a major FGAN storage '
                                                                     'hazard.'],
                                                   'consequences': ['Fifteen people died, '
                                                                    'including twelve emergency '
                                                                    'responders and three members '
                                                                    'of the public.',
                                                                    'More than 260 people received '
                                                                    'treatment for injuries.',
                                                                    'The explosion caused '
                                                                    'extensive damage to nearby '
                                                                    'homes, schools, and community '
                                                                    'infrastructure.',
                                                                    'The incident caused '
                                                                    'substantial property losses '
                                                                    'and long-term disruption to '
                                                                    'the surrounding community.'],
                                                   'investigation_findings': ['The CSB identified '
                                                                              'serious '
                                                                              'deficiencies '
                                                                              'involving '
                                                                              'combustible '
                                                                              'construction and '
                                                                              'storage practices. '
                                                                              'Potential '
                                                                              'contamination and '
                                                                              'other '
                                                                              'detonation-related '
                                                                              'conditions require '
                                                                              'qualified '
                                                                              'interpretation '
                                                                              'rather than '
                                                                              'attribution to a '
                                                                              'single proven '
                                                                              'mechanism.',
                                                                              'The facility lacked '
                                                                              'automatic fire '
                                                                              'detection and '
                                                                              'sprinkler systems.',
                                                                              'The CSB identified '
                                                                              'deficiencies in '
                                                                              'emergency responder '
                                                                              'hazard awareness '
                                                                              'and preparedness.',
                                                                              'The investigation '
                                                                              'identified '
                                                                              'shortcomings in '
                                                                              'regulatory '
                                                                              'oversight and '
                                                                              'storage safety '
                                                                              'requirements.',
                                                                              'The CSB issued '
                                                                              'recommendations '
                                                                              'concerning storage '
                                                                              'safeguards, '
                                                                              'emergency response, '
                                                                              'regulatory '
                                                                              'improvements, and '
                                                                              'community '
                                                                              'protection.'],
                                                   'lessons': ['Apply appropriate noncombustible '
                                                               'construction and segregation '
                                                               'controls for FGAN storage.',
                                                               'Provide suitable fire detection, '
                                                               'suppression, and fire prevention '
                                                               'safeguards.',
                                                               'Control combustible contamination '
                                                               'and heat exposure around ammonium '
                                                               'nitrate.',
                                                               'Conduct pre-incident planning with '
                                                               'emergency responders and '
                                                               'communicate credible explosion '
                                                               'hazards.',
                                                               'Train responders to recognize '
                                                               'situations requiring defensive '
                                                               'response and evacuation.',
                                                               'Evaluate offsite consequences and '
                                                               'appropriate separation from '
                                                               'occupied community areas.',
                                                               'Maintain regulatory compliance and '
                                                               'periodically review evolving '
                                                               'ammonium nitrate storage '
                                                               'guidance.'],
                                                   'official_sources': [{'organization': 'U.S. '
                                                                                         'Chemical '
                                                                                         'Safety '
                                                                                         'Board',
                                                                         'title': 'West Fertilizer '
                                                                                  'Explosion and '
                                                                                  'Fire',
                                                                         'url': 'https://www.csb.gov/west-fertilizer-explosion-and-fire-/',
                                                                         'source_type': 'official_investigation_page',
                                                                         'verified': True},
                                                                        {'organization': 'U.S. '
                                                                                         'Chemical '
                                                                                         'Safety '
                                                                                         'Board',
                                                                         'title': 'West Fertilizer '
                                                                                  'Company Final '
                                                                                  'Report',
                                                                         'url': 'https://www.csb.gov/assets/1/6/west_fertilizer_final_report_for_website_021216.pdf',
                                                                         'source_type': 'official_investigation_report',
                                                                         'verified': True}]},
 'Toulouse AZF Fertilizer Plant Explosion (France, 2001)': {'schema_version': 2,
                                                            'metadata': {'date': '21 September '
                                                                                 '2001',
                                                                         'location': 'Toulouse, '
                                                                                     'France',
                                                                         'type': 'Ammonium nitrate '
                                                                                 'storage '
                                                                                 'explosion',
                                                                         'fatalities': 31,
                                                                         'injuries': '2,442 '
                                                                                     'injured/affected '
                                                                                     'persons '
                                                                                     'recorded by '
                                                                                     'the '
                                                                                     'Haute-Garonne '
                                                                                     'Prefecture '
                                                                                     'on 17 '
                                                                                     'October 2001',
                                                                         'investigation_agency': 'French '
                                                                                                 'judicial '
                                                                                                 'authorities '
                                                                                                 'and '
                                                                                                 'industrial '
                                                                                                 'safety '
                                                                                                 'investigators',
                                                                         'report_title': 'Toulouse '
                                                                                         'AZF '
                                                                                         'Explosion '
                                                                                         '— '
                                                                                         'Investigation '
                                                                                         'and '
                                                                                         'Technical '
                                                                                         'Findings',
                                                                         'report_date': 'Multiple '
                                                                                        'investigation '
                                                                                        'and '
                                                                                        'judicial '
                                                                                        'dates'},
                                                            'event_sequence': ['On 21 September '
                                                                               '2001, a major '
                                                                               'explosion occurred '
                                                                               'at the AZF '
                                                                               'fertilizer plant '
                                                                               'in Toulouse, '
                                                                               'France.',
                                                                               'The explosion '
                                                                               'involved ammonium '
                                                                               'nitrate material '
                                                                               'stored in a '
                                                                               'facility building.',
                                                                               'The blast caused '
                                                                               'severe destruction '
                                                                               'within the '
                                                                               'industrial site '
                                                                               'and extensive '
                                                                               'damage in '
                                                                               'surrounding urban '
                                                                               'areas.',
                                                                               'Emergency services '
                                                                               'responded to '
                                                                               'widespread '
                                                                               'casualties, '
                                                                               'structural damage, '
                                                                               'and disruption to '
                                                                               'nearby '
                                                                               'communities.',
                                                                               'The precise '
                                                                               'initiating '
                                                                               'mechanism remained '
                                                                               'a subject of '
                                                                               'technical '
                                                                               'investigation and '
                                                                               'judicial '
                                                                               'proceedings.'],
                                                            'contributing_factors': ['Storage of '
                                                                                     'hazardous '
                                                                                     'ammonium '
                                                                                     'nitrate '
                                                                                     'material '
                                                                                     'created the '
                                                                                     'potential '
                                                                                     'for severe '
                                                                                     'explosion '
                                                                                     'consequences.',
                                                                                     'Material-handling, '
                                                                                     'storage, and '
                                                                                     'contamination-control '
                                                                                     'practices '
                                                                                     'were '
                                                                                     'important '
                                                                                     'subjects of '
                                                                                     'the '
                                                                                     'investigation.',
                                                                                     'The '
                                                                                     'proximity of '
                                                                                     'populated '
                                                                                     'areas '
                                                                                     'increased '
                                                                                     'the severity '
                                                                                     'of offsite '
                                                                                     'consequences.',
                                                                                     'Uncertainty '
                                                                                     'surrounding '
                                                                                     'the '
                                                                                     'initiating '
                                                                                     'mechanism '
                                                                                     'complicated '
                                                                                     'the '
                                                                                     'reconstruction '
                                                                                     'of the '
                                                                                     'accident '
                                                                                     'sequence.'],
                                                            'system_causes': ['The accident '
                                                                              'demonstrated the '
                                                                              'need for rigorous '
                                                                              'management of '
                                                                              'major-accident '
                                                                              'hazards associated '
                                                                              'with ammonium '
                                                                              'nitrate storage.',
                                                                              'Storage '
                                                                              'segregation, '
                                                                              'material '
                                                                              'identification, '
                                                                              'contamination '
                                                                              'prevention, and '
                                                                              'housekeeping '
                                                                              'require effective '
                                                                              'management systems.',
                                                                              'Land-use planning '
                                                                              'and control of '
                                                                              'development around '
                                                                              'hazardous '
                                                                              'industrial '
                                                                              'installations are '
                                                                              'essential for '
                                                                              'limiting offsite '
                                                                              'consequences.',
                                                                              'Major-accident '
                                                                              'emergency '
                                                                              'preparedness must '
                                                                              'account for '
                                                                              'credible '
                                                                              'high-consequence '
                                                                              'explosion '
                                                                              'scenarios.'],
                                                            'consequences': ['Thirty-one people '
                                                                             'died.',
                                                                             'The Haute-Garonne '
                                                                             'Prefecture recorded '
                                                                             '2,442 injured or '
                                                                             'affected persons in '
                                                                             'its October 2001 '
                                                                             'assessment.',
                                                                             'The explosion caused '
                                                                             'extensive '
                                                                             'destruction at the '
                                                                             'AZF facility.',
                                                                             'Residential, '
                                                                             'commercial, and '
                                                                             'public buildings in '
                                                                             'Toulouse sustained '
                                                                             'significant blast '
                                                                             'damage.',
                                                                             'The accident caused '
                                                                             'major social, '
                                                                             'economic, and '
                                                                             'environmental '
                                                                             'disruption.'],
                                                            'investigation_findings': ['French '
                                                                                       'investigations '
                                                                                       'examined '
                                                                                       'the '
                                                                                       'condition '
                                                                                       'and '
                                                                                       'management '
                                                                                       'of '
                                                                                       'ammonium '
                                                                                       'nitrate '
                                                                                       'material '
                                                                                       'stored at '
                                                                                       'the '
                                                                                       'facility.',
                                                                                       'Technical '
                                                                                       'investigations '
                                                                                       'considered '
                                                                                       'possible '
                                                                                       'initiating '
                                                                                       'mechanisms, '
                                                                                       'including '
                                                                                       'contamination-related '
                                                                                       'scenarios, '
                                                                                       'without '
                                                                                       'establishing '
                                                                                       'a '
                                                                                       'universally '
                                                                                       'uncontested '
                                                                                       'explanation.',
                                                                                       'The '
                                                                                       'accident '
                                                                                       'highlighted '
                                                                                       'the '
                                                                                       'consequences '
                                                                                       'of '
                                                                                       'locating '
                                                                                       'major '
                                                                                       'industrial '
                                                                                       'hazards '
                                                                                       'close to '
                                                                                       'densely '
                                                                                       'populated '
                                                                                       'areas.',
                                                                                       'Investigation '
                                                                                       'and '
                                                                                       'judicial '
                                                                                       'conclusions '
                                                                                       'must be '
                                                                                       'distinguished '
                                                                                       'from '
                                                                                       'engineering '
                                                                                       'hypotheses '
                                                                                       'and '
                                                                                       'subsequent '
                                                                                       'safety '
                                                                                       'recommendations.'],
                                                            'lessons': ['Apply robust ammonium '
                                                                        'nitrate storage controls, '
                                                                        'including material '
                                                                        'segregation and '
                                                                        'prevention of '
                                                                        'incompatible-material '
                                                                        'contamination.',
                                                                        'Maintain accurate '
                                                                        'material identification, '
                                                                        'inventory records, and '
                                                                        'housekeeping standards.',
                                                                        'Evaluate credible '
                                                                        'explosion scenarios and '
                                                                        'their potential offsite '
                                                                        'consequences.',
                                                                        'Use appropriate land-use '
                                                                        'planning and separation '
                                                                        'controls around '
                                                                        'major-hazard '
                                                                        'installations.',
                                                                        'Maintain effective '
                                                                        'emergency preparedness '
                                                                        'and coordination with '
                                                                        'public authorities.',
                                                                        'Clearly distinguish '
                                                                        'confirmed investigation '
                                                                        'findings from hypotheses '
                                                                        'when preparing technical '
                                                                        'accident reports.',
                                                                        'Review major-accident '
                                                                        'prevention systems and '
                                                                        'management-of-change '
                                                                        'arrangements for '
                                                                        'hazardous material '
                                                                        'storage.'],
                                                            'official_sources': [{'organization': 'French '
                                                                                                  'Ministry '
                                                                                                  '/ '
                                                                                                  'BARPI',
                                                                                  'title': 'ARIA '
                                                                                           '21329 '
                                                                                           '— '
                                                                                           'Explosion '
                                                                                           'of '
                                                                                           'ammonium '
                                                                                           'nitrate '
                                                                                           'in a '
                                                                                           'fertilizer '
                                                                                           'plant',
                                                                                  'url': 'https://www.aria.developpement-durable.gouv.fr/fiche_detaillee/21329-2/?lang=en',
                                                                                  'source_type': 'official_accident_record',
                                                                                  'verified': True},
                                                                                 {'organization': 'French '
                                                                                                  'Ministry '
                                                                                                  '/ '
                                                                                                  'BARPI',
                                                                                  'title': 'ARIA '
                                                                                           '21329 '
                                                                                           '— '
                                                                                           'Detailed '
                                                                                           'technical '
                                                                                           'accident '
                                                                                           'report',
                                                                                  'url': 'https://www.aria.developpement-durable.gouv.fr/wp-content/files_mf/FD_21329_TOULOUSE_PA_10092015.pdf',
                                                                                  'source_type': 'official_technical_report',
                                                                                  'verified': True}]},
 'Phillips Petroleum Pasadena Explosion (USA, 1989)': {'schema_version': 2,
                                                       'metadata': {'date': '23 October 1989',
                                                                    'location': 'Pasadena, Texas, '
                                                                                'USA',
                                                                    'type': 'Flammable hydrocarbon '
                                                                            'release, vapor-cloud '
                                                                            'explosion and fire',
                                                                    'fatalities': 23,
                                                                    'injuries': 'More than 130 '
                                                                                'people injured',
                                                                    'investigation_agency': 'US '
                                                                                            'Occupational '
                                                                                            'Safety '
                                                                                            'and '
                                                                                            'Health '
                                                                                            'Administration '
                                                                                            '(OSHA)',
                                                                    'report_title': 'The Phillips '
                                                                                    '66 Company '
                                                                                    'Houston '
                                                                                    'Chemical '
                                                                                    'Complex '
                                                                                    'Explosion and '
                                                                                    'Fire',
                                                                    'report_date': 'April 1990'},
                                                       'event_sequence': ['On 23 October 1989, '
                                                                          'maintenance work was '
                                                                          'being performed at the '
                                                                          'Phillips Petroleum '
                                                                          'polyethylene complex in '
                                                                          'Pasadena, Texas.',
                                                                          'A process isolation '
                                                                          'arrangement involving a '
                                                                          'pneumatically operated '
                                                                          'valve failed to prevent '
                                                                          'the release of '
                                                                          'flammable hydrocarbons.',
                                                                          'The investigation '
                                                                          'identified reversed '
                                                                          'pneumatic connections '
                                                                          'associated with the '
                                                                          'isolation valve.',
                                                                          'A substantial release '
                                                                          'of flammable process '
                                                                          'material formed a vapor '
                                                                          'cloud.',
                                                                          'The vapor cloud '
                                                                          'ignited, producing a '
                                                                          'major explosion '
                                                                          'followed by fires and '
                                                                          'additional explosions.',
                                                                          'Emergency response and '
                                                                          'firefighting operations '
                                                                          'continued under severe '
                                                                          'conditions caused by '
                                                                          'extensive plant '
                                                                          'damage.'],
                                                       'contributing_factors': ['Inadequate '
                                                                                'positive '
                                                                                'isolation of '
                                                                                'hazardous process '
                                                                                'equipment during '
                                                                                'maintenance.',
                                                                                'Reliance on an '
                                                                                'isolation '
                                                                                'arrangement '
                                                                                'vulnerable to '
                                                                                'incorrect valve '
                                                                                'operation.',
                                                                                'Reversed '
                                                                                'pneumatic '
                                                                                'connections '
                                                                                'associated with '
                                                                                'the isolation '
                                                                                'valve.',
                                                                                'Insufficient '
                                                                                'verification of '
                                                                                'equipment '
                                                                                'isolation before '
                                                                                'maintenance '
                                                                                'activities.',
                                                                                'Large inventories '
                                                                                'of flammable '
                                                                                'hydrocarbons '
                                                                                'increased the '
                                                                                'potential '
                                                                                'consequences of a '
                                                                                'loss of '
                                                                                'containment.',
                                                                                'The arrangement '
                                                                                'and proximity of '
                                                                                'process equipment '
                                                                                'contributed to '
                                                                                'escalation '
                                                                                'following the '
                                                                                'initial '
                                                                                'explosion.'],
                                                       'system_causes': ['Deficiencies in '
                                                                         'maintenance isolation '
                                                                         'procedures and '
                                                                         'verification practices.',
                                                                         'Inadequate management of '
                                                                         'maintenance activities '
                                                                         'involving hazardous '
                                                                         'process equipment.',
                                                                         'Weaknesses in process '
                                                                         'safety controls intended '
                                                                         'to prevent major '
                                                                         'hydrocarbon releases.',
                                                                         'Insufficient assurance '
                                                                         'that critical valve '
                                                                         'configurations and '
                                                                         'operating arrangements '
                                                                         'were correctly '
                                                                         'established.',
                                                                         'The accident '
                                                                         'demonstrated the need '
                                                                         'for stronger process '
                                                                         'safety management, '
                                                                         'including equipment '
                                                                         'integrity, operating '
                                                                         'procedures, training, '
                                                                         'and maintenance '
                                                                         'controls.'],
                                                       'consequences': ['Twenty-three people died.',
                                                                        'More than 130 people were '
                                                                        'injured.',
                                                                        'Major explosions and '
                                                                        'fires caused extensive '
                                                                        'destruction within the '
                                                                        'polyethylene complex.',
                                                                        'Multiple process units '
                                                                        'and associated '
                                                                        'infrastructure sustained '
                                                                        'severe damage.',
                                                                        'The accident caused major '
                                                                        'operational disruption '
                                                                        'and substantial economic '
                                                                        'losses.'],
                                                       'investigation_findings': ['The '
                                                                                  'investigation '
                                                                                  'identified '
                                                                                  'failures in the '
                                                                                  'isolation '
                                                                                  'arrangements '
                                                                                  'used during '
                                                                                  'maintenance.',
                                                                                  'Reversed '
                                                                                  'pneumatic '
                                                                                  'connections on '
                                                                                  'an isolation '
                                                                                  'valve were '
                                                                                  'identified as '
                                                                                  'an important '
                                                                                  'factor in the '
                                                                                  'release '
                                                                                  'sequence.',
                                                                                  'The isolation '
                                                                                  'arrangements '
                                                                                  'did not provide '
                                                                                  'adequate '
                                                                                  'protection '
                                                                                  'against '
                                                                                  'inadvertent '
                                                                                  'hydrocarbon '
                                                                                  'release.',
                                                                                  'The accident '
                                                                                  'demonstrated '
                                                                                  'the potential '
                                                                                  'for a major '
                                                                                  'vapor-cloud '
                                                                                  'explosion '
                                                                                  'following a '
                                                                                  'large release '
                                                                                  'of flammable '
                                                                                  'process '
                                                                                  'materials.',
                                                                                  'OSHA '
                                                                                  'investigated '
                                                                                  'the incident '
                                                                                  'and identified '
                                                                                  'serious '
                                                                                  'workplace '
                                                                                  'safety '
                                                                                  'deficiencies.',
                                                                                  'Subsequent '
                                                                                  'technical '
                                                                                  'reviews '
                                                                                  'highlighted the '
                                                                                  'importance of '
                                                                                  'positive '
                                                                                  'isolation, '
                                                                                  'maintenance '
                                                                                  'procedures, and '
                                                                                  'process safety '
                                                                                  'management.'],
                                                       'lessons': ['Apply positive isolation '
                                                                   'methods appropriate to the '
                                                                   'process hazards, such as '
                                                                   'physical disconnection or '
                                                                   'correctly designed blinds '
                                                                   'where required.',
                                                                   'Do not rely solely on a single '
                                                                   'remotely operated valve for '
                                                                   'hazardous maintenance '
                                                                   'isolation when a more robust '
                                                                   'isolation standard is '
                                                                   'required.',
                                                                   'Verify valve position, '
                                                                   'actuator connections, and '
                                                                   'isolation integrity before '
                                                                   'maintenance begins.',
                                                                   'Use formal permit-to-work, '
                                                                   'lockout/tagout, and equipment '
                                                                   'handover procedures.',
                                                                   'Implement effective management '
                                                                   'of change for modifications '
                                                                   'affecting valve actuation, '
                                                                   'instrumentation, and '
                                                                   'maintenance configurations.',
                                                                   'Evaluate major hydrocarbon '
                                                                   'release and vapor-cloud '
                                                                   'explosion scenarios in process '
                                                                   'hazard analyses.',
                                                                   'Maintain effective emergency '
                                                                   'response arrangements for '
                                                                   'major explosions and fires.',
                                                                   'Audit critical process safety '
                                                                   'barriers and verify their '
                                                                   'effectiveness in the field.'],
                                                       'official_sources': [{'organization': 'US '
                                                                                             'OSHA',
                                                                             'title': 'OSHA '
                                                                                      'Accident '
                                                                                      'Report '
                                                                                      '14219646',
                                                                             'url': 'https://www.osha.gov/ords/imis/accidentsearch.accident_detail?id=14219646',
                                                                             'source_type': 'official_accident_record',
                                                                             'verified': True},
                                                                            {'organization': 'US '
                                                                                             'OSHA',
                                                                             'title': 'OSHA '
                                                                                      'Investigation '
                                                                                      'Correspondence '
                                                                                      '— 12 '
                                                                                      'February '
                                                                                      '1991',
                                                                             'url': 'https://www.osha.gov/laws-regs/standardinterpretations/1991-02-12',
                                                                             'source_type': 'official_investigation_correspondence',
                                                                             'verified': True},
                                                                            {'organization': 'UK '
                                                                                             'Health '
                                                                                             'and '
                                                                                             'Safety '
                                                                                             'Executive',
                                                                             'title': 'Phillips 66 '
                                                                                      'Pasadena '
                                                                                      'Accident '
                                                                                      'Review',
                                                                             'url': 'https://www.hse.gov.uk/comah/sragtech/casepasadena89.htm',
                                                                             'source_type': 'official_technical_case_review',
                                                                             'verified': True}]},
 'Formosa Plastics Point Comfort Explosion (USA, 2005)': {'schema_version': 2,
                                                          'metadata': {'date': '6 October 2005',
                                                                       'location': 'Point Comfort, '
                                                                                   'Texas, USA',
                                                                       'type': 'Flammable '
                                                                               'propylene release, '
                                                                               'vapor-cloud '
                                                                               'ignition and fire',
                                                                       'fatalities': 0,
                                                                       'injuries': '16 workers '
                                                                                   'injured, one '
                                                                                   'seriously',
                                                                       'investigation_agency': 'US '
                                                                                               'Chemical '
                                                                                               'Safety '
                                                                                               'and '
                                                                                               'Hazard '
                                                                                               'Investigation '
                                                                                               'Board '
                                                                                               '(CSB)',
                                                                       'report_title': 'Fire at '
                                                                                       'Formosa '
                                                                                       'Plastics '
                                                                                       'Corporation: '
                                                                                       'Evaluating '
                                                                                       'Process '
                                                                                       'Hazards',
                                                                       'report_date': '20 July '
                                                                                      '2006'},
                                                          'event_sequence': ['On 6 October 2005, a '
                                                                             'forklift towing a '
                                                                             'trailer was '
                                                                             'operating at the '
                                                                             'Formosa Plastics '
                                                                             'facility in Point '
                                                                             'Comfort, Texas.',
                                                                             'The vehicle struck '
                                                                             'an unprotected valve '
                                                                             'associated with a '
                                                                             'pressurized '
                                                                             'propylene process '
                                                                             'system.',
                                                                             'The impact damaged '
                                                                             'the equipment and '
                                                                             'caused a release of '
                                                                             'flammable propylene.',
                                                                             'The released '
                                                                             'propylene ignited, '
                                                                             'resulting in a major '
                                                                             'fire.',
                                                                             'The fire affected '
                                                                             'nearby process '
                                                                             'equipment and '
                                                                             'created conditions '
                                                                             'for further '
                                                                             'escalation.',
                                                                             'Emergency response '
                                                                             'personnel worked to '
                                                                             'control the incident '
                                                                             'and isolate the '
                                                                             'affected process '
                                                                             'system.'],
                                                          'contributing_factors': ['A vulnerable '
                                                                                   'process valve '
                                                                                   'was exposed to '
                                                                                   'potential '
                                                                                   'impact from '
                                                                                   'industrial '
                                                                                   'vehicle '
                                                                                   'movements.',
                                                                                   'Physical '
                                                                                   'protection '
                                                                                   'against '
                                                                                   'vehicle impact '
                                                                                   'was inadequate '
                                                                                   'at the '
                                                                                   'affected '
                                                                                   'equipment '
                                                                                   'location.',
                                                                                   'The release '
                                                                                   'involved '
                                                                                   'flammable '
                                                                                   'propylene '
                                                                                   'under process '
                                                                                   'conditions.',
                                                                                   'Emergency '
                                                                                   'isolation '
                                                                                   'arrangements '
                                                                                   'did not '
                                                                                   'provide '
                                                                                   'sufficiently '
                                                                                   'effective '
                                                                                   'control of the '
                                                                                   'released '
                                                                                   'material.',
                                                                                   'Fire '
                                                                                   'protection and '
                                                                                   'equipment '
                                                                                   'vulnerability '
                                                                                   'contributed to '
                                                                                   'the potential '
                                                                                   'for incident '
                                                                                   'escalation.',
                                                                                   'The process '
                                                                                   'hazard '
                                                                                   'evaluation did '
                                                                                   'not adequately '
                                                                                   'address the '
                                                                                   'consequences '
                                                                                   'of vehicle '
                                                                                   'impact on '
                                                                                   'exposed '
                                                                                   'hazardous '
                                                                                   'process '
                                                                                   'equipment.'],
                                                          'system_causes': ['Insufficient '
                                                                            'identification and '
                                                                            'control of '
                                                                            'vehicle-impact '
                                                                            'hazards affecting '
                                                                            'hazardous process '
                                                                            'equipment.',
                                                                            'Inadequate evaluation '
                                                                            'of potential '
                                                                            'loss-of-containment '
                                                                            'scenarios during '
                                                                            'process hazard '
                                                                            'analysis.',
                                                                            'Deficiencies in the '
                                                                            'design and '
                                                                            'effectiveness of '
                                                                            'emergency isolation '
                                                                            'arrangements.',
                                                                            'Insufficient '
                                                                            'protection of '
                                                                            'equipment exposed to '
                                                                            'severe fire '
                                                                            'conditions.',
                                                                            'Weaknesses in the '
                                                                            'implementation and '
                                                                            'verification of '
                                                                            'major-accident '
                                                                            'prevention '
                                                                            'safeguards.'],
                                                          'consequences': ['No fatalities were '
                                                                           'reported.',
                                                                           'Sixteen workers were '
                                                                           'injured, including one '
                                                                           'seriously.',
                                                                           'A major propylene fire '
                                                                           'caused significant '
                                                                           'damage to process '
                                                                           'equipment.',
                                                                           'The incident disrupted '
                                                                           'operations at the '
                                                                           'affected facility.',
                                                                           'The accident '
                                                                           'demonstrated the '
                                                                           'potential for a '
                                                                           'localized mechanical '
                                                                           'impact to escalate '
                                                                           'into a major process '
                                                                           'safety event.'],
                                                          'investigation_findings': ['The US '
                                                                                     'Chemical '
                                                                                     'Safety Board '
                                                                                     'investigated '
                                                                                     'the 6 '
                                                                                     'October 2005 '
                                                                                     'incident.',
                                                                                     'The '
                                                                                     'initiating '
                                                                                     'event '
                                                                                     'involved a '
                                                                                     'forklift '
                                                                                     'towing a '
                                                                                     'trailer '
                                                                                     'striking an '
                                                                                     'unprotected '
                                                                                     'process '
                                                                                     'valve.',
                                                                                     'Damage to '
                                                                                     'the valve '
                                                                                     'resulted in '
                                                                                     'the release '
                                                                                     'of flammable '
                                                                                     'propylene.',
                                                                                     'The '
                                                                                     'investigation '
                                                                                     'identified '
                                                                                     'inadequate '
                                                                                     'protection '
                                                                                     'of '
                                                                                     'vulnerable '
                                                                                     'process '
                                                                                     'equipment '
                                                                                     'from vehicle '
                                                                                     'impacts.',
                                                                                     'The CSB '
                                                                                     'identified '
                                                                                     'weaknesses '
                                                                                     'in emergency '
                                                                                     'isolation '
                                                                                     'and fire '
                                                                                     'protection '
                                                                                     'arrangements.',
                                                                                     'The '
                                                                                     'investigation '
                                                                                     'highlighted '
                                                                                     'deficiencies '
                                                                                     'in '
                                                                                     'evaluating '
                                                                                     'and '
                                                                                     'controlling '
                                                                                     'credible '
                                                                                     'process '
                                                                                     'hazards.'],
                                                          'lessons': ['Identify hazardous process '
                                                                      'equipment exposed to '
                                                                      'vehicle movements and '
                                                                      'provide suitable impact '
                                                                      'barriers or physical '
                                                                      'separation.',
                                                                      'Include vehicle-impact and '
                                                                      'mechanical-damage scenarios '
                                                                      'in process hazard analyses '
                                                                      'where credible.',
                                                                      'Design emergency isolation '
                                                                      'systems to limit hazardous '
                                                                      'material releases and '
                                                                      'verify their effectiveness '
                                                                      'under emergency conditions.',
                                                                      'Evaluate remote-operated '
                                                                      'isolation valves and their '
                                                                      'accessibility during fires '
                                                                      'or explosions.',
                                                                      'Assess passive fire '
                                                                      'protection requirements for '
                                                                      'critical equipment and '
                                                                      'structural supports.',
                                                                      'Maintain effective traffic '
                                                                      'management and industrial '
                                                                      'vehicle operating controls.',
                                                                      'Verify that safeguards '
                                                                      'identified during process '
                                                                      'hazard analysis are '
                                                                      'implemented and maintained.',
                                                                      'Use incident findings to '
                                                                      'improve mechanical '
                                                                      'integrity, emergency '
                                                                      'preparedness, and process '
                                                                      'safety management.'],
                                                          'official_sources': [{'organization': 'US '
                                                                                                'CSB',
                                                                                'title': 'Formosa '
                                                                                         'Plastics '
                                                                                         'Propylene '
                                                                                         'Explosion',
                                                                                'url': 'https://www.csb.gov/formosa-plastics-propylene-explosion/',
                                                                                'source_type': 'official_investigation_page',
                                                                                'verified': True},
                                                                               {'organization': 'US '
                                                                                                'CSB',
                                                                                'title': 'Fire at '
                                                                                         'Formosa '
                                                                                         'Plastics '
                                                                                         'Corporation: '
                                                                                         'Evaluating '
                                                                                         'Process '
                                                                                         'Hazards',
                                                                                'url': 'https://www.csb.gov/assets/1/20/formosa_report.pdf',
                                                                                'source_type': 'official_case_study_pdf',
                                                                                'verified': True}]},
 'Williams Olefins Geismar Explosion (USA, 2013)': {'schema_version': 2,
                                                    'metadata': {'date': '13 June 2013',
                                                                 'location': 'Geismar, Louisiana, '
                                                                             'USA',
                                                                 'type': 'Reboiler overpressure '
                                                                         'rupture, BLEVE and fire',
                                                                 'fatalities': 2,
                                                                 'injuries': '167 reported '
                                                                             'injuries',
                                                                 'investigation_agency': 'US '
                                                                                         'Chemical '
                                                                                         'Safety '
                                                                                         'and '
                                                                                         'Hazard '
                                                                                         'Investigation '
                                                                                         'Board '
                                                                                         '(CSB)',
                                                                 'report_title': 'Williams Geismar '
                                                                                 'Olefins Plant '
                                                                                 'Reboiler Rupture '
                                                                                 'and Fire',
                                                                 'report_date': '19 October 2016'},
                                                    'event_sequence': ['On 13 June 2013, a '
                                                                       'catastrophic equipment '
                                                                       'failure occurred at the '
                                                                       'Williams Olefins plant in '
                                                                       'Geismar, Louisiana.',
                                                                       'A propylene fractionator '
                                                                       'reboiler was in an offline '
                                                                       'operating condition.',
                                                                       'Liquid became trapped in '
                                                                       'the reboiler while an '
                                                                       'effective pressure relief '
                                                                       'path was unavailable.',
                                                                       'Heating of the trapped '
                                                                       'liquid caused hydraulic '
                                                                       'thermal expansion and a '
                                                                       'rapid pressure increase.',
                                                                       'The reboiler ruptured '
                                                                       'catastrophically after the '
                                                                       'internal pressure exceeded '
                                                                       'its mechanical capacity.',
                                                                       'The rupture produced a '
                                                                       'boiling liquid expanding '
                                                                       'vapor explosion (BLEVE), '
                                                                       'followed by a fire.'],
                                                    'contributing_factors': ['The offline reboiler '
                                                                             'was vulnerable to '
                                                                             'overpressure from '
                                                                             'thermal expansion of '
                                                                             'trapped liquid.',
                                                                             'An effective '
                                                                             'pressure relief path '
                                                                             'was not available '
                                                                             'for the hazardous '
                                                                             'equipment '
                                                                             'configuration.',
                                                                             "The equipment's "
                                                                             'special operating '
                                                                             'status was not '
                                                                             'adequately addressed '
                                                                             'in overpressure '
                                                                             'protection '
                                                                             'arrangements.',
                                                                             'Administrative '
                                                                             'controls were '
                                                                             'insufficient to '
                                                                             'prevent the '
                                                                             'hazardous '
                                                                             'configuration.',
                                                                             'Process hazard '
                                                                             'evaluation did not '
                                                                             'adequately identify '
                                                                             'or control the '
                                                                             'thermal expansion '
                                                                             'scenario.'],
                                                    'system_causes': ['Deficiencies in process '
                                                                      'hazard analysis (PHA) and '
                                                                      'the evaluation of credible '
                                                                      'overpressure scenarios.',
                                                                      'Weaknesses in management of '
                                                                      'change (MOC) practices '
                                                                      'affecting equipment '
                                                                      'configuration and '
                                                                      'operation.',
                                                                      'Insufficient pre-startup '
                                                                      'safety review (PSSR) '
                                                                      'effectiveness.',
                                                                      'Inadequate operating '
                                                                      'procedures and controls for '
                                                                      'equipment in non-routine '
                                                                      'operating conditions.',
                                                                      'Insufficient verification '
                                                                      'of pressure relief '
                                                                      'requirements for standby '
                                                                      'and out-of-service '
                                                                      'equipment.',
                                                                      'Weaknesses in process '
                                                                      'safety program '
                                                                      'implementation and '
                                                                      'oversight.'],
                                                    'consequences': ['Two workers were fatally '
                                                                     'injured.',
                                                                     'A total of 167 injuries were '
                                                                     'reported.',
                                                                     'The reboiler suffered '
                                                                     'catastrophic rupture.',
                                                                     'The resulting explosion and '
                                                                     'fire damaged plant '
                                                                     'equipment.',
                                                                     'The incident demonstrated '
                                                                     'the major-accident potential '
                                                                     'of trapped-liquid thermal '
                                                                     'expansion in process '
                                                                     'equipment.'],
                                                    'investigation_findings': ['The US Chemical '
                                                                               'Safety Board '
                                                                               'investigated the '
                                                                               'incident and '
                                                                               'released its final '
                                                                               'case study on 19 '
                                                                               'October 2016.',
                                                                               'Hydraulic thermal '
                                                                               'expansion of '
                                                                               'trapped liquid was '
                                                                               'the initiating '
                                                                               'overpressure '
                                                                               'mechanism.',
                                                                               'The failed '
                                                                               'reboiler did not '
                                                                               'have effective '
                                                                               'pressure relief '
                                                                               'for the relevant '
                                                                               'operating '
                                                                               'configuration.',
                                                                               'The CSB identified '
                                                                               'deficiencies '
                                                                               'involving process '
                                                                               'hazard analysis, '
                                                                               'management of '
                                                                               'change, '
                                                                               'pre-startup safety '
                                                                               'review and '
                                                                               'operating '
                                                                               'procedures.',
                                                                               'The CSB '
                                                                               'recommended '
                                                                               'strengthening '
                                                                               'industry guidance '
                                                                               'on pressure relief '
                                                                               'for equipment in '
                                                                               'standby and '
                                                                               'out-of-service '
                                                                               'conditions.',
                                                                               'The CSB emphasized '
                                                                               'the need for '
                                                                               'pressure relief '
                                                                               'protection where '
                                                                               'credible internal '
                                                                               'overpressure could '
                                                                               'exceed equipment '
                                                                               'design limits.'],
                                                    'lessons': ['Evaluate trapped-liquid thermal '
                                                                'expansion for all credible '
                                                                'blocked-in equipment '
                                                                'configurations.',
                                                                'Provide suitable pressure relief '
                                                                'protection where credible '
                                                                'overpressure scenarios can exceed '
                                                                'equipment design limits.',
                                                                'Explicitly assess equipment in '
                                                                'standby, isolated, and '
                                                                'out-of-service operating '
                                                                'conditions.',
                                                                'Use PHA and MOC reviews to '
                                                                'identify changes that can '
                                                                'compromise pressure relief or '
                                                                'introduce trapped-liquid hazards.',
                                                                'Verify equipment configuration, '
                                                                'isolation boundaries and '
                                                                'safeguards through effective PSSR '
                                                                'and operating procedures.',
                                                                'Avoid relying exclusively on '
                                                                'administrative controls where '
                                                                'engineered overpressure '
                                                                'protection is necessary.',
                                                                'Include non-routine operating '
                                                                'scenarios in operator training '
                                                                'and process safety reviews.',
                                                                'Monitor the effectiveness of PHA, '
                                                                'MOC, PSSR and operating '
                                                                'procedures using process safety '
                                                                'performance indicators.'],
                                                    'official_sources': [{'organization': 'US CSB',
                                                                          'title': 'Williams '
                                                                                   'Olefins Plant '
                                                                                   'Explosion and '
                                                                                   'Fire',
                                                                          'url': 'https://www.csb.gov/williams-olefins-plant-explosion-and-fire-/',
                                                                          'source_type': 'official_investigation_page',
                                                                          'verified': True},
                                                                         {'organization': 'US CSB',
                                                                          'title': 'Williams '
                                                                                   'Geismar '
                                                                                   'Olefins Plant '
                                                                                   'Reboiler '
                                                                                   'Rupture and '
                                                                                   'Fire',
                                                                          'url': 'https://www.csb.gov/assets/1/6/williams_case_study_2016-10-19.pdf',
                                                                          'source_type': 'official_case_study_pdf',
                                                                          'verified': True}]},
 'ITC Deer Park Tank Farm Fire (USA, 2019)': {'schema_version': 2,
                                              'metadata': {'date': '17 March 2019',
                                                           'location': 'Deer Park, Texas, USA',
                                                           'type': 'Flammable liquid release and '
                                                                   'tank farm fire',
                                                           'fatalities': 0,
                                                           'injuries': '0 reported injuries',
                                                           'investigation_agency': 'US Chemical '
                                                                                   'Safety and '
                                                                                   'Hazard '
                                                                                   'Investigation '
                                                                                   'Board (CSB)',
                                                           'report_title': 'Intercontinental '
                                                                           'Terminals Company '
                                                                           '(ITC) Tank Fire',
                                                           'report_date': '6 July 2023'},
                                              'event_sequence': ['On 17 March 2019, a loss of '
                                                                 'containment occurred at the '
                                                                 'Intercontinental Terminals '
                                                                 'Company tank farm in Deer Park, '
                                                                 'Texas.',
                                                                 'The initiating release involved '
                                                                 'the circulation pump associated '
                                                                 'with storage Tank 80-8.',
                                                                 'A mechanical seal failure '
                                                                 'allowed butane-enriched naphtha '
                                                                 'to escape from the pump.',
                                                                 'The flammable liquid release '
                                                                 'generated hazardous vapor that '
                                                                 'subsequently ignited.',
                                                                 'The resulting fire spread '
                                                                 'through the affected tank farm '
                                                                 'containment area.',
                                                                 'The fire continued for '
                                                                 'approximately three days and '
                                                                 'destroyed 15 storage tanks.',
                                                                 'Following the fire, failure of a '
                                                                 'containment wall allowed '
                                                                 'contaminated liquid to enter '
                                                                 'nearby waterways.'],
                                              'contributing_factors': ['Inadequate mechanical '
                                                                       'integrity management of '
                                                                       'the Tank 80-8 circulation '
                                                                       'pump contributed to the '
                                                                       'loss of containment.',
                                                                       'The pump mechanical seal '
                                                                       'was vulnerable to failure '
                                                                       'under the conditions '
                                                                       'preceding the incident.',
                                                                       'Insufficient early leak '
                                                                       'detection delayed '
                                                                       'effective recognition of '
                                                                       'the hazardous release.',
                                                                       'Emergency isolation '
                                                                       'arrangements were '
                                                                       'inadequate to promptly '
                                                                       'limit the release of '
                                                                       'flammable material.',
                                                                       'The tank farm '
                                                                       'configuration permitted '
                                                                       'escalation from an initial '
                                                                       'pump fire to a multi-tank '
                                                                       'fire.',
                                                                       'Secondary containment '
                                                                       'performance was '
                                                                       'insufficient to prevent '
                                                                       'subsequent offsite '
                                                                       'contamination.'],
                                              'system_causes': ['Deficiencies in the mechanical '
                                                                'integrity program for rotating '
                                                                'equipment handling hazardous '
                                                                'materials.',
                                                                'Insufficient implementation of '
                                                                'safeguards for detecting and '
                                                                'responding to flammable '
                                                                'hydrocarbon leaks.',
                                                                'Inadequate evaluation and control '
                                                                'of major fire escalation '
                                                                'scenarios.',
                                                                'Weaknesses in emergency isolation '
                                                                'design and response capability.',
                                                                'Insufficient assessment of '
                                                                'secondary containment integrity '
                                                                'under major emergency conditions.',
                                                                'Gaps in process safety management '
                                                                'and verification of critical '
                                                                'safeguards.'],
                                              'consequences': ['No fatalities or injuries were '
                                                               'reported.',
                                                               'Fifteen storage tanks in the '
                                                               'affected containment area were '
                                                               'destroyed.',
                                                               'The tank farm fire continued for '
                                                               'approximately three days.',
                                                               'The incident caused extensive '
                                                               'damage to storage and associated '
                                                               'equipment.',
                                                               'Contaminated firewater and '
                                                               'released material entered '
                                                               'surrounding waterways following '
                                                               'containment failure.',
                                                               'The incident resulted in '
                                                               'significant environmental '
                                                               'consequences and prolonged '
                                                               'emergency response.'],
                                              'investigation_findings': ['The US Chemical Safety '
                                                                         'Board investigated the '
                                                                         'ITC Deer Park tank farm '
                                                                         'fire.',
                                                                         'The initiating loss of '
                                                                         'containment occurred at '
                                                                         'the Tank 80-8 '
                                                                         'circulation pump.',
                                                                         'Mechanical seal failure '
                                                                         'allowed a flammable '
                                                                         'butane-enriched naphtha '
                                                                         'mixture to escape.',
                                                                         'The investigation '
                                                                         'identified deficiencies '
                                                                         'in pump mechanical '
                                                                         'integrity and leak '
                                                                         'detection.',
                                                                         'The CSB identified '
                                                                         'weaknesses in emergency '
                                                                         'isolation arrangements '
                                                                         'for limiting hazardous '
                                                                         'releases.',
                                                                         'The incident '
                                                                         'demonstrated '
                                                                         'vulnerabilities in '
                                                                         'preventing escalation of '
                                                                         'tank farm fires.',
                                                                         'The investigation also '
                                                                         'addressed the '
                                                                         'consequences of '
                                                                         'secondary containment '
                                                                         'failure and '
                                                                         'environmental '
                                                                         'contamination.'],
                                              'lessons': ['Establish a risk-based mechanical '
                                                          'integrity program for circulation and '
                                                          'transfer pumps handling flammable '
                                                          'liquids.',
                                                          'Monitor pump condition, bearing health, '
                                                          'vibration, and mechanical seal '
                                                          'performance using appropriate '
                                                          'engineering criteria.',
                                                          'Install suitable hydrocarbon leak '
                                                          'detection and ensure alarms are '
                                                          'integrated with effective operator '
                                                          'response.',
                                                          'Evaluate remotely operated emergency '
                                                          'isolation valves to reduce release '
                                                          'duration during fires.',
                                                          'Review tank spacing, drainage, '
                                                          'firewater availability, foam '
                                                          'application capability, and credible '
                                                          'fire escalation scenarios.',
                                                          'Verify secondary containment integrity '
                                                          'and assess potential failure during '
                                                          'prolonged firewater accumulation.',
                                                          'Provide arrangements for controlled '
                                                          'collection and management of '
                                                          'contaminated firefighting water.',
                                                          'Include pump seal failure, delayed '
                                                          'isolation, and multi-tank fire '
                                                          'scenarios in process hazard analysis '
                                                          'and emergency response exercises.',
                                                          'Verify critical fire protection and '
                                                          'isolation safeguards through periodic '
                                                          'inspection, testing, and maintenance.'],
                                              'official_sources': [{'organization': 'US CSB',
                                                                    'title': 'Intercontinental '
                                                                             'Terminals Company '
                                                                             '(ITC) Tank Fire — '
                                                                             'Final Investigation '
                                                                             'Report',
                                                                    'url': 'https://www.csb.gov/assets/1/6/itc_report_-_final_%28july_6%2C_2023%29.pdf',
                                                                    'source_type': 'official_investigation_report',
                                                                    'verified': True},
                                                                   {'organization': 'US CSB',
                                                                    'title': 'ITC Tank Fire — '
                                                                             'Recommendation '
                                                                             'Status Summary',
                                                                    'url': 'https://www.csb.gov/assets/recommendation/Status_Change_Summary_ITC_%28ITC_R4%29_O-ARAR.pdf',
                                                                    'source_type': 'official_recommendation_record',
                                                                    'verified': True}]},
 'Jaipur Indian Oil Depot Fire (India, 2009)': {'schema_version': 2,
                                                'metadata': {'date': '29 October 2009',
                                                             'location': 'Sanganer, Jaipur, '
                                                                         'Rajasthan, India',
                                                             'type': 'Gasoline release, vapor '
                                                                     'cloud explosion and tank '
                                                                     'farm fire',
                                                             'fatalities': 11,
                                                             'injuries': '105 injuries reported by '
                                                                         'PESO',
                                                             'investigation_agency': 'Government '
                                                                                     'of India '
                                                                                     'inquiry '
                                                                                     'committee '
                                                                                     'chaired by '
                                                                                     'M. B. Lal',
                                                             'report_title': 'IOC Fire Accident '
                                                                             'Investigation Report',
                                                             'report_date': '2010'},
                                                'event_sequence': ['On 29 October 2009, Indian Oil '
                                                                   'Corporation personnel at the '
                                                                   'Jaipur POL terminal were '
                                                                   'preparing to transfer motor '
                                                                   'spirit (gasoline) to the '
                                                                   'neighbouring BPCL terminal.',
                                                                   'At approximately 6:10 PM, '
                                                                   'gasoline began escaping from '
                                                                   'the hammer blind valve '
                                                                   'associated with the Tank 401-A '
                                                                   'delivery line.',
                                                                   'The uncontrolled gasoline '
                                                                   'release generated a '
                                                                   'substantial flammable vapour '
                                                                   'cloud within the terminal.',
                                                                   'The release continued for '
                                                                   'approximately 75 minutes '
                                                                   'before ignition.',
                                                                   'The accumulated vapour cloud '
                                                                   'ignited, resulting in a major '
                                                                   'explosion and extensive fire.',
                                                                   'The fire spread through the '
                                                                   'installation and affected the '
                                                                   "terminal's 11 storage tanks.",
                                                                   'Emergency response and '
                                                                   'firefighting continued as the '
                                                                   'major fire persisted for '
                                                                   'approximately 11 days.'],
                                                'contributing_factors': ['Loss of containment '
                                                                         'occurred during '
                                                                         'preparation for gasoline '
                                                                         'transfer at the hammer '
                                                                         'blind valve.',
                                                                         'The release was not '
                                                                         'stopped promptly, '
                                                                         'allowing a substantial '
                                                                         'flammable vapour cloud '
                                                                         'to develop.',
                                                                         'Limitations in leak '
                                                                         'detection and emergency '
                                                                         'isolation contributed to '
                                                                         'the severity of the '
                                                                         'developing incident.',
                                                                         'Operating practices and '
                                                                         'procedural controls did '
                                                                         'not adequately prevent '
                                                                         'or control the major '
                                                                         'gasoline release.',
                                                                         'The accumulation of '
                                                                         'flammable vapour created '
                                                                         'conditions for a major '
                                                                         'explosion following '
                                                                         'ignition.',
                                                                         'The large hydrocarbon '
                                                                         'inventory and tank-farm '
                                                                         'configuration increased '
                                                                         'the potential for fire '
                                                                         'escalation.'],
                                                'system_causes': ['Inadequate control of major '
                                                                  'accident hazards associated '
                                                                  'with gasoline transfer and '
                                                                  'valve operations.',
                                                                  'Deficiencies in operating '
                                                                  'procedures, personnel '
                                                                  'competency and the management '
                                                                  'of abnormal operating '
                                                                  'conditions.',
                                                                  'Insufficient safeguards for '
                                                                  'rapid detection and isolation '
                                                                  'of a major flammable-liquid '
                                                                  'release.',
                                                                  'Weaknesses in hazard '
                                                                  'identification and risk '
                                                                  'assessment for credible '
                                                                  'large-release scenarios.',
                                                                  'Inadequate assurance that '
                                                                  'emergency response arrangements '
                                                                  'could control a rapidly '
                                                                  'escalating terminal fire.',
                                                                  'Insufficient integration of '
                                                                  'operational discipline, '
                                                                  'mechanical integrity and '
                                                                  'process safety management.'],
                                                'consequences': ['Eleven fatalities were recorded '
                                                                 'in the Jaipur terminal accident.',
                                                                 'The Petroleum and Explosives '
                                                                 'Safety Organisation reported 105 '
                                                                 'injuries.',
                                                                 'A major vapour cloud explosion '
                                                                 'caused extensive damage within '
                                                                 'the petroleum storage terminal.',
                                                                 'Fire affected all 11 storage '
                                                                 'tanks at the facility.',
                                                                 'The major fire continued for '
                                                                 'approximately 11 days, requiring '
                                                                 'prolonged emergency response.',
                                                                 'The incident resulted in major '
                                                                 'asset destruction, operational '
                                                                 'disruption and environmental '
                                                                 'impacts.',
                                                                 'The accident highlighted the '
                                                                 'potential for a single gasoline '
                                                                 'release to escalate into a '
                                                                 'terminal-wide major accident.'],
                                                'investigation_findings': ['The '
                                                                           'government-appointed '
                                                                           'investigation '
                                                                           'committee was chaired '
                                                                           'by M. B. Lal.',
                                                                           'The initiating event '
                                                                           'involved a major '
                                                                           'gasoline release from '
                                                                           'the hammer blind valve '
                                                                           'during transfer-line '
                                                                           'preparation.',
                                                                           'The prolonged release '
                                                                           'permitted formation of '
                                                                           'a substantial '
                                                                           'flammable vapour cloud '
                                                                           'before ignition.',
                                                                           'Deficiencies in '
                                                                           'operating procedures '
                                                                           'and operational '
                                                                           'controls were '
                                                                           'significant '
                                                                           'contributors to the '
                                                                           'incident.',
                                                                           'Emergency detection '
                                                                           'and isolation '
                                                                           'safeguards were '
                                                                           'inadequate for '
                                                                           'controlling the '
                                                                           'developing release.',
                                                                           'The investigation '
                                                                           'highlighted weaknesses '
                                                                           'in the management of '
                                                                           'major accident hazards '
                                                                           'at petroleum storage '
                                                                           'terminals.',
                                                                           'The precise ignition '
                                                                           'source should not be '
                                                                           'presented as '
                                                                           'conclusively '
                                                                           'established without '
                                                                           'specific supporting '
                                                                           'evidence.'],
                                                'lessons': ['Establish and enforce detailed '
                                                            'operating procedures for gasoline '
                                                            'transfer, line preparation and valve '
                                                            'changeover.',
                                                            'Verify valve positions, isolation '
                                                            'arrangements and transfer readiness '
                                                            'before introducing or redirecting '
                                                            'flammable liquids.',
                                                            'Provide effective hydrocarbon leak '
                                                            'detection with clear alarms and '
                                                            'prompt operator response '
                                                            'requirements.',
                                                            'Evaluate remotely operated emergency '
                                                            'isolation valves and other safeguards '
                                                            'for rapid limitation of major '
                                                            'releases.',
                                                            'Conduct process hazard analysis '
                                                            'covering large gasoline releases, '
                                                            'vapour cloud formation, explosion and '
                                                            'multi-tank fire escalation.',
                                                            'Strengthen competency assurance, '
                                                            'shift supervision, emergency drills '
                                                            'and response to abnormal operating '
                                                            'conditions.',
                                                            'Review tank-farm fire protection, '
                                                            'emergency access, firefighting '
                                                            'resources and escalation-control '
                                                            'arrangements.',
                                                            'Use management of change, mechanical '
                                                            'integrity reviews and periodic '
                                                            'process safety audits to verify '
                                                            'continuing effectiveness of '
                                                            'safeguards.'],
                                                'official_sources': [{'organization': 'Government '
                                                                                      'of India / '
                                                                                      'National '
                                                                                      'Green '
                                                                                      'Tribunal',
                                                                      'title': 'IOC Fire Accident '
                                                                               'Investigation '
                                                                               'Report',
                                                                      'url': 'https://www.greentribunal.gov.in/sites/default/files/news_updates/1724140293_pagenumber.pdf',
                                                                      'source_type': 'official_investigation_report',
                                                                      'verified': True},
                                                                     {'organization': 'Petroleum '
                                                                                      'and '
                                                                                      'Explosives '
                                                                                      'Safety '
                                                                                      'Organisation '
                                                                                      '(PESO)',
                                                                      'title': 'Annual Report '
                                                                               '2009–2010',
                                                                      'url': 'https://www.peso.gov.in/web/sites/default/files/2019-12/AR20092010.pdf',
                                                                      'source_type': 'official_annual_report',
                                                                      'verified': True},
                                                                     {'organization': 'Oil '
                                                                                      'Industry '
                                                                                      'Safety '
                                                                                      'Directorate '
                                                                                      '(OISD)',
                                                                      'title': 'Jaipur Fire '
                                                                               'Incident — Lesson '
                                                                               'Learnt',
                                                                      'url': 'https://www.oisd.gov.in/public/assets/upload/Publications/1717003432_92e45b7e87b5e2cdb0a4.pdf',
                                                                      'source_type': 'official_safety_publication',
                                                                      'verified': True}]},
'Shell Polymers Furnace Explosion and Fire (USA, 2025)': {'schema_version': 2,
                                                           'metadata': {'date': '4 June 2025',
                                                                        'location': 'Monaca, Pennsylvania, '
                                                                                    'USA',
                                                                        'type': 'Ethane cracking furnace '
                                                                                'explosion and fire',
                                                                        'fatalities': 'No fatalities '
                                                                                      'reported',
                                                                        'injuries': 'No injuries reported; '
                                                                                    '15 employees evacuated',
                                                                        'report_title': 'Furnace Explosion '
                                                                                        'and Fire at Shell '
                                                                                        'Polymers',
                                                                        'report_number': '2025-05-I-PA',
                                                                        'report_date': '16 September 2026 '
                                                                                       '(public release; '
                                                                                       'report dated '
                                                                                       'September 2026)',
                                                                        'investigation_agency': 'U.S. '
                                                                                                'Chemical '
                                                                                                'Safety and '
                                                                                                'Hazard '
                                                                                                'Investigation '
                                                                                                'Board '
                                                                                                '(CSB)'},
                                                           'event_sequence': ['Furnace 5 was returning to '
                                                                              'service after coke-trap '
                                                                              'cleaning.',
                                                                              'Opening both isolation valves '
                                                                              'allowed cracked gas to flow '
                                                                              'backward from the quench '
                                                                              'tower into the furnace.',
                                                                              'Gas contacted lit pilots, '
                                                                              'ignited, and ruptured a '
                                                                              'firebox wall.'],
                                                           'contributing_factors': ['The digital '
                                                                                    'human-machine interface '
                                                                                    '(HMI) for '
                                                                                    'motor-operated valves '
                                                                                    'made valve '
                                                                                    'identification '
                                                                                    'difficult.',
                                                                                    'A process control '
                                                                                    'engineer with limited '
                                                                                    'process knowledge '
                                                                                    'inadvertently opened a '
                                                                                    'valve.'],
                                                           'system_causes': ['Administrative measures failed '
                                                                             'to prevent the recognized '
                                                                             'backflow hazard.',
                                                                             'Available engineered backflow '
                                                                             'controls were not configured '
                                                                             'for removal of double '
                                                                             'isolation.'],
                                                           'consequences': ['The fire prompted evacuation of '
                                                                            '15 employees; the report '
                                                                            'records no injuries.',
                                                                            'Shell estimated property damage '
                                                                            'at $95 million.'],
                                                           'investigation_findings': ['The CSB identified '
                                                                                      'administrative-control '
                                                                                      'reliance and '
                                                                                      'human-machine '
                                                                                      'interface design as '
                                                                                      'key safety issues.',
                                                                                      'The investigation '
                                                                                      'linked simultaneous '
                                                                                      'isolation-valve '
                                                                                      'opening to the '
                                                                                      'backflow and '
                                                                                      'explosion.'],
                                                           'lessons': ['Use engineered protection against '
                                                                       'backflow during every furnace '
                                                                       'operating mode.',
                                                                       'Design digital valve-control '
                                                                       'interfaces to reduce selection '
                                                                       'errors.',
                                                                       'Review severe-consequence scenarios '
                                                                       'protected only by administrative '
                                                                       'measures.'],
                                                           'official_sources': [{'organization': 'U.S. '
                                                                                                 'Chemical '
                                                                                                 'Safety and '
                                                                                                 'Hazard '
                                                                                                 'Investigation '
                                                                                                 'Board '
                                                                                                 '(CSB)',
                                                                                 'title': 'Shell Polymers '
                                                                                          'investigation '
                                                                                          'overview',
                                                                                 'url': 'https://www.csb.gov/shell-polymers-furnace-explosion-and-fire/',
                                                                                 'verified': True},
                                                                                {'organization': 'U.S. '
                                                                                                 'Chemical '
                                                                                                 'Safety and '
                                                                                                 'Hazard '
                                                                                                 'Investigation '
                                                                                                 'Board '
                                                                                                 '(CSB)',
                                                                                 'title': 'Furnace Explosion '
                                                                                          'and Fire at Shell '
                                                                                          'Polymers — '
                                                                                          'investigation '
                                                                                          'report',
                                                                                 'url': 'https://www.csb.gov/file.aspx?DocumentId=6343',
                                                                                 'verified': True}],
                                                           'grounding_notes': 'This is the June 2025 Monaca '
                                                                              'event, not another Shell '
                                                                              'incident. Do not confuse the '
                                                                              'report-release year 2026 with '
                                                                              'the incident year. Omit a '
                                                                              'precise incident time because '
                                                                              'the overview and report '
                                                                              'differ. The interface '
                                                                              'deficiency concerned a '
                                                                              'digital safety-system HMI '
                                                                              'logic screen for '
                                                                              'motor-operated valves, not '
                                                                              'the physical spacing of '
                                                                              'valves or handles. Do not '
                                                                              'convert this into a '
                                                                              'physical-layout finding. '
                                                                              'Coke-trap cleaning is not '
                                                                              'established here as routine. '
                                                                              'Recommendations concern '
                                                                              'engineered backflow '
                                                                              'protection, '
                                                                              'administrative-control '
                                                                              'reliance, and digital HMI '
                                                                              'usability; do not name '
                                                                              'unassessed hardware or invent '
                                                                              'requirements. Treat lessons '
                                                                              'as recommendations, not proof '
                                                                              'that a specific historical '
                                                                              'safeguard was entirely '
                                                                              'absent. Unknown casualty '
                                                                              'information is not zero. Do '
                                                                              'not transfer '
                                                                              'hydrofluoric-acid facts from '
                                                                              'the unrelated PES prompt '
                                                                              'instructions into this case. '
                                                                              'Use only the supplied '
                                                                              'sources; do not invent '
                                                                              'report-page citations. In '
                                                                              'Major Findings, reproduce the '
                                                                              'supplied investigation '
                                                                              'findings without adding or '
                                                                              'strengthening historical '
                                                                              'claims. Do not invent '
                                                                              'equipment prescriptions, '
                                                                              'check valves, dead-leg '
                                                                              'isolation, keyed handles, '
                                                                              'universal industry claims, or '
                                                                              'mandatory requirements. '
                                                                              'Engineering interpretation '
                                                                              'must stay within the supplied '
                                                                              'lessons, be labelled as '
                                                                              'interpretation, and must not '
                                                                              'be called an official '
                                                                              'recommendation or a direct '
                                                                              'quotation. Do not label a '
                                                                              'task routine, or claim '
                                                                              'safeguards were bypassed, '
                                                                              'unless supplied information '
                                                                              'establishes that. Include the '
                                                                              'supplied official source '
                                                                              'URLs.',
                                                           'report_mode': 'source_based'},
 'Husky Energy Superior Refinery Explosion and Fire (USA, 2018)': {'schema_version': 2,
                                                                   'metadata': {'date': '26 April 2018',
                                                                                'location': 'Superior, '
                                                                                            'Wisconsin, USA',
                                                                                'type': 'FCC unit explosion '
                                                                                        'followed by asphalt '
                                                                                        'storage tank fire',
                                                                                'fatalities': 0,
                                                                                'injuries': '36 workers '
                                                                                            'sought medical '
                                                                                            'attention, '
                                                                                            'including 11 '
                                                                                            'OSHA-recordable '
                                                                                            'injuries',
                                                                                'report_title': 'FCC Unit '
                                                                                                'Explosion '
                                                                                                'and Asphalt '
                                                                                                'Fire at '
                                                                                                'Husky '
                                                                                                'Superior '
                                                                                                'Refinery',
                                                                                'report_number': '2018-02-I-WI',
                                                                                'report_date': '23 December '
                                                                                               '2022 (report '
                                                                                               'publication; '
                                                                                               'website '
                                                                                               'release 29 '
                                                                                               'December '
                                                                                               '2022)',
                                                                                'investigation_agency': 'U.S. '
                                                                                                        'Chemical '
                                                                                                        'Safety '
                                                                                                        'and '
                                                                                                        'Hazard '
                                                                                                        'Investigation '
                                                                                                        'Board '
                                                                                                        '(CSB)'},
                                                                   'event_sequence': ['The incident occurred '
                                                                                      'during a planned '
                                                                                      'fluid catalytic '
                                                                                      'cracking unit '
                                                                                      'shutdown.',
                                                                                      'Air and hydrocarbons '
                                                                                      'mixed during '
                                                                                      'shutdown, leading to '
                                                                                      'explosions in the gas '
                                                                                      'concentration '
                                                                                      'equipment.',
                                                                                      'Explosion debris '
                                                                                      'punctured an asphalt '
                                                                                      'tank; spilled asphalt '
                                                                                      'subsequently burned.'],
                                                                   'contributing_factors': ['Safeguards '
                                                                                            'separating the '
                                                                                            'air and '
                                                                                            'hydrocarbon '
                                                                                            'systems were '
                                                                                            'ineffective '
                                                                                            'during '
                                                                                            'transient '
                                                                                            'operation.',
                                                                                            'Catalyst '
                                                                                            'slide-valve '
                                                                                            'condition and '
                                                                                            'operation '
                                                                                            'required '
                                                                                            'improved '
                                                                                            'mechanical-integrity '
                                                                                            'controls.'],
                                                                   'system_causes': ['Process hazard '
                                                                                     'analysis and operating '
                                                                                     'procedures did not '
                                                                                     'adequately control '
                                                                                     'shutdown hazards.',
                                                                                     'Process knowledge and '
                                                                                     'training needed '
                                                                                     'stronger coverage of '
                                                                                     'transient operating '
                                                                                     'conditions.'],
                                                                   'consequences': ['There were no '
                                                                                    'fatalities; 36 workers '
                                                                                    'sought treatment, '
                                                                                    'including 11 '
                                                                                    'OSHA-recordable '
                                                                                    'injuries.',
                                                                                    'Husky reported '
                                                                                    'approximately $550 '
                                                                                    'million in property '
                                                                                    'damage.'],
                                                                   'investigation_findings': ['The CSB '
                                                                                              'identified '
                                                                                              'transient-operation '
                                                                                              'safeguards '
                                                                                              'and process '
                                                                                              'safety '
                                                                                              'management as '
                                                                                              'major issues.',
                                                                                              'The CSB '
                                                                                              'recommended '
                                                                                              'improved '
                                                                                              'steam '
                                                                                              'barriers, '
                                                                                              'purging, '
                                                                                              'monitoring, '
                                                                                              'and shutdown '
                                                                                              'procedures.'],
                                                                   'lessons': ['Evaluate startup, shutdown, '
                                                                               'and standby hazards '
                                                                               'explicitly.',
                                                                               'Maintain and verify '
                                                                               'air–hydrocarbon separation '
                                                                               'safeguards.',
                                                                               'Prepare responders for '
                                                                               'asphalt releases and fires.'],
                                                                   'official_sources': [{'organization': 'U.S. '
                                                                                                         'Chemical '
                                                                                                         'Safety '
                                                                                                         'and '
                                                                                                         'Hazard '
                                                                                                         'Investigation '
                                                                                                         'Board '
                                                                                                         '(CSB)',
                                                                                         'title': 'Husky '
                                                                                                  'Superior '
                                                                                                  'investigation '
                                                                                                  'overview '
                                                                                                  'and '
                                                                                                  'recommendations',
                                                                                         'url': 'https://www.csb.gov/husky-energy-superior-refinery-explosion-and-fire/',
                                                                                         'verified': True},
                                                                                        {'organization': 'U.S. '
                                                                                                         'Chemical '
                                                                                                         'Safety '
                                                                                                         'and '
                                                                                                         'Hazard '
                                                                                                         'Investigation '
                                                                                                         'Board '
                                                                                                         '(CSB)',
                                                                                         'title': 'FCC Unit '
                                                                                                  'Explosion '
                                                                                                  'and '
                                                                                                  'Asphalt '
                                                                                                  'Fire at '
                                                                                                  'Husky '
                                                                                                  'Superior '
                                                                                                  'Refinery '
                                                                                                  '— report',
                                                                                         'url': 'https://www.csb.gov/assets/1/20/husky_superior_refinery_report_2022-12-23_(1)1.pdf?16884=',
                                                                                         'verified': True}],
                                                                   'grounding_notes': 'Do not conflate 36 '
                                                                                      'people receiving '
                                                                                      'medical attention '
                                                                                      'with 11 '
                                                                                      'OSHA-recordable '
                                                                                      'injuries. Distinguish '
                                                                                      'the initial FCC '
                                                                                      'explosions from the '
                                                                                      'later asphalt fire. '
                                                                                      'Do not assert an HF '
                                                                                      'release: potential HF '
                                                                                      'escalation is not an '
                                                                                      'actual HF release. '
                                                                                      'Treat lessons as '
                                                                                      'recommendations, not '
                                                                                      'proof that a specific '
                                                                                      'historical safeguard '
                                                                                      'was entirely absent. '
                                                                                      'Unknown casualty '
                                                                                      'information is not '
                                                                                      'zero. Do not transfer '
                                                                                      'hydrofluoric-acid '
                                                                                      'facts from the '
                                                                                      'unrelated PES prompt '
                                                                                      'instructions into '
                                                                                      'this case. Use only '
                                                                                      'the supplied sources; '
                                                                                      'do not invent '
                                                                                      'report-page '
                                                                                      'citations. In Major '
                                                                                      'Findings, reproduce '
                                                                                      'the supplied '
                                                                                      'investigation '
                                                                                      'findings without '
                                                                                      'adding or '
                                                                                      'strengthening '
                                                                                      'historical claims. Do '
                                                                                      'not invent equipment '
                                                                                      'prescriptions, check '
                                                                                      'valves, dead-leg '
                                                                                      'isolation, keyed '
                                                                                      'handles, universal '
                                                                                      'industry claims, or '
                                                                                      'mandatory '
                                                                                      'requirements. '
                                                                                      'Engineering '
                                                                                      'interpretation must '
                                                                                      'stay within the '
                                                                                      'supplied lessons, be '
                                                                                      'labelled as '
                                                                                      'interpretation, and '
                                                                                      'must not be called an '
                                                                                      'official '
                                                                                      'recommendation or a '
                                                                                      'direct quotation. Do '
                                                                                      'not label a task '
                                                                                      'routine, or claim '
                                                                                      'safeguards were '
                                                                                      'bypassed, unless '
                                                                                      'supplied information '
                                                                                      'establishes that. '
                                                                                      'Include the supplied '
                                                                                      'official source URLs.',
                                                                   'report_mode': 'source_based'},
 'ExxonMobil Baton Rouge Refinery Chemical Release and Fire (USA, 2016)': {'schema_version': 2,
                                                                           'metadata': {'date': '22 November '
                                                                                                '2016',
                                                                                        'location': 'Baton '
                                                                                                    'Rouge, '
                                                                                                    'Louisiana, '
                                                                                                    'USA',
                                                                                        'type': 'Isobutane '
                                                                                                'release and '
                                                                                                'fire in a '
                                                                                                'sulfuric '
                                                                                                'acid '
                                                                                                'alkylation '
                                                                                                'unit',
                                                                                        'fatalities': 'Not '
                                                                                                      'quantified '
                                                                                                      'in '
                                                                                                      'the '
                                                                                                      'reviewed '
                                                                                                      'CSB '
                                                                                                      'source '
                                                                                                      'excerpts; '
                                                                                                      'do '
                                                                                                      'not '
                                                                                                      'infer '
                                                                                                      'zero',
                                                                                        'injuries': 'Four '
                                                                                                    'workers '
                                                                                                    'seriously '
                                                                                                    'burned; '
                                                                                                    'CSB '
                                                                                                    'overview '
                                                                                                    'also '
                                                                                                    'reports '
                                                                                                    'two '
                                                                                                    'additional '
                                                                                                    'injuries',
                                                                                        'report_title': 'Key '
                                                                                                        'Lessons '
                                                                                                        'from '
                                                                                                        'the '
                                                                                                        'ExxonMobil '
                                                                                                        'Baton '
                                                                                                        'Rouge '
                                                                                                        'Refinery '
                                                                                                        'Isobutane '
                                                                                                        'Release '
                                                                                                        'and '
                                                                                                        'Fire',
                                                                                        'report_number': '2016-02-I-LA',
                                                                                        'report_date': '18 '
                                                                                                       'September '
                                                                                                       '2017 '
                                                                                                       '(public '
                                                                                                       'release)',
                                                                                        'investigation_agency': 'U.S. '
                                                                                                                'Chemical '
                                                                                                                'Safety '
                                                                                                                'and '
                                                                                                                'Hazard '
                                                                                                                'Investigation '
                                                                                                                'Board '
                                                                                                                '(CSB)'},
                                                                           'event_sequence': ['Operators '
                                                                                              'needed to '
                                                                                              'open a spare '
                                                                                              'pump inlet '
                                                                                              'plug valve, '
                                                                                              'but its '
                                                                                              'gearbox '
                                                                                              'malfunctioned.',
                                                                                              'Gearbox '
                                                                                              'removal also '
                                                                                              'removed bolts '
                                                                                              'securing the '
                                                                                              'pressure-retaining '
                                                                                              'top-cap.',
                                                                                              'Turning the '
                                                                                              'valve stem '
                                                                                              'allowed the '
                                                                                              'valve to come '
                                                                                              'apart; '
                                                                                              'released '
                                                                                              'isobutane '
                                                                                              'formed a '
                                                                                              'cloud and '
                                                                                              'ignited.'],
                                                                           'contributing_factors': ['An '
                                                                                                    'older '
                                                                                                    'valve '
                                                                                                    'design '
                                                                                                    'connected '
                                                                                                    'the '
                                                                                                    'gearbox '
                                                                                                    'bracket '
                                                                                                    'to '
                                                                                                    'pressure-retaining '
                                                                                                    'components.',
                                                                                                    'Removing '
                                                                                                    'faulty '
                                                                                                    'gearboxes '
                                                                                                    'was '
                                                                                                    'accepted '
                                                                                                    'practice '
                                                                                                    'without '
                                                                                                    'adequate '
                                                                                                    'written '
                                                                                                    'guidance '
                                                                                                    'or '
                                                                                                    'training.'],
                                                                           'system_causes': ['Equipment-design '
                                                                                             'human factors '
                                                                                             'were not '
                                                                                             'adequately '
                                                                                             'controlled.',
                                                                                             'Procedures and '
                                                                                             'training did '
                                                                                             'not cover safe '
                                                                                             'gearbox '
                                                                                             'removal and '
                                                                                             'its hazards.'],
                                                                           'consequences': ['Four workers '
                                                                                            'sustained '
                                                                                            'serious burns; '
                                                                                            'the '
                                                                                            'investigation '
                                                                                            'overview '
                                                                                            'additionally '
                                                                                            'records two '
                                                                                            'other injuries.',
                                                                                            'ExxonMobil '
                                                                                            'estimated an '
                                                                                            'isobutane '
                                                                                            'release of '
                                                                                            '2,000 pounds.'],
                                                                           'investigation_findings': ['The '
                                                                                                      'CSB '
                                                                                                      'linked '
                                                                                                      'the '
                                                                                                      'release '
                                                                                                      'to '
                                                                                                      'unintended '
                                                                                                      'disassembly '
                                                                                                      'of '
                                                                                                      'the '
                                                                                                      'valve '
                                                                                                      'pressure '
                                                                                                      'boundary.',
                                                                                                      'Its '
                                                                                                      'safety '
                                                                                                      'bulletin '
                                                                                                      'addresses '
                                                                                                      'equipment '
                                                                                                      'design, '
                                                                                                      'human '
                                                                                                      'factors, '
                                                                                                      'procedures, '
                                                                                                      'and '
                                                                                                      'training.'],
                                                                           'lessons': ['Separate actuator '
                                                                                       'maintenance '
                                                                                       'attachments from '
                                                                                       'pressure-retaining '
                                                                                       'fasteners where '
                                                                                       'practicable.',
                                                                                       'Provide '
                                                                                       'task-specific '
                                                                                       'procedures and '
                                                                                       'training for '
                                                                                       'anticipated '
                                                                                       'operating tasks.',
                                                                                       'Address recurring '
                                                                                       'equipment '
                                                                                       'malfunctions rather '
                                                                                       'than normalizing '
                                                                                       'workarounds.'],
                                                                           'official_sources': [{'organization': 'U.S. '
                                                                                                                 'Chemical '
                                                                                                                 'Safety '
                                                                                                                 'and '
                                                                                                                 'Hazard '
                                                                                                                 'Investigation '
                                                                                                                 'Board '
                                                                                                                 '(CSB)',
                                                                                                 'title': 'Baton '
                                                                                                          'Rouge '
                                                                                                          'investigation '
                                                                                                          'overview',
                                                                                                 'url': 'https://www.csb.gov/exxonmobil-baton-rouge-refinery-chemical-release-and-fire/',
                                                                                                 'verified': True},
                                                                                                {'organization': 'U.S. '
                                                                                                                 'Chemical '
                                                                                                                 'Safety '
                                                                                                                 'and '
                                                                                                                 'Hazard '
                                                                                                                 'Investigation '
                                                                                                                 'Board '
                                                                                                                 '(CSB)',
                                                                                                 'title': 'Baton '
                                                                                                          'Rouge '
                                                                                                          'safety '
                                                                                                          'bulletin',
                                                                                                 'url': 'https://www.csb.gov/file.aspx?DocumentId=6045',
                                                                                                 'verified': True}],
                                                                           'grounding_notes': 'This incident '
                                                                                              'involved '
                                                                                              'isobutane in '
                                                                                              'sulfuric acid '
                                                                                              'alkylation, '
                                                                                              'not HF '
                                                                                              'alkylation. '
                                                                                              'Four refers '
                                                                                              'to serious '
                                                                                              'burn '
                                                                                              'injuries, not '
                                                                                              'necessarily '
                                                                                              'total '
                                                                                              'injuries: the '
                                                                                              'overview also '
                                                                                              'lists two '
                                                                                              'others. The '
                                                                                              'publication '
                                                                                              'is a safety '
                                                                                              'bulletin, not '
                                                                                              'a full '
                                                                                              'investigation-report '
                                                                                              'format. Treat '
                                                                                              'lessons as '
                                                                                              'recommendations, '
                                                                                              'not proof '
                                                                                              'that a '
                                                                                              'specific '
                                                                                              'historical '
                                                                                              'safeguard was '
                                                                                              'entirely '
                                                                                              'absent. '
                                                                                              'Unknown '
                                                                                              'casualty '
                                                                                              'information '
                                                                                              'is not zero. '
                                                                                              'Do not '
                                                                                              'transfer '
                                                                                              'hydrofluoric-acid '
                                                                                              'facts from '
                                                                                              'the unrelated '
                                                                                              'PES prompt '
                                                                                              'instructions '
                                                                                              'into this '
                                                                                              'case. Use '
                                                                                              'only the '
                                                                                              'supplied '
                                                                                              'sources; do '
                                                                                              'not invent '
                                                                                              'report-page '
                                                                                              'citations. In '
                                                                                              'Major '
                                                                                              'Findings, '
                                                                                              'reproduce the '
                                                                                              'supplied '
                                                                                              'investigation '
                                                                                              'findings '
                                                                                              'without '
                                                                                              'adding or '
                                                                                              'strengthening '
                                                                                              'historical '
                                                                                              'claims. Do '
                                                                                              'not invent '
                                                                                              'equipment '
                                                                                              'prescriptions, '
                                                                                              'check valves, '
                                                                                              'dead-leg '
                                                                                              'isolation, '
                                                                                              'keyed '
                                                                                              'handles, '
                                                                                              'universal '
                                                                                              'industry '
                                                                                              'claims, or '
                                                                                              'mandatory '
                                                                                              'requirements. '
                                                                                              'Engineering '
                                                                                              'interpretation '
                                                                                              'must stay '
                                                                                              'within the '
                                                                                              'supplied '
                                                                                              'lessons, be '
                                                                                              'labelled as '
                                                                                              'interpretation, '
                                                                                              'and must not '
                                                                                              'be called an '
                                                                                              'official '
                                                                                              'recommendation '
                                                                                              'or a direct '
                                                                                              'quotation. Do '
                                                                                              'not label a '
                                                                                              'task routine, '
                                                                                              'or claim '
                                                                                              'safeguards '
                                                                                              'were '
                                                                                              'bypassed, '
                                                                                              'unless '
                                                                                              'supplied '
                                                                                              'information '
                                                                                              'establishes '
                                                                                              'that. Include '
                                                                                              'the supplied '
                                                                                              'official '
                                                                                              'source URLs.',
                                                                           'report_mode': 'source_based'},
 'Caribbean Petroleum Corporation (CAPECO) Tank Explosion and Fire (Puerto Rico, 2009)': {'schema_version': 2,
                                                                                          'metadata': {'date': '23 '
                                                                                                               'October '
                                                                                                               '2009',
                                                                                                       'location': 'Bayamón, '
                                                                                                                   'Puerto '
                                                                                                                   'Rico, '
                                                                                                                   'USA',
                                                                                                       'type': 'Gasoline '
                                                                                                               'storage '
                                                                                                               'tank '
                                                                                                               'overfill, '
                                                                                                               'vapor '
                                                                                                               'cloud '
                                                                                                               'explosion, '
                                                                                                               'and '
                                                                                                               'tank '
                                                                                                               'fires',
                                                                                                       'fatalities': 'Not '
                                                                                                                     'quantified '
                                                                                                                     'in '
                                                                                                                     'the '
                                                                                                                     'reviewed '
                                                                                                                     'CSB '
                                                                                                                     'source '
                                                                                                                     'excerpts; '
                                                                                                                     'do '
                                                                                                                     'not '
                                                                                                                     'infer '
                                                                                                                     'zero',
                                                                                                       'injuries': 'Not '
                                                                                                                   'quantified '
                                                                                                                   'in '
                                                                                                                   'the '
                                                                                                                   'reviewed '
                                                                                                                   'CSB '
                                                                                                                   'source '
                                                                                                                   'excerpts; '
                                                                                                                   'do '
                                                                                                                   'not '
                                                                                                                   'infer '
                                                                                                                   'zero',
                                                                                                       'report_title': 'Caribbean '
                                                                                                                       'Petroleum '
                                                                                                                       'Tank '
                                                                                                                       'Terminal '
                                                                                                                       'Explosion '
                                                                                                                       'and '
                                                                                                                       'Multiple '
                                                                                                                       'Tank '
                                                                                                                       'Fires',
                                                                                                       'report_number': '2010.02.I.PR',
                                                                                                       'report_date': '21 '
                                                                                                                      'October '
                                                                                                                      '2015',
                                                                                                       'investigation_agency': 'U.S. '
                                                                                                                               'Chemical '
                                                                                                                               'Safety '
                                                                                                                               'and '
                                                                                                                               'Hazard '
                                                                                                                               'Investigation '
                                                                                                                               'Board '
                                                                                                                               '(CSB)'},
                                                                                          'event_sequence': ['Gasoline '
                                                                                                             'was '
                                                                                                             'transferred '
                                                                                                             'from '
                                                                                                             'a '
                                                                                                             'ship '
                                                                                                             'into '
                                                                                                             'the '
                                                                                                             'onshore '
                                                                                                             'tank '
                                                                                                             'farm.',
                                                                                                             'A '
                                                                                                             'storage '
                                                                                                             'tank '
                                                                                                             'overflowed; '
                                                                                                             'gasoline '
                                                                                                             'spray '
                                                                                                             'formed '
                                                                                                             'a '
                                                                                                             'large '
                                                                                                             'vapor '
                                                                                                             'cloud.',
                                                                                                             'The '
                                                                                                             'cloud '
                                                                                                             'ignited '
                                                                                                             'in '
                                                                                                             'the '
                                                                                                             'wastewater '
                                                                                                             'treatment '
                                                                                                             'area, '
                                                                                                             'followed '
                                                                                                             'by '
                                                                                                             'explosions '
                                                                                                             'and '
                                                                                                             'multiple '
                                                                                                             'tank '
                                                                                                             'fires.'],
                                                                                          'contributing_factors': ['Tank-level '
                                                                                                                   'monitoring '
                                                                                                                   'was '
                                                                                                                   'unreliable.',
                                                                                                                   'Independent '
                                                                                                                   'or '
                                                                                                                   'redundant '
                                                                                                                   'overfill '
                                                                                                                   'alarms '
                                                                                                                   'and '
                                                                                                                   'safeguards '
                                                                                                                   'were '
                                                                                                                   'inadequate.'],
                                                                                          'system_causes': ['Safety '
                                                                                                            'management '
                                                                                                            'did '
                                                                                                            'not '
                                                                                                            'adequately '
                                                                                                            'control '
                                                                                                            'the '
                                                                                                            'tank-overfill '
                                                                                                            'hazard.',
                                                                                                            'The '
                                                                                                            'CSB '
                                                                                                            'identified '
                                                                                                            'gaps '
                                                                                                            'in '
                                                                                                            'regulatory '
                                                                                                            'treatment '
                                                                                                            'of '
                                                                                                            'bulk '
                                                                                                            'petroleum '
                                                                                                            'terminals '
                                                                                                            'in '
                                                                                                            'its '
                                                                                                            '2015 '
                                                                                                            'report.'],
                                                                                          'consequences': ['The '
                                                                                                           'incident '
                                                                                                           'damaged '
                                                                                                           '17 '
                                                                                                           'of '
                                                                                                           '48 '
                                                                                                           'storage '
                                                                                                           'tanks '
                                                                                                           'and '
                                                                                                           'nearby '
                                                                                                           'buildings.',
                                                                                                           'Petroleum '
                                                                                                           'and '
                                                                                                           'contaminated '
                                                                                                           'firefighting '
                                                                                                           'runoff '
                                                                                                           'affected '
                                                                                                           'soil, '
                                                                                                           'wetlands, '
                                                                                                           'and '
                                                                                                           'waterways.'],
                                                                                          'investigation_findings': ['The '
                                                                                                                     'CSB '
                                                                                                                     'found '
                                                                                                                     'inadequate '
                                                                                                                     'overfill '
                                                                                                                     'safeguards '
                                                                                                                     'at '
                                                                                                                     'the '
                                                                                                                     'terminal.',
                                                                                                                     'The '
                                                                                                                     'investigation '
                                                                                                                     'identified '
                                                                                                                     'weaknesses '
                                                                                                                     'in '
                                                                                                                     'preparation '
                                                                                                                     'for '
                                                                                                                     'multiple '
                                                                                                                     'tank '
                                                                                                                     'fires.'],
                                                                                          'lessons': ['Provide '
                                                                                                      'reliable '
                                                                                                      'tank-level '
                                                                                                      'indication '
                                                                                                      'and '
                                                                                                      'independent '
                                                                                                      'overfill '
                                                                                                      'prevention.',
                                                                                                      'Assess '
                                                                                                      'major-accident '
                                                                                                      'hazards '
                                                                                                      'at '
                                                                                                      'bulk '
                                                                                                      'storage '
                                                                                                      'terminals.',
                                                                                                      'Plan '
                                                                                                      'firefighting '
                                                                                                      'resources '
                                                                                                      'and '
                                                                                                      'control '
                                                                                                      'contaminated '
                                                                                                      'runoff.'],
                                                                                          'official_sources': [{'organization': 'U.S. '
                                                                                                                                'Chemical '
                                                                                                                                'Safety '
                                                                                                                                'and '
                                                                                                                                'Hazard '
                                                                                                                                'Investigation '
                                                                                                                                'Board '
                                                                                                                                '(CSB)',
                                                                                                                'title': 'CAPECO '
                                                                                                                         'investigation '
                                                                                                                         'overview '
                                                                                                                         'and '
                                                                                                                         'recommendations',
                                                                                                                'url': 'https://www.csb.gov/caribbean-petroleum-corporation-capeco-refinery-tank-explosion-and-fire/',
                                                                                                                'verified': True},
                                                                                                               {'organization': 'U.S. '
                                                                                                                                'Chemical '
                                                                                                                                'Safety '
                                                                                                                                'and '
                                                                                                                                'Hazard '
                                                                                                                                'Investigation '
                                                                                                                                'Board '
                                                                                                                                '(CSB)',
                                                                                                                'title': 'CAPECO '
                                                                                                                         'final '
                                                                                                                         'investigation '
                                                                                                                         'report',
                                                                                                                'url': 'https://www.csb.gov/file.aspx?DocumentId=5965',
                                                                                                                'verified': True}],
                                                                                          'grounding_notes': 'The '
                                                                                                             'facility '
                                                                                                             'operated '
                                                                                                             'as '
                                                                                                             'a '
                                                                                                             'storage '
                                                                                                             'terminal '
                                                                                                             'at '
                                                                                                             'the '
                                                                                                             'incident '
                                                                                                             'date; '
                                                                                                             'the '
                                                                                                             'legacy '
                                                                                                             'CSB '
                                                                                                             'page '
                                                                                                             'title '
                                                                                                             'includes '
                                                                                                             'refinery. '
                                                                                                             'Do '
                                                                                                             'not '
                                                                                                             'import '
                                                                                                             'Buncefield '
                                                                                                             'casualty '
                                                                                                             'numbers '
                                                                                                             'from '
                                                                                                             'the '
                                                                                                             'comparison '
                                                                                                             'section '
                                                                                                             'of '
                                                                                                             'the '
                                                                                                             'CAPECO '
                                                                                                             'report. '
                                                                                                             'Regulatory '
                                                                                                             'findings '
                                                                                                             'describe '
                                                                                                             'the '
                                                                                                             '2015 '
                                                                                                             'report '
                                                                                                             'context, '
                                                                                                             'not '
                                                                                                             'current '
                                                                                                             'law. '
                                                                                                             'Treat '
                                                                                                             'lessons '
                                                                                                             'as '
                                                                                                             'recommendations, '
                                                                                                             'not '
                                                                                                             'proof '
                                                                                                             'that '
                                                                                                             'a '
                                                                                                             'specific '
                                                                                                             'historical '
                                                                                                             'safeguard '
                                                                                                             'was '
                                                                                                             'entirely '
                                                                                                             'absent. '
                                                                                                             'Unknown '
                                                                                                             'casualty '
                                                                                                             'information '
                                                                                                             'is '
                                                                                                             'not '
                                                                                                             'zero. '
                                                                                                             'Do '
                                                                                                             'not '
                                                                                                             'transfer '
                                                                                                             'hydrofluoric-acid '
                                                                                                             'facts '
                                                                                                             'from '
                                                                                                             'the '
                                                                                                             'unrelated '
                                                                                                             'PES '
                                                                                                             'prompt '
                                                                                                             'instructions '
                                                                                                             'into '
                                                                                                             'this '
                                                                                                             'case. '
                                                                                                             'Use '
                                                                                                             'only '
                                                                                                             'the '
                                                                                                             'supplied '
                                                                                                             'sources; '
                                                                                                             'do '
                                                                                                             'not '
                                                                                                             'invent '
                                                                                                             'report-page '
                                                                                                             'citations. '
                                                                                                             'In '
                                                                                                             'Major '
                                                                                                             'Findings, '
                                                                                                             'reproduce '
                                                                                                             'the '
                                                                                                             'supplied '
                                                                                                             'investigation '
                                                                                                             'findings '
                                                                                                             'without '
                                                                                                             'adding '
                                                                                                             'or '
                                                                                                             'strengthening '
                                                                                                             'historical '
                                                                                                             'claims. '
                                                                                                             'Do '
                                                                                                             'not '
                                                                                                             'invent '
                                                                                                             'equipment '
                                                                                                             'prescriptions, '
                                                                                                             'check '
                                                                                                             'valves, '
                                                                                                             'dead-leg '
                                                                                                             'isolation, '
                                                                                                             'keyed '
                                                                                                             'handles, '
                                                                                                             'universal '
                                                                                                             'industry '
                                                                                                             'claims, '
                                                                                                             'or '
                                                                                                             'mandatory '
                                                                                                             'requirements. '
                                                                                                             'Engineering '
                                                                                                             'interpretation '
                                                                                                             'must '
                                                                                                             'stay '
                                                                                                             'within '
                                                                                                             'the '
                                                                                                             'supplied '
                                                                                                             'lessons, '
                                                                                                             'be '
                                                                                                             'labelled '
                                                                                                             'as '
                                                                                                             'interpretation, '
                                                                                                             'and '
                                                                                                             'must '
                                                                                                             'not '
                                                                                                             'be '
                                                                                                             'called '
                                                                                                             'an '
                                                                                                             'official '
                                                                                                             'recommendation '
                                                                                                             'or '
                                                                                                             'a '
                                                                                                             'direct '
                                                                                                             'quotation. '
                                                                                                             'Do '
                                                                                                             'not '
                                                                                                             'label '
                                                                                                             'a '
                                                                                                             'task '
                                                                                                             'routine, '
                                                                                                             'or '
                                                                                                             'claim '
                                                                                                             'safeguards '
                                                                                                             'were '
                                                                                                             'bypassed, '
                                                                                                             'unless '
                                                                                                             'supplied '
                                                                                                             'information '
                                                                                                             'establishes '
                                                                                                             'that. '
                                                                                                             'Include '
                                                                                                             'the '
                                                                                                             'supplied '
                                                                                                             'official '
                                                                                                             'source '
                                                                                                             'URLs.',
                                                                                          'report_mode': 'source_based'},
 'Tesoro Anacortes Refinery Fatal Explosion and Fire (USA, 2010)': {'schema_version': 2,
                                                                    'metadata': {'date': '2 April 2010',
                                                                                 'location': 'Anacortes, '
                                                                                             'Washington, '
                                                                                             'USA',
                                                                                 'type': 'Naphtha '
                                                                                         'hydrotreater heat '
                                                                                         'exchanger rupture, '
                                                                                         'explosion, and '
                                                                                         'fire',
                                                                                 'fatalities': 7,
                                                                                 'injuries': 'Seven '
                                                                                             'employees '
                                                                                             'fatally '
                                                                                             'injured; '
                                                                                             'separate '
                                                                                             'nonfatal '
                                                                                             'injury count '
                                                                                             'not '
                                                                                             'established '
                                                                                             'here',
                                                                                 'report_title': 'Catastrophic '
                                                                                                 'Rupture of '
                                                                                                 'Heat '
                                                                                                 'Exchanger '
                                                                                                 '(Seven '
                                                                                                 'Fatalities): '
                                                                                                 'Tesoro '
                                                                                                 'Anacortes '
                                                                                                 'Refinery',
                                                                                 'report_number': '2010-08-I-WA',
                                                                                 'report_date': '1 May 2014 '
                                                                                                '(approval '
                                                                                                'and '
                                                                                                'release; '
                                                                                                'report '
                                                                                                'dated May '
                                                                                                '2014)',
                                                                                 'investigation_agency': 'U.S. '
                                                                                                         'Chemical '
                                                                                                         'Safety '
                                                                                                         'and '
                                                                                                         'Hazard '
                                                                                                         'Investigation '
                                                                                                         'Board '
                                                                                                         '(CSB)'},
                                                                    'event_sequence': ['Workers were '
                                                                                       'switching a process '
                                                                                       'stream between '
                                                                                       'parallel exchanger '
                                                                                       'banks.',
                                                                                       'An in-service carbon '
                                                                                       'steel heat exchanger '
                                                                                       'ruptured after high '
                                                                                       'temperature hydrogen '
                                                                                       'attack weakened it.',
                                                                                       'The release of hot '
                                                                                       'hydrogen and naphtha '
                                                                                       'caused a fatal '
                                                                                       'explosion and fire.'],
                                                                    'contributing_factors': ['The refinery '
                                                                                             'did not '
                                                                                             'effectively '
                                                                                             'evaluate the '
                                                                                             'potential for '
                                                                                             'high '
                                                                                             'temperature '
                                                                                             'hydrogen '
                                                                                             'attack (HTHA).',
                                                                                             'Personnel were '
                                                                                             'exposed during '
                                                                                             'hazardous '
                                                                                             'nonroutine '
                                                                                             'exchanger '
                                                                                             'operations.'],
                                                                    'system_causes': ['Safeguards did not '
                                                                                      'effectively prevent '
                                                                                      'HTHA failure.',
                                                                                      'The CSB identified '
                                                                                      'deficiencies in '
                                                                                      'control of nonroutine '
                                                                                      'work and process '
                                                                                      'safety culture.'],
                                                                    'consequences': ['Seven employees were '
                                                                                     'fatally injured.',
                                                                                     'The heat exchanger '
                                                                                     'catastrophically '
                                                                                     'failed and a major '
                                                                                     'fire occurred.'],
                                                                    'investigation_findings': ['The CSB '
                                                                                               'identified '
                                                                                               'HTHA as the '
                                                                                               'exchanger '
                                                                                               'failure '
                                                                                               'mechanism.',
                                                                                               'The '
                                                                                               'investigation '
                                                                                               'called for '
                                                                                               'stronger '
                                                                                               'safeguards, '
                                                                                               'including '
                                                                                               'more '
                                                                                               'HTHA-resistant '
                                                                                               'materials.'],
                                                                    'lessons': ['Evaluate material '
                                                                                'susceptibility using actual '
                                                                                'operating conditions.',
                                                                                'Prefer effective '
                                                                                'prevention, including '
                                                                                'resistant materials, over '
                                                                                'reliance on inspection '
                                                                                'alone.',
                                                                                'Control access and exposure '
                                                                                'during hazardous nonroutine '
                                                                                'work.'],
                                                                    'official_sources': [{'organization': 'U.S. '
                                                                                                          'Chemical '
                                                                                                          'Safety '
                                                                                                          'and '
                                                                                                          'Hazard '
                                                                                                          'Investigation '
                                                                                                          'Board '
                                                                                                          '(CSB)',
                                                                                          'title': 'Tesoro '
                                                                                                   'Anacortes '
                                                                                                   'investigation '
                                                                                                   'overview',
                                                                                          'url': 'https://www.csb.gov/tesoro-anacortes-refinery-fatal-explosion-and-fire-/',
                                                                                          'verified': True},
                                                                                         {'organization': 'U.S. '
                                                                                                          'Chemical '
                                                                                                          'Safety '
                                                                                                          'and '
                                                                                                          'Hazard '
                                                                                                          'Investigation '
                                                                                                          'Board '
                                                                                                          '(CSB)',
                                                                                          'title': 'Tesoro '
                                                                                                   'Anacortes '
                                                                                                   'final '
                                                                                                   'investigation '
                                                                                                   'report',
                                                                                          'url': 'https://www.csb.gov/assets/1/7/Tesoro_Anacortes_2014-May-01.pdf',
                                                                                          'verified': True}],
                                                                    'grounding_notes': 'Distinguish heat '
                                                                                       'exchanger shell '
                                                                                       'degradation by HTHA '
                                                                                       'from tube-only '
                                                                                       'failure or ordinary '
                                                                                       'thinning. Do not '
                                                                                       'imply all seven '
                                                                                       'deaths occurred '
                                                                                       'immediately. '
                                                                                       'Historical critiques '
                                                                                       'of standards are not '
                                                                                       'statements of '
                                                                                       'current standards. '
                                                                                       'Treat lessons as '
                                                                                       'recommendations, not '
                                                                                       'proof that a '
                                                                                       'specific historical '
                                                                                       'safeguard was '
                                                                                       'entirely absent. '
                                                                                       'Unknown casualty '
                                                                                       'information is not '
                                                                                       'zero. Do not '
                                                                                       'transfer '
                                                                                       'hydrofluoric-acid '
                                                                                       'facts from the '
                                                                                       'unrelated PES prompt '
                                                                                       'instructions into '
                                                                                       'this case. Use only '
                                                                                       'the supplied '
                                                                                       'sources; do not '
                                                                                       'invent report-page '
                                                                                       'citations. In Major '
                                                                                       'Findings, reproduce '
                                                                                       'the supplied '
                                                                                       'investigation '
                                                                                       'findings without '
                                                                                       'adding or '
                                                                                       'strengthening '
                                                                                       'historical claims. '
                                                                                       'Do not invent '
                                                                                       'equipment '
                                                                                       'prescriptions, check '
                                                                                       'valves, dead-leg '
                                                                                       'isolation, keyed '
                                                                                       'handles, universal '
                                                                                       'industry claims, or '
                                                                                       'mandatory '
                                                                                       'requirements. '
                                                                                       'Engineering '
                                                                                       'interpretation must '
                                                                                       'stay within the '
                                                                                       'supplied lessons, be '
                                                                                       'labelled as '
                                                                                       'interpretation, and '
                                                                                       'must not be called '
                                                                                       'an official '
                                                                                       'recommendation or a '
                                                                                       'direct quotation. Do '
                                                                                       'not label a task '
                                                                                       'routine, or claim '
                                                                                       'safeguards were '
                                                                                       'bypassed, unless '
                                                                                       'supplied information '
                                                                                       'establishes that. '
                                                                                       'Include the supplied '
                                                                                       'official source '
                                                                                       'URLs.',
                                                                    'report_mode': 'source_based'},
 'Silver Eagle Refinery Flash Fire and Catastrophic Pipe Explosion (USA, 2009)': {'schema_version': 2,
                                                                                  'metadata': {'date': '12 '
                                                                                                       'January '
                                                                                                       '2009 '
                                                                                                       'and '
                                                                                                       '4 '
                                                                                                       'November '
                                                                                                       '2009 '
                                                                                                       '(separate '
                                                                                                       'incidents)',
                                                                                               'location': 'Woods '
                                                                                                           'Cross, '
                                                                                                           'Utah, '
                                                                                                           'USA',
                                                                                               'type': 'January '
                                                                                                       'naphtha '
                                                                                                       'tank '
                                                                                                       'flash '
                                                                                                       'fire; '
                                                                                                       'separate '
                                                                                                       'November '
                                                                                                       'hydrogen '
                                                                                                       'release '
                                                                                                       'and '
                                                                                                       'pipe '
                                                                                                       'explosion',
                                                                                               'fatalities': 'Not '
                                                                                                             'quantified '
                                                                                                             'in '
                                                                                                             'the '
                                                                                                             'reviewed '
                                                                                                             'CSB '
                                                                                                             'source '
                                                                                                             'excerpts; '
                                                                                                             'do '
                                                                                                             'not '
                                                                                                             'infer '
                                                                                                             'zero',
                                                                                               'injuries': 'January: '
                                                                                                           'four '
                                                                                                           'seriously '
                                                                                                           'burned; '
                                                                                                           'November: '
                                                                                                           'nearby '
                                                                                                           'workers '
                                                                                                           'not '
                                                                                                           'seriously '
                                                                                                           'injured '
                                                                                                           'per '
                                                                                                           'CSB '
                                                                                                           'summary',
                                                                                               'report_title': 'Silver '
                                                                                                               'Eagle '
                                                                                                               'Metallurgical '
                                                                                                               'Analysis '
                                                                                                               '(November '
                                                                                                               'incident); '
                                                                                                               'CSB '
                                                                                                               'combined '
                                                                                                               'investigation '
                                                                                                               'overview',
                                                                                               'report_date': '14 '
                                                                                                              'April '
                                                                                                              '2014 '
                                                                                                              '(technical '
                                                                                                              'report '
                                                                                                              'listed '
                                                                                                              'by '
                                                                                                              'CSB); '
                                                                                                              'investigation '
                                                                                                              'closed '
                                                                                                              '28 '
                                                                                                              'January '
                                                                                                              '2015',
                                                                                               'investigation_agency': 'U.S. '
                                                                                                                       'Chemical '
                                                                                                                       'Safety '
                                                                                                                       'and '
                                                                                                                       'Hazard '
                                                                                                                       'Investigation '
                                                                                                                       'Board '
                                                                                                                       '(CSB)'},
                                                                                  'event_sequence': ['January '
                                                                                                     '12: a '
                                                                                                     'naphtha '
                                                                                                     'tank '
                                                                                                     'released '
                                                                                                     'a '
                                                                                                     'vapor '
                                                                                                     'cloud '
                                                                                                     'that '
                                                                                                     'ignited '
                                                                                                     'in a '
                                                                                                     'flash '
                                                                                                     'fire.',
                                                                                                     'November '
                                                                                                     '4: a '
                                                                                                     'separate '
                                                                                                     '10-inch '
                                                                                                     'reactor-bottom '
                                                                                                     'pipe '
                                                                                                     'failure '
                                                                                                     'released '
                                                                                                     'hydrogen.',
                                                                                                     'The '
                                                                                                     'November '
                                                                                                     'release '
                                                                                                     'ignited '
                                                                                                     'and '
                                                                                                     'exploded, '
                                                                                                     'producing '
                                                                                                     'a '
                                                                                                     'damaging '
                                                                                                     'blast '
                                                                                                     'wave.'],
                                                                                  'contributing_factors': ['The '
                                                                                                           'November '
                                                                                                           'pipe '
                                                                                                           'had '
                                                                                                           'become '
                                                                                                           'dangerously '
                                                                                                           'thin '
                                                                                                           'from '
                                                                                                           'corrosion.',
                                                                                                           'The '
                                                                                                           'failed '
                                                                                                           'November '
                                                                                                           'component '
                                                                                                           'had '
                                                                                                           'no '
                                                                                                           'recorded '
                                                                                                           'corrosion '
                                                                                                           'inspection '
                                                                                                           'history.'],
                                                                                  'system_causes': ['The '
                                                                                                    'November '
                                                                                                    'investigation '
                                                                                                    'identified '
                                                                                                    'a gap '
                                                                                                    'in '
                                                                                                    'component-level '
                                                                                                    'mechanical '
                                                                                                    'integrity.',
                                                                                                    'The CSB '
                                                                                                    'highlighted '
                                                                                                    'the '
                                                                                                    'limits '
                                                                                                    'of '
                                                                                                    'relying '
                                                                                                    'on '
                                                                                                    'inspection '
                                                                                                    'without '
                                                                                                    'controlling '
                                                                                                    'damage '
                                                                                                    'mechanisms.'],
                                                                                  'consequences': ['The '
                                                                                                   'January '
                                                                                                   'flash '
                                                                                                   'fire '
                                                                                                   'seriously '
                                                                                                   'burned '
                                                                                                   'two '
                                                                                                   'operators '
                                                                                                   'and two '
                                                                                                   'contractors.',
                                                                                                   'The '
                                                                                                   'November '
                                                                                                   'blast '
                                                                                                   'damaged '
                                                                                                   'over 100 '
                                                                                                   'homes; '
                                                                                                   'two '
                                                                                                   'sustained '
                                                                                                   'severe '
                                                                                                   'damage.'],
                                                                                  'investigation_findings': ['The '
                                                                                                             'CSB '
                                                                                                             'commissioned '
                                                                                                             'a '
                                                                                                             'metallurgical '
                                                                                                             'examination '
                                                                                                             'of '
                                                                                                             'the '
                                                                                                             'November '
                                                                                                             'pipe '
                                                                                                             'failure.',
                                                                                                             'The '
                                                                                                             'combined '
                                                                                                             'investigation '
                                                                                                             'covers '
                                                                                                             'two '
                                                                                                             'distinct '
                                                                                                             'events, '
                                                                                                             'not '
                                                                                                             'one '
                                                                                                             'continuous '
                                                                                                             'sequence.'],
                                                                                  'lessons': ['Identify and '
                                                                                              'inspect '
                                                                                              'susceptible '
                                                                                              'piping '
                                                                                              'components.',
                                                                                              'Control '
                                                                                              'degradation '
                                                                                              'through '
                                                                                              'appropriate '
                                                                                              'design and '
                                                                                              'materials.',
                                                                                              'Consider '
                                                                                              'offsite blast '
                                                                                              'consequences '
                                                                                              'in refinery '
                                                                                              'hazard '
                                                                                              'assessments.'],
                                                                                  'official_sources': [{'organization': 'U.S. '
                                                                                                                        'Chemical '
                                                                                                                        'Safety '
                                                                                                                        'and '
                                                                                                                        'Hazard '
                                                                                                                        'Investigation '
                                                                                                                        'Board '
                                                                                                                        '(CSB)',
                                                                                                        'title': 'Silver '
                                                                                                                 'Eagle '
                                                                                                                 'combined '
                                                                                                                 'investigation '
                                                                                                                 'overview',
                                                                                                        'url': 'https://www.csb.gov/silver-eagle-refinery-flash-fire-and-explosion-and-catastrophic-pipe-explosion/',
                                                                                                        'verified': True},
                                                                                                       {'organization': 'U.S. '
                                                                                                                        'Chemical '
                                                                                                                        'Safety '
                                                                                                                        'and '
                                                                                                                        'Hazard '
                                                                                                                        'Investigation '
                                                                                                                        'Board '
                                                                                                                        '(CSB)',
                                                                                                        'title': 'CSB '
                                                                                                                 'metallurgical '
                                                                                                                 'findings '
                                                                                                                 'summary, '
                                                                                                                 '10 '
                                                                                                                 'April '
                                                                                                                 '2014',
                                                                                                        'url': 'https://www.csb.gov/-csb-releases-analysis-showing-cause-of-rupture-and-hydrogen-blast-in-2009-silver-eagle-refinery-accident-in-woods-cross-utah-pipe-walls-thinned-due-to-corrosion-that-went-uninspected-for-years-/',
                                                                                                        'verified': True}],
                                                                                  'grounding_notes': 'Always '
                                                                                                     'separate '
                                                                                                     'the '
                                                                                                     'January '
                                                                                                     'tank '
                                                                                                     'flash '
                                                                                                     'fire '
                                                                                                     'from '
                                                                                                     'the '
                                                                                                     'November '
                                                                                                     'pipe '
                                                                                                     'explosion. '
                                                                                                     'Four '
                                                                                                     'serious '
                                                                                                     'burn '
                                                                                                     'injuries '
                                                                                                     'belong '
                                                                                                     'to '
                                                                                                     'January. '
                                                                                                     'The '
                                                                                                     'metallurgical '
                                                                                                     'analysis '
                                                                                                     'concerns '
                                                                                                     'November; '
                                                                                                     'do not '
                                                                                                     'attribute '
                                                                                                     'the '
                                                                                                     'January '
                                                                                                     'mechanism '
                                                                                                     'to '
                                                                                                     'that '
                                                                                                     'analysis. '
                                                                                                     'No '
                                                                                                     'report '
                                                                                                     'number '
                                                                                                     'is '
                                                                                                     'supplied. '
                                                                                                     'Treat '
                                                                                                     'lessons '
                                                                                                     'as '
                                                                                                     'recommendations, '
                                                                                                     'not '
                                                                                                     'proof '
                                                                                                     'that a '
                                                                                                     'specific '
                                                                                                     'historical '
                                                                                                     'safeguard '
                                                                                                     'was '
                                                                                                     'entirely '
                                                                                                     'absent. '
                                                                                                     'Unknown '
                                                                                                     'casualty '
                                                                                                     'information '
                                                                                                     'is not '
                                                                                                     'zero. '
                                                                                                     'Do not '
                                                                                                     'transfer '
                                                                                                     'hydrofluoric-acid '
                                                                                                     'facts '
                                                                                                     'from '
                                                                                                     'the '
                                                                                                     'unrelated '
                                                                                                     'PES '
                                                                                                     'prompt '
                                                                                                     'instructions '
                                                                                                     'into '
                                                                                                     'this '
                                                                                                     'case. '
                                                                                                     'Use '
                                                                                                     'only '
                                                                                                     'the '
                                                                                                     'supplied '
                                                                                                     'sources; '
                                                                                                     'do not '
                                                                                                     'invent '
                                                                                                     'report-page '
                                                                                                     'citations. '
                                                                                                     'In '
                                                                                                     'Major '
                                                                                                     'Findings, '
                                                                                                     'reproduce '
                                                                                                     'the '
                                                                                                     'supplied '
                                                                                                     'investigation '
                                                                                                     'findings '
                                                                                                     'without '
                                                                                                     'adding '
                                                                                                     'or '
                                                                                                     'strengthening '
                                                                                                     'historical '
                                                                                                     'claims. '
                                                                                                     'Do not '
                                                                                                     'invent '
                                                                                                     'equipment '
                                                                                                     'prescriptions, '
                                                                                                     'check '
                                                                                                     'valves, '
                                                                                                     'dead-leg '
                                                                                                     'isolation, '
                                                                                                     'keyed '
                                                                                                     'handles, '
                                                                                                     'universal '
                                                                                                     'industry '
                                                                                                     'claims, '
                                                                                                     'or '
                                                                                                     'mandatory '
                                                                                                     'requirements. '
                                                                                                     'Engineering '
                                                                                                     'interpretation '
                                                                                                     'must '
                                                                                                     'stay '
                                                                                                     'within '
                                                                                                     'the '
                                                                                                     'supplied '
                                                                                                     'lessons, '
                                                                                                     'be '
                                                                                                     'labelled '
                                                                                                     'as '
                                                                                                     'interpretation, '
                                                                                                     'and '
                                                                                                     'must '
                                                                                                     'not be '
                                                                                                     'called '
                                                                                                     'an '
                                                                                                     'official '
                                                                                                     'recommendation '
                                                                                                     'or a '
                                                                                                     'direct '
                                                                                                     'quotation. '
                                                                                                     'Do not '
                                                                                                     'label '
                                                                                                     'a task '
                                                                                                     'routine, '
                                                                                                     'or '
                                                                                                     'claim '
                                                                                                     'safeguards '
                                                                                                     'were '
                                                                                                     'bypassed, '
                                                                                                     'unless '
                                                                                                     'supplied '
                                                                                                     'information '
                                                                                                     'establishes '
                                                                                                     'that. '
                                                                                                     'Include '
                                                                                                     'the '
                                                                                                     'supplied '
                                                                                                     'official '
                                                                                                     'source '
                                                                                                     'URLs.',
                                                                                  'report_mode': 'source_based'},
 'Tosco Avon Refinery Petroleum Naphtha Fire (USA, 1999)': {'schema_version': 2,
                                                            'metadata': {'date': '23 February 1999',
                                                                         'location': 'Martinez, California, '
                                                                                     'USA',
                                                                         'type': 'Naphtha release and fire '
                                                                                 'during piping replacement '
                                                                                 'on an operating crude unit',
                                                                         'fatalities': 4,
                                                                         'injuries': 'One worker seriously '
                                                                                     'injured, in addition '
                                                                                     'to four fatalities',
                                                                         'report_title': 'Refinery Fire '
                                                                                         'Incident: Tosco '
                                                                                         'Avon Refinery',
                                                                         'report_number': '99-014-I-CA',
                                                                         'report_date': '21 March 2001 '
                                                                                        '(Board approval)',
                                                                         'investigation_agency': 'U.S. '
                                                                                                 'Chemical '
                                                                                                 'Safety and '
                                                                                                 'Hazard '
                                                                                                 'Investigation '
                                                                                                 'Board '
                                                                                                 '(CSB)'},
                                                            'event_sequence': ['A leaking, corroded naphtha '
                                                                               'line was scheduled for '
                                                                               'replacement while the crude '
                                                                               'unit remained operating.',
                                                                               'Attempts to isolate and '
                                                                               'drain the piping were '
                                                                               'unsuccessful.',
                                                                               'During piping removal, '
                                                                               'naphtha escaped onto hot '
                                                                               'equipment and ignited, '
                                                                               'engulfing workers on the '
                                                                               'tower.'],
                                                            'contributing_factors': ['Leaking isolation and '
                                                                                     'blocked draining paths '
                                                                                     'impeded safe '
                                                                                     'preparation.',
                                                                                     'Work continued despite '
                                                                                     'unresolved isolation '
                                                                                     'and draining '
                                                                                     'problems.'],
                                                            'system_causes': ['Hazardous nonroutine '
                                                                              'maintenance lacked adequate '
                                                                              'planning and management '
                                                                              'oversight.',
                                                                              'The CSB identified weaknesses '
                                                                              'in shutdown decisions, '
                                                                              'corrosion control, and '
                                                                              'management of change.'],
                                                            'consequences': ['Four workers were killed and '
                                                                             'one was seriously injured.',
                                                                             'The fire engulfed workers '
                                                                             'positioned at different '
                                                                             'heights on the fractionator.'],
                                                            'investigation_findings': ['The CSB investigated '
                                                                                       'the February 1999 '
                                                                                       'naphtha fire.',
                                                                                       'Recommendations '
                                                                                       'addressed safe '
                                                                                       'maintenance, '
                                                                                       'management '
                                                                                       'oversight, and '
                                                                                       'corrosion '
                                                                                       'management.'],
                                                            'lessons': ['Verify isolation and draining '
                                                                        'before opening process piping.',
                                                                        'Use explicit shutdown criteria when '
                                                                        'repairs cannot be made safely '
                                                                        'online.',
                                                                        'Stop and reassess work when '
                                                                        'required safety conditions cannot '
                                                                        'be achieved.'],
                                                            'official_sources': [{'organization': 'U.S. '
                                                                                                  'Chemical '
                                                                                                  'Safety '
                                                                                                  'and '
                                                                                                  'Hazard '
                                                                                                  'Investigation '
                                                                                                  'Board '
                                                                                                  '(CSB)',
                                                                                  'title': 'Tosco Avon '
                                                                                           'investigation '
                                                                                           'overview and '
                                                                                           'recommendations',
                                                                                  'url': 'https://www.csb.gov/tosco-avon-refinery-petroleum-naphtha-fire/',
                                                                                  'verified': True},
                                                                                 {'organization': 'U.S. '
                                                                                                  'Chemical '
                                                                                                  'Safety '
                                                                                                  'and '
                                                                                                  'Hazard '
                                                                                                  'Investigation '
                                                                                                  'Board '
                                                                                                  '(CSB)',
                                                                                  'title': 'Tosco Avon final '
                                                                                           'investigation '
                                                                                           'report',
                                                                                  'url': 'https://www.csb.gov/file.aspx?DocumentId=5586',
                                                                                  'verified': True}],
                                                            'grounding_notes': 'This is the February 1999 '
                                                                               'naphtha fire, not the '
                                                                               'January 1997 hydrocracker '
                                                                               'explosion at the same '
                                                                               'refinery. Do not describe '
                                                                               'the work as safely isolated '
                                                                               'or blame ignition on hot '
                                                                               'work; the reviewed sequence '
                                                                               'involves naphtha contacting '
                                                                               'hot equipment. Treat lessons '
                                                                               'as recommendations, not '
                                                                               'proof that a specific '
                                                                               'historical safeguard was '
                                                                               'entirely absent. Unknown '
                                                                               'casualty information is not '
                                                                               'zero. Do not transfer '
                                                                               'hydrofluoric-acid facts from '
                                                                               'the unrelated PES prompt '
                                                                               'instructions into this case. '
                                                                               'Use only the supplied '
                                                                               'sources; do not invent '
                                                                               'report-page citations. In '
                                                                               'Major Findings, reproduce '
                                                                               'the supplied investigation '
                                                                               'findings without adding or '
                                                                               'strengthening historical '
                                                                               'claims. Do not invent '
                                                                               'equipment prescriptions, '
                                                                               'check valves, dead-leg '
                                                                               'isolation, keyed handles, '
                                                                               'universal industry claims, '
                                                                               'or mandatory requirements. '
                                                                               'Engineering interpretation '
                                                                               'must stay within the '
                                                                               'supplied lessons, be '
                                                                               'labelled as interpretation, '
                                                                               'and must not be called an '
                                                                               'official recommendation or a '
                                                                               'direct quotation. Do not '
                                                                               'label a task routine, or '
                                                                               'claim safeguards were '
                                                                               'bypassed, unless supplied '
                                                                               'information establishes '
                                                                               'that. Include the supplied '
                                                                               'official source URLs.',
                                                            'report_mode': 'source_based'}
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

        official_sources = accident_data.get("official_sources", [])

        verified_sources = [
            item for item in official_sources
            if isinstance(item, dict)
            and item.get("verified") is True
            and item.get("organization")
            and item.get("title")
            and item.get("url")
        ]

        sources_text = "\n".join(
            f'{number}. {item["organization"]} — '
            f'{item["title"]} — {item["url"]}'
            for number, item in enumerate(verified_sources, start=1)
        )

        sources_section = (
            "\nOFFICIAL INVESTIGATION SOURCES:\n\n"
            + sources_text
            + "\n"
            if sources_text else ""
        )

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
{sources_section}
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

        if verified_sources:
            prompt += """
OFFICIAL SOURCE REQUIREMENTS:

- Use only official source references explicitly supplied above.
- Do not invent official report URLs, titles, or document identifiers.
- Do not claim that a specific source supports a particular finding
  unless that relationship is established by verified information.
"""

        # Seveso-specific historical grounding.
        # Other accident prompts remain unchanged.
        if accident == "Seveso Chemical Accident (Italy, 1976)":
            prompt += """
ADDITIONAL SEVESO HISTORICAL ACCURACY REQUIREMENTS:

1. State only that the bursting disc ruptured as
   reactor pressure increased.

   Do not claim that reactor pressure exceeded the
   bursting-disc design setting, rated burst pressure,
   set-point, or design limit.

   The verified historical record does not establish
   the actual bursting-disc pressure setting.

   Do not infer specific historical pressure values
   or equipment design specifications from the
   fact that the bursting disc ruptured.

2. Do not claim that the relief system was designed
   or sized only for equipment protection unless
   that historical design basis is verified.

3. Describe controls for interrupted batch operations
   as inadequate. Do not assert that specific shutdown
   or restart procedures were entirely absent.

4. Do not speculate about the exact configuration
   or absence of temperature instruments, alarms,
   interlocks, or automatic shutdown systems.

5. Present modern engineering safeguards as
   recommendations, not as verified historical
   equipment deficiencies.

6. Do not invent TCDD release quantities, human
   casualty counts, investigation report numbers,
   or specific historical equipment settings.

7. Preserve the verified causal sequence:
   interrupted batch operation, uncontrolled
   exothermic reaction, temperature and pressure
   increase, bursting-disc rupture, toxic release
   containing TCDD, and off-site contamination.

8. A bursting disc is a pressure-relief device.
   Do not describe its opening as a failure to
   contain material. Distinguish its intended
   pressure-relief function from the hazardous
   consequences of discharging toxic material
   to the atmosphere.

9. Do not attribute specific investigation findings
   directly to Italian authorities or to an official
   investigation report unless that attribution is
   explicitly verified. Describe the supplied
   findings as documented accident findings.

10. Do not assert that the historical relief-system
    design lacked containment, treatment, or other
    specific equipment unless verified.

    State that the bursting-disc discharge provided
    a pathway for toxic material to reach the
    atmosphere. Present containment or treatment
    of hazardous relief discharges as a modern
    engineering recommendation.
"""

        prompt += '\nADDITIONAL OUTPUT ACCURACY REQUIREMENTS:\n\n- If abbreviating Recognized and Generally Accepted Good Engineering\n  Practices, use exactly RAGAGEP. Otherwise write the term in full.\n- Describe emergency isolation as operable from a safe location.\n  Do not add an off-site operation requirement unless explicitly\n  established by the supplied information.\n- Keep additional engineering recommendations clearly separate from\n  historical findings. Do not place an inferred or synthesized finding\n  in a column labelled as verified investigation findings.\n- Describe the initial release as process fluid containing hydrocarbons\n  and hydrofluoric acid; do not imply that hydrofluoric acid was the\n  predominant constituent unless a supplied composition establishes it.\n\nPES-SPECIFIC FINDING ACCURACY:\nFor Philadelphia Energy Solutions, preserve the distinction between:\n(a) the CSB\'s October 2022 finding that no federal requirement existed\nfor petroleum refineries to analyze and implement inherently safer\ndesign strategies; and\n(b) whether a particular facility applied inherently safer design.\nThe supplied information establishes (a), not a blanket assertion of (b).\nDo not state "inherently safer design not applied" as a verified finding.\nIn every findings summary or table, retain the historical date and\nregulatory scope of this finding. If a summary cannot preserve those\nqualifications, omit that summary row rather than strengthen the claim.\n'
        if accident_data.get("grounding_notes"):
            prompt += "\nCASE-SPECIFIC SOURCE QUALIFICATIONS:\n" + accident_data["grounding_notes"] + "\n"
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
def render_source_based_report(accident, record):
    """Render the reviewed record without AI additions or an API request."""
    labels = {
        "date": "Incident date", "location": "Location", "type": "Accident type",
        "fatalities": "Fatalities", "injuries": "Injuries",
        "investigation_agency": "Investigation agency", "report_title": "Report title",
        "report_number": "Report number", "report_date": "Report date"
    }
    lines = [f"# {accident}", "",
             "Source-based case study: this report presents the curated record without AI expansion.",
             "Unquantified information is left explicit; it must not be interpreted as zero.",
             "", "## Accident Information", "", "| Field | Value |", "|---|---|"]
    for key, value in record["metadata"].items():
        display_value = str(value).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {labels.get(key, key)} | {display_value} |")
    headings = [
        ("event_sequence", "1. Event Sequence"),
        ("contributing_factors", "2. Contributing Factors"),
        ("system_causes", "3. System and Management Causes"),
        ("consequences", "4. Effects and Consequences"),
        ("investigation_findings", "5. Investigation Findings"),
        ("lessons", "6. Lessons and Recommendations")
    ]
    for key, heading in headings:
        lines.extend(["", "## " + heading, ""])
        if key == "lessons":
            lines.extend(["These are source-informed prevention lessons; they do not assert that every listed safeguard was historically absent.", ""])
        lines.extend(f"{number}. {claim}" for number, claim in enumerate(record[key], 1))
    lines.extend(["", "## Official Investigation Sources", ""])
    for source in record.get("official_sources", []):
        lines.append(f'- [{source["organization"]} — {source["title"]}]({source["url"]})')
    lines.extend(["", "Review the cited investigation material before professional use. Historical findings do not establish current regulatory requirements."])
    return "\n".join(lines)


def analyze_accident(industry, accident):
    """
    Generates a grounded accident case study.

    The function only calls Groq when verified accident
    data is available in VERIFIED_ACCIDENT_DATA.
    """

    record = VERIFIED_ACCIDENT_DATA.get(accident)
    if isinstance(record, dict) and record.get("report_mode") == "source_based":
        return render_source_based_report(accident, record)

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

        # V2.24: Independently display verified BP investigation links.
        if "BP Texas City" in selected_accident:
            st.subheader("Official Investigation Sources")
            st.markdown(
                "1. [U.S. Chemical Safety Board — BP Texas City "
                "Investigation](https://www.csb.gov/"
                "bp-america-texas-city-refinery-explosion/)\n"
                "2. [U.S. Chemical Safety Board — Final Investigation "
                "Report (PDF)](https://www.csb.gov/assets/1/20/"
                "csbfinalreportbp.pdf)"
            )

        # V2.25: Ensure verified BP sources are in the download.
        download_answer = answer

        if "BP Texas City" in selected_accident:
            official_sources = [
                (
                    "U.S. Chemical Safety Board — BP Texas City Investigation",
                    "https://www.csb.gov/"
                    "bp-america-texas-city-refinery-explosion/"
                ),
                (
                    "U.S. Chemical Safety Board — Final Investigation Report",
                    "https://www.csb.gov/assets/1/20/"
                    "csbfinalreportbp.pdf"
                ),
            ]

            missing_sources = [
                f"- [{label}]({url})"
                for label, url in official_sources
                if url not in download_answer
            ]

            if missing_sources:
                download_answer += (
                    "\n\n## Official Investigation Sources\n\n"
                    + "\n".join(missing_sources)
                )

        st.download_button(
            label="Download Case Study as Markdown",
            data=download_answer,
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

