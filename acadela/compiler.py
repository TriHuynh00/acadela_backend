

import sys
import textx.scoping.providers as scoping_providers


from textx import metamodel_from_file, TextXSyntaxError
from os.path import join, dirname, abspath

sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\sacm')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\exception_handler')

from acadela.sacm.interpreter.case_template import CaseInterpreter
from acadela.sacm.exception_handler.syntax_error_handler import SyntaxErrorHandler

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.

def convert_import_path(i):
    return i.replace(".", "/") + ".aca"


this_folder = dirname(__file__)

# def verifyImport(model):
#     importList = model.importList
#     for importStmt in importList:
#         # print('import {} = get {} from {}'.format(
#         #     importStmt.importVar,
#         #     importStmt.objectId,
#         #     importStmt.path
#         # ))
#         print('import {} from {}'.format(
#             importStmt.importVar,
#             importStmt.path
#         ))
#         absImportPath = this_folder + importStmt.path
#         importedModel = mm.model_from_file(absImportPath)
#
#         print (importedModel.defObj[0].object)

# model_str = """
#     define entity Discharge
#             description = 'Discharge Stage Definition'
#             multiplicity = 'exactlyOne'
# """
input_str = r"""
    #aca0.1
    import stages.discharge as istage  
    workspace Umcg
    
    define HumanTask TestCharlson
        #manualActivate #mandatory
        description = 'Charlson Comorbidity Form'
        Form //CharlsonForm
            field Charlson1
                #selector #mandatory
                Question = 'Do you have diabetes?'
                    Option 'No' value = '0'
                    Option 'Yes' value = '1'

            field Charlson2
                #selector #mandatory
                Question = 'Do you have hearth attacks?'
                    Option 'No' value = '0'
                    Option 'Yes' value = '1'
    
    define case GCS1_Groningen
        prefix = 'GCS1'
        version = 1
        description = 'an obesity treatment care plan'
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
            On activate invoke 'http://integration-producer:8081/v1/activate'
            On delete invoke 'http://integration-producer:8081/v1/delete'
                
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
            //dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            //externalId = 'SelectPatient'
            
            HumanTask MeasureBMI
                #mandatory
                description = 'Measure BMI score'
                owner = 'Settings.UmcgProfessionals'
                dueDateRef = 'Settings.WorkplanDueDate'
                externalId = 'HumanTask1External'
                dynamicDescriptionRef = 'Settings.PatientNumber'
                
                Precondition
                    previousStep = 'PatientConsent' 
                
                Trigger
                    On activate invoke 'http://integration-producer:8081/v1/activate' method Post
                
                Form //abc
                    field Height
                        #number(0-150) #exactlyOne
                        description = 'Height of patient in cm'    
                        
                    field Weight
                        #number(0-300) #exactlyOne
                        description = 'Weight of patient in kg'
                        
                    field AgeRange
                        #selector #mandatory
                        Question = 'What is your age range?'
                            Option 'less than 10' value = '1' additionalDescription = 'child' externalId = 'childBMI'
                            Option '10-30' value = '1.2'
                            Option '30-50' value = '1.5'
                            Option 'over 50' value = '1.7'
                    
                    DynamicField BmiScore
                        #mandatory #number
                        description = 'BMI Calculation in kilogram and meters'
                        expression = 'Height * Height'
                        
                    DynamicField BmiScorePlus
                        #mandatory #readOnly #left #number
                        description = 'BMI Calculation with age counted'
                        additionalDescription = 'full Derived field'
                        expression = '(Height * Height) + Age'
                        uiRef = colors(5<red<10<green<25)
                        externalId = 'BmiPlus'                                 
        
        Stage Stage2
            #mandatory #manualActivate
            owner = 'Settings.CaseManager'
            description = 'Perform Obesity Treatment'
            
            Precondition
                previousStep = 'AdmitPatient' 
            
            AutoTask AutoTask1
                #mandatory #exactlyOne
                description = 'Automated Task 1'
                
                Trigger
                    On activate 
                    invoke 'https://server1.com/api1' 
                    method Post
                    with failureMessage 'Cannot complete the task!'
                
                    On complete 
                    invoke 'https://server1.com/api2' 
                    method Post
                    with failureMessage 'Cannot complete the task!'
                
                Form 
                    field AutoField1
                        #number(<10) #mandatory
                        description = 'AutoField1'
                
            DualTask DualTask1
                #mandatory #repeatSerial #manualActivate
                description = 'Measure Blood Pressure and inform doctor in emergency situation'
                owner = 'Settings.UmcgProfessionals'
                externalId = 'HumanTask1External'
                
                Precondition
                    previousStep = 'AdmitPatient' 
                
                Form 
                    field Systolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Systolic blood pressure'
                        
                    field Diastolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Diastolic blood pressure'
                        
                    field BloodPressureAnalysis
                        #readonly #systemDuty #number(0-300)
                        description = 'Automatically alert when blood pressure is critically high'
        
                        
"""

# workspace staticId = 'c023' id = 'Lleida_Cancer'
#     define case COPD_Plan
#         multiplicity = 3
#         prefix = 'COPD1'
#         uiReference = colors(5<=green<7<red<13)

# Meta-model knows how to parse and instantiate models.
model = None

try:
    input = input_str
    # if len(sys.argv) > 1:
    #     input = sys.argv[1];


    def importURI_to_scope_name(import_obj):
        # this method is responsible to deduce the module name in the
        # language from the importURI string
        # e.g. here: import "file.ext" --> module name "file".
        return import_obj.importURI.split('.')[0]


    def custom_scope_redirection(obj):
        from textx import textx_isinstance
        if textx_isinstance(obj, mm["Stage"]):
            if obj.ref is None:
                from textx.scoping import Postponed
                return Postponed()
            return [obj.ref]
        else:
            return []


    mm = metamodel_from_file(join(this_folder, 'CompactTreatmentPlan.tx'),
                             ignore_case=True)

    mm.register_scope_providers(
        {
            "*.*": scoping_providers\
                .FQNImportURI(importURI_converter=convert_import_path,
                          importAs=True)
        }
    )

    rootImportPath = join(abspath(dirname(__file__)), 'aa')
    print("rootImportPart", rootImportPath)
    model = mm.model_from_str(input, rootImportPath)
    # model = mm.model_from_str(input)
    acaInterpreter = CaseInterpreter(mm, model)

    acaInterpreter.interpret()

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)


