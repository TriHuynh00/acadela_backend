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

input_str = r"""
    #aca0.1
    //import extfile.caseGCS1 as caseG
    import extfile.discharge as dStage
    import extfile.form as iForm
    import extfile.taskCharlsonTest
    import extfile.field
    import extfile.hook
    import extfile.redGreenUiRef as rgu
      
    workspace Umcg
    
    // define use case caseG.GCS1_Groningen
    
    define case MT1_Groningen
        prefix = 'MT1'
        version = 2
        description = 'MockTreatment'
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional' 
            group UmcgPatients name = 'Umcg Patient' 

            user matthijs
            user williamst
            user michelf

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
                
            CasePatient UmcgPatients #exactlyOne
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
                InfoPath AdmitPatient.MeasureBMI.Height
                InfoPath AdmitPatient.MeasureBMI.Weight
            
            Section BMIScore #center
                description = "Height and Weight of Patient"
                InfoPath AdmitPatient.MeasureBMI.BMIScore
        
        Stage AdmitPatient
            #mandatory
            owner = 'Setting.CaseManager'
            description = 'Admit Patient'
            //dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            //externalId = 'SelectPatient'
            
            use task TestCharlson
            
            HumanTask MeasureBMI
                #mandatory
                description = 'Measure BMI score'
                owner = 'Setting.UmcgProfessionals'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'HumanTask1External'
                dynamicDescriptionRef = 'Setting.PatientNumber'
                
                Trigger
                    use Hook hook1
                //    On activate invoke 'http://integration-producer:8081/v1/activate' method Post
                
                use Form iForm.BMIForm                              
        
        Stage Treatment
            #mandatory #manualActivate
            owner = 'Setting.CaseManager'
            description = 'Treatment'
            
            Precondition
                previousStep = 'AdmitPatient' 
            
            AutoTask RecordPatientData
                #mandatory #exactlyOne
                description = 'Record Basic Patient Info'
                
                Trigger
                    On activate 
                    invoke 'https://server1.com/api1' 
                    method Post
                    with failureMessage 'Cannot complete the data creation task!'
                
                    On complete 
                    invoke 'https://server1.com/api2' 
                    method Post
                    with failureMessage 'Cannot complete the completion of data creation!'
                
                Form RecordInfoForm
                    field AdmittedTimes
                        #number(<10) #mandatory
                        description = 'How many times have the patient been admitted to our hospitals'
                        
                    DynamicField AdtimePlus
                        #mandatory #readOnly #left #number
                        description = 'Admitted Times Plus 1'
                        
                        expression = 'AdmittedTimes + 1'
                        uiRef = use rgu.redGreenUiRef
                        externalId = 'BmiPlus'   
                    
                
            DualTask MeasureBloodPressure
                #mandatory #repeatSerial #manualActivate
                description = 'Measure Blood Pressure and inform doctor in emergency situation'
                owner = 'Setting.UmcgProfessionals'
                externalId = 'HumanTask1External'
                
                Precondition
                    previousStep = 'AdmitPatient' 
                
                Form BloodPressureForm
                    field Systolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Systolic blood pressure'
                        
                    field Diastolic 
                        #readonly #humanDuty #number(0-300)
                        description = 'Measure Diastolic blood pressure'
                        
                    field BloodPressureAnalysis
                        #readonly #systemDuty #number(0-300)
                        description = 'Automatically alert when blood pressure is critically high'
                        
        use stage dStage.Discharge
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

    runNetworkOp = True
    acaInterpreter.interpret(runNetworkOp)

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)


