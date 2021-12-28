treatmentPlanStr = """
#aca0.1

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

    // A comment
        /* a multiline
         * Comment
         */

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

    SummaryPanel
        Section BloodPressureMeasurement #left
            label = "Systolic Pressure:"
            InfoPath Evaluation.MeasureBloodPressure.Systolic

        Section Diastolic #left
            label = "Diastolic"
            InfoPath Evaluation.MeasureBloodPressure.Diastolic 
            
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
            owner = 'Setting.Nurse'
            dueDateRef = 'Setting.WorkplanDueDate'
            externalId = 'SelectPatient'
            
            Form PatientAssignForm
                #mandatory
                
                Field SelectPatient
                    #custom
                    CustomFieldValue = "Setting.CasePatient"
                    label = "Assigned Patient"
                    
                Field SelectDoctor
                    #custom
                    CustomFieldValue = "Setting.Clinician"
                    label = "Assigned Clinician"
                  
    Stage Evaluation
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Evaluation'
        
        Precondition
            previousStep = 'Identification'
            
        HumanTask MeasureBloodPressure
            #mandatory #exactlyOne
            label = 'Measure Blood Pressure'
            owner = 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
            
            Form BloodPressureForm
                #mandatory
                Field Systolic
                    #number(0-300)
                    label = 'Systolic Blood pressure (mm Hg):'
                    uiRef = 'colors(0<green<=120<yellow<=139<red<300)'

                Field Diastolic
                    #number(0-300)
                    label = 'Diastolic Blood pressure (mm Hg):'
                    uiRef = 'colors(0<green<=80<yellow<=89<red<300)'

                DynamicField SystolicAnalysis
                    #left
                    label = 'Systolic Assessment:'
                    expression = 'if (Systolic < 120) then "Normal"
                                  else if (Systolic < 130) then "Elevated" 
                                  else "High"'
                    
                DynamicField DiastolicAnalysis
                    #left 
                    label = 'Diastolic Assessment:'
                    expression = 'if (Diastolic < 80) then "Normal"
                                  else if (Diastolic <= 89) then "Elevated" 
                                  else "High"'
                                  
                DynamicField OverallAssessment
                    #left #custom
                    CustomFieldValue = "Setting.BloodPressureCondition"
                    label = 'Overall Assessment:'
                    
                    expression = 'if (Diastolic < 80 and Systolic < 120) then "Normal"
                                  else if (Diastolic < 80 and Systolic < 130) then "Elevated" 
                                  else "High"'
            
            HumanTask RequestMedicalTest
                #notmandatory
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                label = 'Request Medical Test'
                
                Precondition
                    previousStep = 'MeasureBloodPressure'
                
                Form CgiForm
                    Field CholesterolTest
                    #singlechoice
                        question = 'Perform Blood Cholesterol Test?'
                        Option 'No' value='0'
                        Option 'Yes' value='1'
                    
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
                Field CholesterolLvl
                    #text #left #mandatory
                    label = "Blood Cholesterol Level (mm/L):" 

    Stage Treatment
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Treatment'

        // Define two Preconditions to express the OR logic between them
        Precondition
            previousStep = 'Evaluation' 
            condition = '((Evaluation.RequestMedicalTest.CholesterolTest = 0 and Evaluation.MeasureBloodPressure.Diastolic > 130) 
                            or Evaluation.MeasureBloodPressure.Diastolic > 150)'
            //condition = 'Evaluation.RequestMedicalTest.CholesterolTest = 0'
            
        Precondition
            previousStep = 'MedicalTest'
            condition = 'Setting.BloodPressureCondition = "High"'
        
        HumanTask Prescribe
            #mandatory #repeatParallel #manualActivate
            label = 'Prescribe'
            owner = 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
            
            Form PrescriptionForm
                #mandatory
                Field AntihypertensiveDrug
                    #text #left
                    label = "Medicine Name:"
                
                Field DailyDose
                    #number #center 
                    label = "Daily Dose:"
                    
                Field Frequency
                    #number #left
                    label = "Frequency"
                
                Field FrequencyUnit
                    #text #center
                    label = "Frequency Unit"
                    
                Field Comment
                    #notmandatory #stretched
                    label = "Comment:"
                    
    Stage Discharge
        #mandatory #activateWhen('Evaluation.MeasureBloodPressure.Systolic > 100')
        owner = 'Setting.CaseOwner'
        label = 'Discharge'
        
        precondition
            previousStep = 'Identification'
        
        HumanTask DischargePatient
            #mandatory
            owner = 'Setting.CaseOwner'
            label = "Discharge Patient"
            
            Form DischargeForm
                Field DoctorNote 
                    #text
                    label = "Post-Treatment Recommendation:"
"""