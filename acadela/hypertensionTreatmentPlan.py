treatmentPlanStr = """
    #aca0.1
    //import extfile.form as iForm
    //import extfile.taskCharlsonTest
    //import extfile.redGreenUiRef as rgu

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

            user matthijs
            user williamst
            user michelf
            user hopkinsc

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

            Attribute EvalDueDate
                #maxOne #date.after(TODAY)
                label = 'Evaluation Due Date'
                
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
            #mandatory #noRepeat
            owner = 'Setting.CaseOwner'
            label = 'Admit Patient'

            HumanTask SelectPatient
                #mandatory
                label = 'Assign Patient'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.EvalDueDate'
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
            
        Stage Treatment
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Treatment'

            Precondition
                previousStep = 'Evaluation' 
                
            HumanTask Prescription
                #mandatory 
                label = 'Prescribe Antihypertensive Drugs'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.EvalDueDate'

                Form PrescriptionForm
                    
                    Field AntihypertensiveDrug1
                        #mandatory #text #left 
                        label = "Antihypertensive medicine 1:"
                    
                    Field DailyDose1
                        #mandatory #number #center 
                        label = "Daily Dose:"
                    
                    Field AntihypertensiveDrug2
                        #notmandatory #text #left 
                        label = "Antihypertensive medicine 2:"
                        
                    Field DailyDose2
                        #number #center 
                        label = "Daily Dose:"
                        
                    Field AntihypertensiveDrug3
                        #notmandatory #text #left 
                        label = "Antihypertensive medicine 3:"
                        
                    Field DailyDose3
                        #number #center 
                        label = "Daily Dose:"
                                            
                    Field ExtraDrugs
                        #longtext #left
                        label = 'Additional Medicine'

        Stage Discharge
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Discharge'
            
            precondition
                previousStep = 'Treatment'
            
            HumanTask DischargePatient
                #mandatory
                owner = 'Setting.CaseOwner'
                label = "Discharge Patient"
                
                Form DischargeForm
                    Field DoctorNote 
                        #text
                        label = "Post-Treatment Recommendation:"
"""