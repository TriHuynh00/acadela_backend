treatmentPlanStr = """
    workspace Umcg

    define case ST1_SmokeInhalation
        prefix = 'ST1'
        version = 2
        label = 'Assessment Of Smoke Inhalation Injury'
        
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
                InfoPath EvaluationIntermediate.ImmediateRisks.ImmediateFactor1
                InfoPath EvaluationIntermediate.ImmediateRisks.ImmediateFactor2
                InfoPath EvaluationIntermediate.ImmediateRisks.ImmediateFactor3

            Section Risks #left
                label = "Potential Signs for Class II?"
                InfoPath Evaluation.AssessRisk.Factor1
                InfoPath Evaluation.AssessRisk.Factor2
                InfoPath Evaluation.AssessRisk.Factor3
                InfoPath Evaluation.AssessRisk.Factor4

            Section Risks #left
                label = "Symptoms for Class II?"
                InfoPath Sy.ASy.S1
                InfoPath Sy.ASy.S2
                InfoPath Sy.ASy.S3
                InfoPath Sy.ASy.S4
                InfoPath Sy.ASy.S5
                InfoPath Sy.ASy.S6

            Section Risks #left
                label = "Results of laryngoscopy"
                InfoPath ClassTwo.AssessClassTwo.ClTwo1
                InfoPath ClassTwo.AssessClassTwo.ClTwo2

            Section Risks #right
                label = "Actions taken for Class II diagnosed patient"
                InfoPath ClassTwoDiagnosed.AssessClassTwoDiagnosed.CLDiagnosed1
                InfoPath ClassTwoDiagnosed.AssessClassTwoDiagnosed.CLDiagnosed2
                InfoPath ClassTwoDiagnosed.AssessClassTwoDiagnosed.CLDiagnosed3

             Section Risks #right
                label = "Actions taken for Class II not diagnosed patient"
                InfoPath ClassTwoNotDiagnosed.AssessClassTwoNotDiagnosed.CLNotDiagnosed1
                InfoPath ClassTwoNotDiagnosed.AssessClassTwoNotDiagnosed.CLNotDiagnosed2
                

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
                      
        Stage EvaluationIntermediate
            #mandatory 
            owner = 'Setting.Clinician'
            label = 'Intermediate Signs'
            
            Precondition
                previousStep = 'Identification'
                
            HumanTask ImmediateRisks
                #mandatory #exactlyOne
                label = 'Assess immediate signs for smoke inhalation injury (Class II)'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'ImmediateRisks'
                
                Form ImmediateRisksForm 
                        
                        Field ImmediateFactor1
                        #singlechoice 
                            question = 'Visible burns or edema of the oropharnyx'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                        Field ImmediateFactor2
                        #singlechoice 
                            question = 'Full thickness nasolabial burns'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                        Field ImmediateFactor3
                        #singlechoice 
                            question = 'Circumfeerential neck burns'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

        Stage Evaluation
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Potential Signs'
            
            Precondition
                previousStep = 'EvaluationIntermediate'
                condition = 'EvaluationIntermediate.ImmediateRisks.ImmediateFactor1 + EvaluationIntermediate.ImmediateRisks.ImmediateFactor2 + EvaluationIntermediate.ImmediateRisks.ImmediateFactor3 = 0'
                       

            HumanTask AssessRisk
                #mandatory #exactlyOne
                label = 'Assess potential signs for smoke inhalation injury (Class II)'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessRisk'

                
                Form AssessRiskForm
                        Field Factor1
                        #singlechoice
                            question = 'Burns in a closed space'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                        Field Factor2
                        #singlechoice
                            question = 'Singed nasal hair'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                        Field Factor3
                        #singlechoice
                            question = 'Facial burns'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                
                        Field Factor4
                        #singlechoice
                            question = 'Soot in the mouth'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

    
        Stage Sy
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Symtopmatic'

            Precondition
                previousStep = 'Evaluation'
                condition = 'Evaluation.AssessRisk.Factor1 + Evaluation.AssessRisk.Factor2 + Evaluation.AssessRisk.Factor3 + Evaluation.AssessRisk.Factor4 > 0'

            
            HumanTask ASy
                #mandatory #exactlyOne
                label = 'Evaluate symptoms'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'ASy'
                
                Form SymptomaticForm
                    Field S1
                        #singlechoice
                            question = 'signss of respiratory'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field S2
                        #singlechoice
                            question = 'throat pain'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field S3
                        #singlechoice
                            question = 'odynophagia'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field S4
                        #singlechoice
                            question = 'drooling'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field S5
                        #singlechoice
                            question = 'stridor'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field S6
                        #singlechoice
                            question = 'hoarseness'
                            Option 'No' value='0'
                            Option 'Yes' value='1'


        Stage ClassTwo
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Laryngoscopy'
            
            Precondition
                previousStep = 'ASy'
                condition = 'Sy.ASy.S1 + Sy.ASy.S2 + Sy.ASy.S3 + Sy.ASy.S4 + Sy.ASy.S5 + Sy.ASy.S6 = 0'
            
            HumanTask AssessClassTwo
                #mandatory #exactlyOne
                label = 'Direct or indirect laryngoscopy'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwo'
                
                Form ClassTwoForm
                    Field ClTwo1
                        #singlechoice
                            question = 'Erythema at upper airway'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field ClTwo2
                        #singlechoice
                            question = 'Blisters of the palate'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

        Stage ClassTwoDiagnosed
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Class II Diagnosed'

            Precondition
                previousStep = 'EvaluationIntermediate'
                condition = 'EvaluationIntermediate.ImmediateRisks.ImmediateFactor1 + EvaluationIntermediate.ImmediateRisks.ImmediateFactor2 + EvaluationIntermediate.ImmediateRisks.ImmediateFactor3 > 0'

            Precondition
                previousStep = 'ASy'
                condition = 'Sy.ASy.S1 + Sy.ASy.S2 + Sy.ASy.S3 + Sy.ASy.S4 + Sy.ASy.S5 + Sy.ASy.S6 > 0'

            Precondition
                previousStep = 'ClassTwo'
                condition = 'ClassTwo.AssessClassTwo.ClTwo1 + ClassTwo.AssessClassTwo.ClTwo2 > 0'

            HumanTask AssessClassTwoDiagnosed
                #mandatory #exactlyOne
                label = 'Next steps for patient Diagnosed with Class II'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwoDiagnosed'
                
                Form ClassTwoDiagnosedForm
                    Field CLDiagnosed1
                        #singlechoice 
                            question = 'Early intubation for airway protection'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field CLDiagnosed2
                        #singlechoice 
                            question = 'Admit to ICU for bronchoscopy or consider to transfer to burn center'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field CLDiagnosed3
                        #singlechoice 
                            question = 'Transfer to burn center'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

        Stage ClassTwoNotDiagnosed
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Class II not Diagnosed'

            Precondition
                previousStep = 'Evaluation'
                condition = 'Evaluation.AssessRisk.Factor1 + Evaluation.AssessRisk.Factor2 + Evaluation.AssessRisk.Factor3 + Evaluation.AssessRisk.Factor4 = 0'

            Precondition
                previousStep = 'ClassTwo'
                condition = 'ClassTwo.AssessClassTwo.ClTwo1 + ClassTwo.AssessClassTwo.ClTwo2 = 0'

            HumanTask AssessClassTwoNotDiagnosed
                #mandatory #exactlyOne
                label = 'Next steps for patient not Diagnosed with Class II'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwoNotDiagnosed'
                
                Form ClassTwoNotDiagnosedForm
                    Field CLNotDiagnosed1
                        #singlechoice
                            question = 'If high-risk, consider 24-hour observation to rule out lower airway injury'
                            Option 'No' value='0'
                            Option 'Yes' value='1'

                    Field CLNotDiagnosed2
                        #singlechoice
                            question = 'If high-risk, bronchoscopy to rule out lower airway injury'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                        
"""