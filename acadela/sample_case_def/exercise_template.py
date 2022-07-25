treatmentPlanStr = """
#aca0.1
import extfile.redGreenUiRef as rgu
import extfile.form

workspace Umcg

define case ST1_Hypertension
    prefix = 'ST1'
    version = 1
    label = 'Hypertension Treatment'
    
    Responsibilities
        group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
        group UmcgClinicians name = 'Umcg Clinician'
        group UmcgProfessionals name = 'Umcg Professional' 
        group UmcgPatients name = 'Umcg Patient' 
        group UmcgNurses name = 'Umcg Nurse' 
            //user williamst
            //user michelf
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
                    CustomFieldValue = "Setting.CasePatient"
                    label = "Assigned Patient"
                    
                InputField SelectDoctor
                    #custom
                    CustomFieldValue = "Setting.Clinician"
                    label = "Assigned Clinician"
       
           Trigger
               On complete invoke 'http://127.0.0.1:3001/connecare' method post
               On complete invoke 'https://server1.com/api2' method Post with failureMessage 'Cannot complete the completion of data creation!'


    Stage Evaluation
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Evaluation'
        
        Precondition
            previousStep = 'Identification'
            
            HumanTask RequestMedicalTest
                #notmandatory
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                label = 'Request Medical Test'
                
                Precondition
                    previousStep = 'MeasureBloodPressure'
                    previousStep = 'MeasureBloodCholesterol'
                    condition = 'Setting.BloodPressureCondition = "High"'

                Form CgiForm
                    InputField CholesterolTest
                    #singlechoice
                        question = 'Perform Blood Cholesterol Test?'
                        Option 'No' value='0'
                        Option 'Yes' value='1'

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
            
            Trigger
                On complete
                invoke 'localhost:3001/connecare' 
                method POST
            
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

        HumanTask MeasureBMI
            #mandatory
            owner = 'Setting.Nurse'
            label = 'Measure BMI'
            
            use Form BMIForm
            
    Stage BloodCholesterolTest
        #mandatory
        label = "Blood Cholesterol Test"
        owner = "Setting.Nurse"
        
        Precondition
            previousStep = "Evaluation"
            condition = "Evaluation.MeasureBloodPressure.Diastolic > 80"
            
        HumanTask TestBloodCholesterol
            label = "Test Blood Cholesterol"
            dueDateRef = "Setting.WorkplanDueDate"
            
            Form CholesterolTestForm
                InputField BloodCholesterolLvl
                    #number(1-10) #left
                    label = "Blood Cholesterol Lvl"
                    
                OutputField BloodCholesterolState
                    label = "Blood Cholesterol Condition"
                    expression = 'if (BloodCholesterolLvl < 2) then "Normal"
                                  else if (BloodCholesterolLvl < 6) then "High"
                                  else "Critical"'
                                  
            
"""