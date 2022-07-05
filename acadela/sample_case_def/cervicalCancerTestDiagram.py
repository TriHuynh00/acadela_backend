treatmentPlanStr = """
workspace Umcg
    define case ST1_CervicalCancer
        prefix = 'ST1'
        version = 12
        label = 'Cervical Cancer'
        
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician'
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional' 
            group UmcgPatients name = 'Umcg Patient' 
            group UmcgNurses name = 'Umcg Nurse'
             
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
                
        SummaryPanel
            Section Risks #left
                label = "Immediate Signs for Class II?"
                InfoPath Identification.SelectPatient.PatientAge
                
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
                    
                    InputField SelectPatient
                        #custom
                        CustomFieldValue = "Setting.CasePatient"
                        label = "Assigned Patient"
                    
                    InputField PatientAge
                        #number
                        label = "Patient age"
                        
                    InputField SelectDoctor
                        #custom
                        CustomFieldValue = "Setting.Clinician"
                        label = "Assigned Clinician"
                        
        Stage CY
            #mandatory #repeatserial
            owner = 'Setting.Clinician'
            label = 'Cytological-Testing'
            
            Precondition
                previousStep = 'Identification'
                
            Precondition
                previousStep = 'CY'
                condition = '(CY.AssessCY.Colp = 2 or CY.AssessCY.Colp = 3) and Identification.SelectPatient.PatientAge < 30'
                                   
            HumanTask AssessCY
                #mandatory 
                label = 'Evaluate test results'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
            
                Form CYForm
                    InputField ColpCy
                    #singlechoice
                        question = 'Cytological testing'
                        Option 'Pap I' value='0'
                        Option 'Pap II-a' value='1'
                        Option 'Pap II-p,g' value='2'
                        Option 'Pap IIID-1' value='3'
                        Option 'Pap IIID-2' value='4'
                        Option 'Pap III-p,g' value='5'
                        Option 'Pap IV' value='6'
                        Option 'Pap V' value='7'
        Stage HPVT
            #mandatory
            owner = 'Setting.Clinician'
            label = 'HPV-Testing'
            
            Precondition
                previousStep = 'CY'
                //condition = '(CY.AssessCY.Colp = 2 or CY.AssessCY.Colp = 3) and Identification.SelectPatient.PatientAge > 29'
                condition = '(CY.AssessCY.Colp = 2 or CY.AssessCY.Colp = 3) and (Identification.SelectPatient.PatientAge >= 30 and Identification.SelectPatient.PatientAge <= 34)'
                
            Precondition
                previousStep = 'Identification'
                condition = 'Identification.SelectPatient.PatientAge >= 35'
            
                
            HumanTask AssessHPV
                #mandatory
                label = 'Evaluate test results'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
            
                Form HPVForm
                        InputField HPVResult
                        #singlechoice
                            question = 'Cytological testing'
                            Option 'Negative' value='0'
                            Option 'Positive' value='1'
        
        Stage KO
            #mandatory
            owner = 'Setting.Clinician'
            label = 'KO-Testing'
            
            //Precondition
            //    previousStep = 'Identification'
            //    condition = 'Identification.SelectPatient.PatientAge > 34'
            
            Precondition
                previousStep = 'HPVT'
                previousStep = 'CY'
                condition = 'Identification.SelectPatient.PatientAge >= 35 and ((HPVT.AssessHPV.HPV = 1 and CY.AssessCY.Colp = 0) or (HPVT.AssessHPV.HPV = 0 and CY.AssessCY.Colp = 3))'
                       
            HumanTask AssessKO
                #mandatory #exactlyOne
                label = 'Evaluate test results'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
                
                Form KOForm
                    InputField HPVKo
                    #singlechoice
                        question = 'HPV'
                        Option 'Negative' value='0'
                        Option 'Positive' value='1'
                    InputField ColpKo
                    #singlechoice
                        question = 'Cytological testing'
                        Option 'Pap I' value='0'
                        Option 'Pap II-p,g' value='2'
                        Option 'Pap IIID-1' value='3'
                        Option 'Pap IIID-2' value='4'
                        Option 'Pap III-p,g' value='5'
                        Option 'Pap IV' value='6'
                        Option 'Pap V' value='7'
    Stage KOII 
            #mandatory
            owner = 'Setting.Clinician'
            label = 'KO-Testing II'
            
            Precondition
                previousStep = 'KO'
                condition = 'KO.AssessKO.HPV = 1 and KO.AssessKO.Colp = 0 or KO.AssessKO.HPV = 0 and KO.AssessKO.Colp = 3'
           
            HumanTask AssessKOII
                #mandatory #exactlyOne
                label = 'Evaluate test results'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
                
                Form KOIIForm
                        InputField HPV
                        #singlechoice
                            question = 'HPV'
                            Option 'Negative' value='0'
                            Option 'Positive' value='1'
                        InputField Colp
                        #singlechoice
                            question = 'Cytological testing'
                            Option 'Pap I' value='0'
                            Option 'Pap II-a' value='1'
                            Option 'Pap II-p,g' value='2'
                            Option 'Pap IIID-1' value='3'
                            Option 'Pap IIID-2' value='4'
                            Option 'Pap III-p,g' value='5'
                            Option 'Pap IV' value='6'
                            Option 'Pap V' value='7'
         
    
     Stage CO
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Colposcopy'
            
            Precondition
                previousStep = 'CY'
                condition = 'CY.AssessCY.Colp = 5 or CY.AssessCY.Colp = 4 or CY.AssessCY.Colp = 6 or CY.AssessCY.Colp = 7'
            Precondition
                previousStep = 'KO'
                condition = 'KO.AssessKO.HPV = 1 and KO.AssessKO.Colp = 3 or KO.AssessKO.HPV = 1 and KO.AssessKO.Colp = 2'
            Precondition
                previousStep = 'KO'
                condition = 'KO.AssessKO.Colp = 5 or KO.AssessKO.Colp = 4 or KO.AssessKO.Colp = 6 or KO.AssessKO.Colp = 7'
            Precondition
                previousStep = 'KOII'
                condition = 'KOII.AssessKOII.HPV = 1 or KOII.AssessKOII.Colp > 2'
            Precondition
                previousStep = 'HPVT'
                condition = 'HPVT.AssessHPV.HPV = 1'
                
            HumanTask AssessCO
                #mandatory #exactlyOne
                label = 'Recommendation: Colposkopy'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
                
                Form COForm
                    InputField PSAgeRefCo
                        #custom
                        CustomFieldValue = "Identification.SelectPatient.PatientAge"
                        label = "Patient Age"
    Stage PS
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Primary Screening' 
            
            Precondition
                previousStep = 'HPVT'
                condition = 'HPVT.AssessHPV.HPV = 0 and (CY.AssessCY.Colp = 0 or CY.AssessCY.Colp = 2) and Identification.SelectPatient.PatientAge >= 35'
                
            Precondition
                previousStep = 'HPVT'
                condition = 'HPVT.AssessHPV.HPV = 0 and (CY.AssessCY.Colp = 2 or CY.AssessCY.Colp = 3) and (Identification.SelectPatient.PatientAge >= 30 and Identification.SelectPatient.PatientAge <= 34)'
                
            Precondition
                previousStep = 'CY'
                condition = '(CY.AssessCY.Colp = 0 or CY.AssessCY.Colp = 1) and Identification.SelectPatient.PatientAge < 35'
            
            Precondition
                previousStep = 'KO'
                condition = 'KO.AssessKO.HPV = 0 and (KO.AssessKO.Colp = 0 or KO.AssessKO.Colp = 2) and Identification.SelectPatient.PatientAge >= 35'       
            Precondition
                previousStep = 'KOII'
                condition = 'KOII.AssessKOII.HPV = 0 and KOII.AssessKOII.Colp < 3'
            
            HumanTask AssessPS
                #mandatory #exactlyOne
                label = 'Recommendation: Primary Screening'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'
                
                Form PSForm
                    #mandatory
                    
                    InputField PSAgeRef
                        #custom
                        CustomFieldValue = "Identification.SelectPatient.PatientAge"
                        label = "Patient Age"
                        
                    InputField NextTestRecommendation
                        #singlechoice
                            question = 'Recommended Time for the Next Test:'
                            option 'none' value = '0'
                            option 'every 3 month' value = '1'
                            option 'every 6 month' value = '2'
                            option 'every year' value = '3'
                            option 'every 3 year' value = '4'
                            option 'other' value = '5'
                            
                    InputField OtherRecommendationTime
                        #text
                        label = 'Other Recommendation Time:'
"""