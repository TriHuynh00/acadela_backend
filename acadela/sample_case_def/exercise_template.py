treatmentPlanStr = """
#aca0.1
import extfile.redGreenUiRef as rgu

workspace Umcg

define case Hypertension
    prefix = 'ST1'
    version = 1
    label = 'Hypertension Treatment'
    
    Responsibilities
        group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
        group UmcgClinicians name = 'Umcg Clinician'
        group UmcgProfessionals name = 'Umcg Professional' 
        group UmcgPatients name = 'Umcg Patient' 
        group UmcgNurses name = 'Umcg Nurse' 
        user williamst
        user michelf
            //user hopkinsc
            // A comment

    Setting
        CaseOwner UmcgProfessionals #exactlyOne
            label = 'UMCG Professionals'   
        Attribute WorkplanDueDate
            #exactlyOne #date.after(TODAY)
            label = 'Workplan Due Date'
            externalId = 'dueDateConnie'

        CasePatient UmcgPatients #exactlyOne
            label = 'Patient'
          
        Attribute Clinician
            #exactlyOne #Link.Users(UmcgClinicians) 
            label = 'Clinician'
      
        Attribute Nurse
            #exactlyOne #Link.Users(UmcgNurses) 
            label = 'Nurse'
            
        Attribute BloodPressureCondition
            #exactlyOne #text
            label = 'Blood Pressure Condition'

    Trigger
        On activate invoke 'http://integration-producer:8081/v1/activate'
        On complete invoke 'localhost:3001/connecare'
        
    SummaryPanel
        Section BloodPressureMeasurement #left
            label = "Systolic Pressure:"
            InfoPath Evaluation.MeasureBloodPressure.Diastolic
        Section BloodPressureDiastolicAnalysis #left
            label = "Diastolic Analysi:"
            InfoPath Evaluation.MeasureBloodPressure.DiastolicAnalysis

    Stage Identification
        #mandatory
        owner = 'Setting.CaseOwner'
        label = 'Identification'

        HumanTask SelectPatient
            #mandatory
            label = 'Assign Patient'
            dueDateRef = 'Setting.WorkplanDueDate'
            externalId = 'SelectPatient'
         
            Form PatientAssignForm
                #mandatory
                 
                InputField SelectPatient
                    #custom
                    ElementPath = "Setting.CasePatient"
                    label = "Assigned Patient"
                    
                InputField SelectDoctor
                    #custom
                    ElementPath = "Setting.Clinician"
                    label = "Assigned Clinician"
       
           Trigger
               On complete invoke 'http://127.0.0.1:3001/connecare' method post
               On complete invoke 'https://server1.com/api2' method Post with failureMessage 'Cannot complete the completion of data creation!'


    Stage Evaluation
        #mandatory
        #noRepeat
        #autoActivate
        #any
        owner = 'Setting.Clinician'
        label = 'Evaluation'
        externalId = 'EXTERNAL_ID'
        additionalDescription = 'evaluation1'
        dynamicDescriptionRef = 'Identication.SelectDoctor'
        
        Precondition
            previousStep = 'Identification'
            previousStep = 'Evaluation'
            condition = "Evaluation.RequestMedicalTest.CholesterolTest = 1"

        Precondition
            previousStep = 'Evaluation'
            condition = "Evaluation.RequestMedicalTest.CholesterolTest = 0"

        Trigger
            On activate
                invoke 'http://127.0.0.1:3001/connecare'
                method POST
                with failureMessage 'ERROR_MESSAGE'

            On terminate
                invoke 'http://127.0.0.1:3001/connecare'
                method POST
                with failureMessage 'ERROR_MESSAGE'

        HumanTask RequestMedicalTest
            #notmandatory
            #noRepeat
            #autoActivate
            #any
            owner = 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
            label = 'Request Medical Test'
            additionalDescription = 'ADDITIONAL_DESCRIPTION'
            externalId = 'EXTERNAL_ID'
            dynamicDescriptionRef = 'PATH_TO_OBJ_OF_DYNAMIC_DESCRIPTION'

            Precondition
                previousStep = 'MeasureBloodPressure'
                previousStep = 'Evaluation'
                condition = 'Setting.BloodPressureCondition = "High"'

            Precondition
                previousStep = 'Identification'
                condition = 'Setting.BloodPressureCondition = "High"'

            Trigger
                On activate
                    invoke 'http://127.0.0.1:3001/connecare'
                    method POST
                    with failureMessage 'ERROR_MESSAGE'

            Form CgiForm
                #notreadonly #mandatory
                
                InputField AgeRange
                      #singlechoice #notmandatory #notReadOnly
                      question = 'What is your age range?'
                          Option 'less than 10' value = '1'
                            additionalDescription = 'child'
                            externalId = 'childBMI'
                          Option '10-30' value = '2'
                          Option '30-50' value = '3'
                          Option 'over 50' value = '4'

                  InputField Height
                      #number(0-3) #exactlyOne
                      additionalDescription = '1m = 3.28 ft'
                      defaultValue = '0'
                      label ='Height of patient in m'
                
                  InputField Weight
                      #number(0-300) #exactlyOne
                       #mandatory
                        #notReadOnly
                        #left
                        additionalDescription = '1kg = 2.205 lbs'
                        defaultValue = '0'
                      label ='Weight of patient in kg'
                
                    OutputField BmiScore
                        #mandatory #number
                        label ='BMI Calculation in kilogram and meters'
                        expression = 'round(Weight / (Height * Height))'
                        uiRef = "colors(0 < yellow < 18 < green < 25 < orange < 30 < red < 100)"

                InputField CholesterolTest
                #singlechoice 
                    question = 'Perform Blood Cholesterol Test?'
                    Option 'No' value='0'
                    Option 'Yes' value='1'

                InputField TestField
                    #mandatory
                    #notReadOnly
                    #left
                    #maxOne
                    #noType
                    label = 'TestField'
                    additionalDescription = 'ADDITIONAL_DESCRIPTION'
                    //CustomFieldValue = 'PATH_TO_A_CASE_OBJECT'
                    uiRef = 'colors(0<red<5)'
                    externalId = 'EXTERNAL_ID'
                    defaultValue = 'DEFAULT_VALUE'
                    defaultValues = ['DEFAULT_VALUES']

                OutputField FIELDNAME
                    #mandatory
                    #notReadOnly
                    #left
                    #noType
                    label = 'OUTPUT_FIELD_LABEL'
                    additionalDescription = 'ADDITIONAL_DESCRIPTION'
                    //CustomFieldValue = 'PATH_TO_A_CASE_OBJECT'
                    uiRef = 'colors(0<green<5)'
                    expression = 'DISPLAY_OUTPUT_EXPRESSION'
                    externalId = 'EXTERNAL_ID'
                    defaultValues = ['DEFAULT_VALUES']
                    
        HumanTask MeasureBloodPressure
            #mandatory #exactlyOne
            label = 'Measure Blood Pressure'
            owner= 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
        
            Form BloodPressureForm

                InputField Diastolic
                    #number(0-300)
                    label = 'Diastolic Blood pressure (mm Hg):'
                    uiRef = 'colors(0<green<=80<yellow<=89<red<300)'


                OutputField DiastolicAnalysis
                    #left 
                    label = 'Diastolic Assessment:'
                    expression = ' if (Diastolic < 80) then "Normal"
                                    else if (Diastolic <= 89) then "Elevated" 
                                    else "High"'
                                

    Stage MedicalTest
        #mandatory
        label = 'Medical Test'        
        owner = 'Setting.Nurse'
        
        Precondition
            previousStep = 'Evaluation'
            condition = 'Evaluation.RequestMedicalTest.CholesterolTest = 1'
            
        HumanTask MeasureBloodCholesterol
            #mandatory
            owner = 'Setting.Nurse'
            label = 'Record Blood Cholesterol'    
            
            Form PrescriptionForm
                InputField CholesterolLvl
                    #text #left #mandatory
                    label = "Blood Cholesterol Level (mm/L):" 

    Stage Treatment
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Treatment'

        Precondition
            previousStep = 'Evaluation' 
            condition = 'Evaluation.RequestMedicalTest.CholesterolTest = 0' 

        HumanTask RecordPatientStatus
            #mandatory
            owner = 'Setting.Nurse'
            label = 'Record Pre-treatment Condition:'    
            
            Form PrescriptionForm
                InputField PreTreatmentNote
                    #text #left #mandatory
                    label = "Pre-treatment Note:" 

"""