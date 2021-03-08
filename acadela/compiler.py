from textx import metamodel_from_str, metamodel_from_file, get_children_of_type, TextXSyntaxError
import sys, os
from os.path import join, dirname

sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\acadela_interpreter')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\exception_handler')

from acadela.acadela_interpreter.case_template import CaseInterpreter
from acadela.exception_handler.syntax_error_handler import SyntaxErrorHandler

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.

this_folder = dirname(__file__)
mm = metamodel_from_file(join(this_folder, 'CompactTreatmentPlan.tx'), classes=None, ignore_case=True)

def verifyImport(model):
    importList = model.importList
    for importStmt in importList:
        # print('import {} = get {} from {}'.format(
        #     importStmt.importVar,
        #     importStmt.objectId,
        #     importStmt.path
        # ))
        print('import {} from {}'.format(
            importStmt.importVar,
            importStmt.path
        ))
        absImportPath = this_folder + importStmt.path
        importedModel = mm.model_from_file(absImportPath)

        print (importedModel.defObj[0].object)

# model_str = """
#     define entity Discharge
#             description = 'Discharge Stage Definition'
#             multiplicity = 'exactlyOne'
# """

model_str = """
    #aca0.1
    import discharge from '/stages/discharge.aca' 
    workspace Umcg
    
    define HumanTask TestCharlson
        #manualActivate #mandatory
        description = 'Charlson Comorbidity Form'
        Form //CharlsonForm
            Field Charlson1
                #selector #mandatory
                Question = 'Do you have diabetes?'
                    Option 'No' value = '0'
                    Option 'Yes' value = '1'

            Field Charlson2
                #selector #mandatory
                Question = 'Do you have hearth attacks?'
                    Option 'No' value = '0'
                    Option 'Yes' value = '1'

    
    define case GCS1_Groningen
        prefix = 'GCS1'
        version = 1
        description = 'a obesity treatment care plan'
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional' 
            group UmcgPatients name = 'Umcg Patient' 

            user matthijs
            user williamst

        // A comment
            /* a multiline
             * Comment
             */
             
        Setting
            // description = "Case Configuration"
            CaseOwner UmcgProfessionals #exactlyOne
                description = 'case owner is UMCG Professionals'
            
            Attribute WorkplanDueDate
                #exactlyOne #date.after(TODAY)
                description = 'Workplan Due Date'
                externalId = 'dueDateConnie'
                
            CasePatient UmcgPatient #exactlyOne
                description = 'the patient of this case'
            
            Attribute EvalDueDate
                #maxOne #date.after(TODAY)
                description = 'Evaluation Due Date'
                
            Attribute MaxDoctor
                #maxOne #number(3-5)
                description = "Maximum number of doctor per patient"
                
        Trigger
            on activate invoke 'http://integration-producer:8081/v1/activate'
            on delete invoke 'http://integration-producer:8081/v1/delete'
                
        SummaryPanel
            Section BMIHeightAndWeight #left
                description = "Height and Weight of Patient"
                InfoPath Identification.MeasureBMI.Height
                InfoPath Identification.MeasureBMI.Weight
            
            Section BMIScore #center
                description = "Height and Weight of Patient"
                InfoPath Identification.MeasureBMI.BMIScore
                
        Stage AdmitPatient
            #mandatory #manualActivate
            owner = 'Settings.CaseManager'
            description = 'Admit Patient into Treatment'
            dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            externalId = 'SelectPatient'
            
            HumanTask MeasureBMI
                #mandatory
                description = 'Measure BMI score'
                owner = 'Settings.UmcgProfessionals'
                dueDateRef = 'Settings.WorkplanDueDate'
                externalId = 'HumanTask1External'
                dynamicDescriptionRef = 'Settings.PatientNumber'
                
                Trigger
                    on activate invoke 'http://integration-producer:8081/v1/activate' method Post
                
                Form //abc
                    Field Height
                        #number(0-150) #exactlyOne
                        description = 'Height of patient in cm'    
                        
                    Field Weight
                        #number(0-300) #exactlyOne
                        description = 'Weight of patient in kg'
                        
                    Field AgeRange
                        #selector #mandatory
                        Question = 'What is your age range?'
                            additionalDescription = 'age range affect BMI'
                            Option 'less than 10' value = '1'
                            Option '10-30' value = '1.2'
                            Option '30-50' value = '1.5'
                            Option 'over 50' value = '1.7'
                    
                    DynamicField BmiScore
                        #mandatory
                        description = 'BMI Calculation in kilogram and meters'
                        expression = 'Height * Height'            
                           
            AutoTask AutoTask1
                #mandatory #exactlyOne
                description = 'Automated Task 1'
                
                Trigger
                    on activate invoke 'https://server1.com/api1' method post
                
                Form 
                    Field AutoField1
                        #number(<10) #mandatory
                        description = 'AutoField1'
                
            DualTask DualTask1
                #mandatory #repeatSerial #manualActivate
                description = 'Measure Blood Pressure and inform doctor in emergency situation'
                owner = 'Settings.UmcgProfessionals'
                externalId = 'HumanTask1External'
                
                Form 
                    Field Systolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Systolic blood pressure'
                        
                    Field Diastolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Diastolic blood pressure'
                        
                    Field BloodPressureAnalysis
                        #readonly #systemDuty #number(0-300)
                        description = 'Automatically alert when blood pressure is critically high'
"""

str2="""
    #aca0.1
    //import discharge from '/stages/discharge.aca' 
    workspace Umcg
    define case GCS1_Groningen
        prefix = 'GCS1'
        version = 1
        Responsibilities
            group name = 'Umcg Physician' id = 'UmcgPhysicians'
            group name = 'Umcg Clinician' id = 'UmcgClinicians'
            group name = 'Umcg Professional' id = 'UmcgProfessionals'
            group name = 'Umcg Patient' id = 'UmcgPatients'
            
            user matthijs
            user williamst
        
        // A comment
            /* a multiline
             * Comment
             */
        
        entity CaseData
            description = 'Settings desc'
            #exactlyOne
            
            attributeList
                entity Settings
                    description = "Settings"
                    #exactlyOne
                    type = "Link.EntityDefinition.Settings"
                    
                    attributeList
                        Attribute Patient
                            description = 'Patient'
                            #exactlyOne
                            additionalDescription = 'Patient that is assigned to this case'
                            type = 'Link.Users(UmcgPatients)'
                            
                        Attribute CaseOwner
                            description = 'Case Owner'
                            #exactlyOne
                            additionalDescription = 'The owner of this case'
                            type = 'Link.Users(UmcgClinicians)'
                    endAttributeList
                    
            endAttributeList
                
            
        entity Identifications
            description = 'Identitfication desc'
            #atLeastOne
            
        CaseDefinition Leida
"""

# workspace staticId = 'c023' id = 'Lleida_Cancer'
#     define case COPD_Plan
#         multiplicity = 3
#         prefix = 'COPD1'
#         uiReference = colors(5<=green<7<red<13)

# Meta-model knows how to parse and instantiate models.
model = None

try:
    input = model_str
    if len(sys.argv) > 1:
        input = sys.argv[1];

    model = mm.model_from_str(input)
    # verifyImport(model)
    # importList = model.importList
    #
    # for importStmt in importList:
    #     print('import {} = get {} from {}'.format(
    #         importStmt.importVar,
    #         importStmt.objectId,
    #         importStmt.path
    #     ))
    #     absImportPath = this_folder + importStmt.path
    #     importedModel = mm.model_from_file(absImportPath)
    #
    #     print (importedModel.defObj[0].object)


    point_interpreter = CaseInterpreter(mm, model)

    point_interpreter.interpret()

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)


