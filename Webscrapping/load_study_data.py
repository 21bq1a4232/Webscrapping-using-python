# In a Django management command file, e.g., load_study_data.py
import json
import time
from django.db import transaction
import os
from django.utils.dateparse import parse_date
import sys
from datetime import datetime
import traceback


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django

django.setup()

from myapp.models import ClinicalStudy, SponsorCollaborator, Description, Condition, Design, Intervention, ArmGroup, Outcome, Eligibility, ContactLocation, Reference, MiscInfo

def load_json_data(json_file):

        with open(json_file, 'r') as f:
            data = json.load(f)
            #print(data)
            data = data[0]
            #print(data)
            for study_info in data["studies"]:
                # try:
                    with transaction.atomic():
                            
                            # 
                            # primary_completion_date = ((study_info['protocolSection']['statusModule']['primaryCompletionDateStruct'].get('date', None)))
                            # if len(str(primary_completion_date))==7:
                            #     primary_completion_date+="-01"
                            # completion_date_str = (study_info['protocolSection']['statusModule']['completionDateStruct'].get('date', None))
                            # expanded_access=study_info['protocolSection']['statusModule']['expandedAccessInfo'].get('hasExpandedAccess', False)
                            # if expanded_access == 'false':
                            #     expanded_access = False
                            # expanded_access = False
                            if not ClinicalStudy.objects.filter(nct_id=study_info['protocolSection']['identificationModule'].get('nctId')):
                                study = ClinicalStudy.objects.create(
                                    nct_id=study_info['protocolSection']['identificationModule'].get('nctId', None),
                                    org_study_id=study_info['protocolSection']['identificationModule'].get('orgStudyIdInfo', {}).get('id', None),
                                    organization_name=study_info['protocolSection']['identificationModule']['organization'].get('fullName', None),
                                    brief_title=study_info['protocolSection']['identificationModule'].get('briefTitle', None),
                                    official_title=study_info['protocolSection']['identificationModule'].get('officialTitle', None),
                                    status=study_info['protocolSection']['statusModule'].get('overallStatus', None),
                                    status_verified_date=parse_date(study_info['protocolSection']['statusModule'].get('statusVerifiedDate', None)),
                                    expanded_access= False,#expanded_access,#study_info['protocolSection']['statusModule']['expandedAccessInfo'].get('hasExpandedAccess', False),
                                    #start_date=parse_date(study_info['protocolSection']['statusModule']['startDateStruct'].get('date', None)),
                                    primary_completion_date=parse_date('2004-09-16'),#parse_date(primary_completion_date),
                                    # completion_date = parse_date(completion_date_str + "-01") if completion_date_str and len(completion_date_str) == 7 else parse_date(completion_date_str),
                                    study_first_submit_date=parse_date(study_info['protocolSection']['statusModule'].get('studyFirstSubmitDate', None)),
                                    study_first_submit_qc_date=parse_date(study_info['protocolSection']['statusModule'].get('studyFirstSubmitQcDate', None)),
                                    study_first_post_date = parse_date(study_info['protocolSection']['statusModule']['studyFirstPostDateStruct'].get('date', None)),
                                    last_update_submit_date=parse_date(study_info['protocolSection']['statusModule'].get('lastUpdateSubmitDate', None)),
                                    last_update_post_date = parse_date(study_info['protocolSection']['statusModule']['lastUpdatePostDateStruct'].get('date', None)),
                                )

                            
                            #print(study)
                            
                                sponsor_collaborators = study_info['protocolSection']['sponsorCollaboratorsModule'].get('collaborators',[{}])
                                #print("sjrhksrjhjksrhjhrt",sponsor_collaborators)
                                for collaborator_info in sponsor_collaborators:
                                    #print(collaborator_info)
                                    SponsorCollaborator.objects.create(
                                        study=study,
                                        name=collaborator_info.get('name',"Pranav"),
                                        class_type=collaborator_info.get('class',None)
                                    )

                                #print("sponser collaborators",sponsor_collaborators)
                                
                                description_info = study_info['protocolSection']['descriptionModule']
                                Description.objects.create(
                                    study=study,
                                    brief_summary=description_info.get('briefSummary',None),
                                    detailed_description=description_info.get('detailedDescription',"NO description")
                                )
                                
                                #print(description_info)
                                
                                
                                
                                conditions = study_info['protocolSection']['conditionsModule']['conditions']
                                for condition in conditions:
                                    Condition.objects.create(study=study, condition=condition)
                                
                                #print(conditions)
                                a=None
                                design_info = study_info['protocolSection']['designModule']
                                for i in design_info:
                                    if i=='maskingInfo':
                                        if design_info['maskingInfo']:
                                            a=design_info['maskingInfo'].get('masking',None)
                                if not Design.objects.filter(study=study):
                                    try:
                                        allocation=design_info['designInfo'].get('allocation',None)
                                    except:
                                        allocation = None
                                    try:
                                        intervention_model=design_info['designInfo'].get('interventionModel',None)
                                    except:
                                        intervention_model=None
                                    try:
                                        intervention_model_description=design_info['designInfo'].get('interventionModelDescription',"no description")
                                    except:
                                        intervention_model_description = None
                                    try:
                                        
                                        primary_purpose=design_info['designInfo'].get('primaryPurpose',None)
                                    except:
                                        primary_purpose = None
                                    Design.objects.create(
                                        study=study,
                                        study_type=design_info.get('studyType',None),
                                        phases=design_info.get('phases'),  # Assuming only one phase is present
                                        allocation=allocation,
                                        intervention_model=intervention_model,
                                        intervention_model_description=intervention_model_description  ,
                                        primary_purpose = primary_purpose,
                                        masking=a,#design_info['designInfo']['maskingInfo'].get('masking',None)
                                    )

                                #print(design_info)
                                """
                                interventions = study_info['protocolSection']['armsInterventionsModule']['interventions']
                                for intervention_info in interventions:
                                    Intervention.objects.create(
                                        name=intervention_info['name'],
                                        description=intervention_info['description'],
                                        arm_group_labels=intervention_info['armGroupLabels'][0],  # Assuming only one arm group label is present
                                        other_names=intervention_info.get('otherNames',None),  # Assuming only one other name is present
                                    )

                                #print(interventions)
                                
                                arm_groups = study_info['protocolSection']['armsInterventionsModule']['armGroups']
                                for arm_group_info in arm_groups:
                                    ArmGroup.objects.create(
                                        study=study,
                                        label=arm_group_info['label'],
                                        type=arm_group_info['type'],
                                        description=arm_group_info['description']
                                    )"""

                                
                                
                                # outcomes = study_info['protocolSection']['outcomesModule']['primaryOutcomes']
                                # for outcome_info in outcomes:
                                #     Outcome.objects.create(
                                #         study=study,
                                #         measure=outcome_info.get('measure',None),
                                #         description=outcome_info.get('description','No description'),
                                #         time_frame=outcome_info['timeFrame']
                                #     )

                                
                                
                                eligibility_info = study_info['protocolSection']['eligibilityModule']
                                if not Eligibility.objects.filter(study=study):
                                    Eligibility.objects.create(
                                        study=study,
                                        #eligibility_criteria=eligibility_info['eligibilityCriteria'],
                                        healthy_volunteers=False,#eligibility_info.get('healthyVolunteers',),
                                        sex=eligibility_info.get('sex',None),
                                        minimum_age=eligibility_info.get('minimumAge','10'),
                                        maximum_age=eligibility_info.get('maximumAge','100'),
                                        stdAges=eligibility_info.get('stdAges',None),
                                    )

                                
                                # design_info = study_info['protocolSection']['designModule']
                                # for i in design_info:
                                #     if i=='maskingInfo':
                                #         if design_info['maskingInfo']:
                                #             a=design_info['maskingInfo'].get('masking',None)
                                # location_info = study_info['protocolSection']['contactsLocationsModule']['locations'][0]  # Assuming only one location is present
                                
                                # ContactLocation.objects.create(
                                #     study=study,
                                #     facility=location_info['facility'],
                                #     city=location_info['city'],
                                #     state=location_info.get('state',None),
                                #     zip_code=location_info.get('zip',None),
                                #     country=location_info['country'],
                                #     latitude=location_info['geoPoint']['lat'],
                                #     longitude=location_info['geoPoint']['lon'],
                                # )
                                
                                
                                
                                
                                # protocol_section = study_info.get('protocolSection', {})
                                # contacts_locations_module = protocol_section.get('contactsLocationsModule', {})
                                # locations = contacts_locations_module.get('locations', [])
                                # if locations:
                                #     location_info = locations[0]  # Assuming only one location is present
                                #     ContactLocation.objects.create(
                                #         study=study,
                                #         facility=location_info.get('facility', None),
                                #         city=location_info.get('city', None),
                                #         state=location_info.get('state', None),
                                #         zip_code=location_info.get('zip', None),
                                #         country=location_info.get('country', None),
                                #         latitude=location_info.get('geoPoint', {}).get('lat', None),
                                #         longitude=location_info.get('geoPoint', {}).get('lon', None),
                                #     )
                                
                                
                                # references = study_info['protocolSection']['referencesModule']['references']
                                protocol_section = study_info.get('protocolSection', {})
                                if 'referencesModule' in protocol_section:
                                    references_module = protocol_section['referencesModule'].get('references', [])
                                    for reference_info in references_module:
                                        Reference.objects.create(
                                            study=study,
                                            pmid=reference_info.get('pmid', '123456789'),
                                            type=reference_info.get('type','BACKGROUND'),
                                            citation=reference_info.get('citation',None),
                                        )

                                
                                
                                misc_info = study_info['derivedSection']['miscInfoModule']
                                MiscInfo.objects.create(
                                    study=study,
                                    version_holder=misc_info.get('versionHolder','')
                                )

                                print(f"Created study with NCT ID: {study.nct_id}")
                            
                    transaction.commit()
                    # except KeyError as e:
                    #     # print(f"KeyError: {e}. Skipping...")
                        
                    #     print(f"KeyError in {traceback.extract_tb(sys.exc_info()[2])[-1][2]}: {e}. Skipping...")
                        
                    #     continue
                    # except Exception as e:
                    #     # print(f"An error occurred: {e}. Skipping...")
                    #     print(f"An error occurred in {traceback.extract_tb(sys.exc_info()[2])[-1][2]}: {e}. Skipping...")

                    #     continue
                    # except json.JSONDecodeError as e:
                    #     print(f"Error decoding JSON response: {e}")
        


import requests
import json
import os

def fetch_data_from_urls(url_list):
    data = []
    for url in url_list:
        response = requests.get(url)
        if response.status_code == 200:
            data.append(response.json())
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    save_data_as_json(data, output_directory, output_filename,url_list)
    
    
def save_data_as_json(data, output_dir, filename,urllist):
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Data saved successfully to {output_path}")
    load_json_data("C:\\Users\\User 2\\Desktop\\alldata\\Active.json")
    if data[0].get("nextPageToken"):
        d = data[0]['nextPageToken']
        li = urllist[0]
        print(li,d)
        if '&pageToken=' not in li:
            li += '&pageToken='
            li = li + d
            print([li])
          
            
            fetch_data_from_urls([li])
        else :
            a = li.rfind('=')
            li = li[:a+1]
            li = li + d
            print([li])
           
            fetch_data_from_urls([li])
    else:
        #os.remove("current_url.json")
        exit()
    # index = li.find("pageToken=")
    # if index != -1:
    #     substring = li[index + len("pageToken="):]
    #     next_ampersand = substring.find("&")
    #     if next_ampersand == -1:
    #         updated_url = li[:index + len("pageToken=")] + d 
    #         fetch_data_from_urls(updated_url)
    #         print(updated_url,"this is innder if statemetnet")
    #     else:
    #         # If no '&' is found, replace the entire substring
    #         updated_url = li[:index + len("pageToken=")] + d + li[index + len("pageToken=") + next_ampersand:]
    #         print(updated_url,"this is inner else statmetn")
    #         fetch_data_from_urls(updated_url)
# Example list of URLs
url_list = [
    "https://clinicaltrials.gov/api/v2/studies?pageSize=1000"
]

# Directory to save JSON file
output_directory = "C:\\Users\\User 2\\Desktop\\alldata"

# Filename for the JSON file
output_filename = "Active1.json"
data = fetch_data_from_urls(url_list)

    
    

# Save data as JSON


     
     
     
