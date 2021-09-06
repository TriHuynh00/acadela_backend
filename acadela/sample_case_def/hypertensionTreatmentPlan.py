treatmentPlanStr = """
    #aca0.1
    //import extfile.form as iForm
    //import extfile.taskCharlsonTest
    //import extfile.redGreenUiRef as rgu

    workspace Umcg

    define case ST1_Hypertension
        prefix = 'ST1'
        version = 20
        label = 'Hypertension Treatment'
        
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional' 
            group UmcgPatients name = 'Umcg Patient' 


        // A comment
            /* a multiline
             * Comment
             */

        Setting
            // label = "Case Configuration"
            CaseOwner UmcgProfessionals #exactlyOne
                label = 'UMCG Professionals'

            Attribute WorkplanDueDate
                #exactlyOne #date.after(TODAY)
                label = 'Workplan Due Date'
                externalId = 'dueDateConnie'

            CasePatient UmcgPatients #exactlyOne
                label = 'CasePatient'
                
            Attribute Clinicians
                #exactlyOne #Link.Users(UmcgClinicians) 
                label = 'Clinician'

        SummaryPanel
            Section BloodPressureMeasurement #left
                label = "Systolic Pressure:"
                InfoPath Evaluation.MeasureBloodPressure.Systolic

            Section Diastolic #left
                label = "Diastolic"
                InfoPath Evaluation.MeasureBloodPressure.Diastolic 
                
            Section PrescriptionDrugName #left
                label = "Prescription Drugs"
                InfoPath Treatment.Prescription.AntihypertensiveDrug1
                InfoPath Treatment.Prescription.AntihypertensiveDrug2
                InfoPath Treatment.Prescription.AntihypertensiveDrug3
                
            Section PrescriptionDrugDose #center
                label = "Patient Comorbidities"
                InfoPath Treatment.Prescription.Comorbidities
                
            Section DoctorNote #left
                label = "Recommendations"
                InfoPath Discharge.DischargePatient.DoctorNote

        Stage AdmitPatient
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Admit Patient'

            HumanTask SelectPatient
                #mandatory
                label = 'Assign Patient'
                owner = 'Setting.CaseOwner'
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
                        CustomFieldValue = "Setting.Clinicians"
                        label = "Assigned Clinician"
                      
        Stage Evaluation
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Evaluation'
            
            Precondition
                previousStep = 'AdmitPatient'
                
            HumanTask MeasureBloodPressure
                #mandatory   
                label = 'Description of Illness'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'IllnessDescription'
                
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
                        expression = 'if (Diastolic < 80 and Systolic < 120) then "Normal"
                                      else if (Systolic < 80 and Systolic < 130) then "Elevated" 
                                      else "High"'
                
                HumanTask ExtraExamination
                    #mandatory
                    owner = 'Setting.CaseOwner'
                    dueDateRef = 'Setting.WorkplanDueDate'
                    label = 'Additional Examination'
                    
                    Form CgiForm
                        Field CgiTest
                        #singlechoice
                            question = 'Perform ECG Test?'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                        
        Stage EcgTest
            #mandatory #autoActivate
            owner = 'Setting.CaseOwner'
            label = 'ECG Test'        
            
            Precondition
                previousStep = 'Evaluation'
                condition = 'Evaluation.ExtraExamination.CgiTest>0'
                
            HumanTask MeasureECG
                #mandatory
                owner = 'Setting.CaseOwner'
                label = 'Measure ECG'    
                
                Form PrescriptionForm
                    
                    Field ECG
                        #text #left
                        label = "ECG Value:" 
    
        Stage Treatment
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Treatment'

            Precondition
                previousStep = 'Evaluation' 
                
            HumanTask Prescribe
                #mandatory #atLeastOne #repeatParallel #manualActivate
                label = 'Prescribe'
                owner = 'Setting.CaseOwner'
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
            #mandatory #manualActivate
            owner = 'Setting.CaseOwner'
            label = 'Discharge'
            
            precondition
                previousStep = 'Evaluation'
            
            HumanTask DischargePatient
                #mandatory
                owner = 'Setting.CaseOwner'
                label = "Discharge Patient"
                
                Form DischargeForm
                    Field DoctorNote 
                        #text
                        label = "Post-Treatment Recommendation:"
"""