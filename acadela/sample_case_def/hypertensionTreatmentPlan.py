treatmentPlanStr = """
#aca0.1
import extfile.redGreenUiRef as rgu
import extfile.prescriptionTask as prescription

workspace Umcg

define case ST1_Hypertension
    prefix = 'ST1'
    version = 8
    label = 'Hypertension Treatment'
    
    Responsibilities
        group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
        group UmcgClinicians name = 'Umcg Clinician'
        group UmcgProfessionals name = 'Umcg Professional' 
        group UmcgPatients name = 'Umcg Patient' 
        group UmcgNurses name = 'Umcg Nurse' 
            // user williamst
            //user michelf
            //user hopkinsc
    // A comment
        /* a multiline
         * Comment
         */

    Setting
        CaseOwner UmcgProfessionals #exactlyOne
            label = 'UMCG Professionals'   
            
        CasePatient UmcgPatients #exactlyOne
            label = 'Patient'
          
        Attribute Clinician
            #exactlyOne #Link.Users(UmcgClinicians) 
            label = 'Clinician'
      
        Attribute Nurse
            #exactlyOne #Link.Users(UmcgNurses) 
            label = 'Nurse'
         Attribute WorkplanDueDate
            #exactlyOne #date.after(TODAY)
            label = 'Workplan Due Date'
            externalId = 'dueDateConnie'
    
        Attribute BloodPressureCondition
            #exactlyOne #text
            label = 'Blood Pressure Condition'
    Trigger
        On activate invoke 'http://integration-producer:8081/v1/activate'
        On complete invoke 'localhost:3001/connecare'
        
    SummaryPanel
        Section BloodPressureMeasurement #left
            label = "Systolic Pressure:"
            InfoPath Evaluation.MeasureBloodPressure.Systolic

        Section Diastolic #left
            label = "Diastolic"
            InfoPath Evaluation.MeasureBloodPressure.Systolic
            
        Section DoctorNote #left
            label = "Recommendations"
            InfoPath Discharge.DischargePatient.DoctorNote

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
            
        HumanTask MeasureBloodPressure
            #mandatory #exactlyOne
            label = 'Measure Blood Pressure'
            owner= 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
            
            Form BloodPressureForm
                #mandatory
                InputField Systolic
                    #number(0-300) 
                    label = 'Systolic Blood pressure (mm Hg):'
                    uiRef = 'colors(0<green<=20<yellow<=139<red<=300)'


                OutputField SystolicAnalysis
                    #left
                    label = 'Systolic Assessment:'
                    uiRef = use rgu.redGreenUiRef
                    expression = 'if (Systolic<120) then "Normal"
                            else "High"'
                            
                            
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
                                  
                OutputField OverallAssessment
                    #left #custom
                    CustomFieldValue = "Setting.BloodPressureCondition"
                    label = 'Overall Assessment:'
                    expression = 'if (Diastolic < 80 and Systolic < 120) then "Normal"
                                  else if (Diastolic < 80 and Systolic < 130) then "Elevated" 
                                  else "High"'
            Trigger
                    On complete invoke 'http://127.0.0.1:3001/connecare' method post
                    On complete invoke 'https://server1.com/api2' method Post with failureMessage 'Cannot complete the completion of data creation!'
                    
            HumanTask RequestMedicalTest
                #notmandatory
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                label = 'Request Medical Test'
                
                Precondition
                    previousStep = 'MeasureBloodPressure'
                    condition = 'Setting.BloodPressureCondition = "High"'

                Form CgiForm
                    InputField CholesterolTest
                    #singlechoice
                        question = 'Perform Blood Cholesterol Test?'
                        Option 'No' value='0'
                        Option 'Yes' value='1'
                   // FieldEnd
                 
    Stage MedicalTest
        #mandatory
        label = 'Medical Test' 
        owner = 'Setting.Nurse'
        
        Precondition
            previousStep = 'Evaluation'
            // condition = 'Evaluation.RequestMedicalTest = 1'
            
        HumanTask MeasureBloodCholesterol
            #mandatory
            owner = 'Setting.Nurse'
            label = 'Record Blood Cholesterol'    
            
            Form PrescriptionForm
                InputField CholesterolLvl
                    #text #left #mandatory
                    label = "Blood Cholesterol Level (mm/L):" 
                // FieldEnd

    Stage Treatment
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Treatment'

        // Define two Preconditions to express the OR logic between them
        Precondition
            previousStep = 'Evaluation' 
            condition = 'Evaluation.RequestMedicalTest.CholesterolTest = 0'
        
        Precondition
            previousStep = 'MedicalTest'
            condition = 'Setting.BloodPressureCondition = "High"'
        use Task prescription.Prescribe
        
    Stage Discharge
        #mandatory #manualActivate
        owner = 'Setting.CaseOwner'
        label = 'Discharge'
        
        precondition
            previousStep = 'Identification'
        
        HumanTask DischargePatient
            #mandatory
            owner = 'Setting.CaseOwner'
            label = "Discharge Patient"
            
            Form DischargeForm
                InputField DoctorNote 
                    #text
                    label = "Post-Treatment Recommendation:"
"""