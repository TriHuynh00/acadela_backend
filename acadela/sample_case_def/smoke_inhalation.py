treatmentPlanStr = """
workspace Umcg
    define case ST1_SmokeInhalation
        prefix = 'ST1'
        version = 1
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
                InfoPath Symptomatic.AssessSymptomatic.Symptoms1
                InfoPath Symptomatic.AssessSymptomatic.Symptoms2
                InfoPath Symptomatic.AssessSymptomatic.Symptoms3
                InfoPath Symptomatic.AssessSymptomatic.Symptoms4
                InfoPath Symptomatic.AssessSymptomatic.Symptoms5
                InfoPath Symptomatic.AssessSymptomatic.Symptoms6
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
                    
                    InputField SelectPatient
                        #custom
                        CustomFieldValue = "Setting.CasePatient"
                        label = "Assigned Patient"
                        
                    InputField SelectDoctor
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
                        
                    InputField ImmediateFactor1
                        #singlechoice 
                            question = 'Visible burns or edema of the oropharnyx'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField ImmediateFactor2
                        #singlechoice 
                            question = 'Full thickness nasolabial burns'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField ImmediateFactor3
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
                    InputField Factor1
                        #singlechoice
                            question = 'Burns in a closed space'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Factor2
                        #singlechoice
                            question = 'Singed nasal hair'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Factor3
                        #singlechoice
                            question = 'Facial burns'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                
                    InputField Factor4
                        #singlechoice
                            question = 'Soot in the mouth'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
    
        Stage Symptomatic
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Symtopmatic'
            Precondition
                previousStep = 'Evaluation'
                condition = 'Evaluation.AssessRisk.Factor1 + Evaluation.AssessRisk.Factor2 
                            + Evaluation.AssessRisk.Factor3 + Evaluation.AssessRisk.Factor4>0'
            
            HumanTask AssessSymptomatic
                #mandatory #exactlyOne
                label = 'Evaluate symptoms'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'Symptomatic'
                
                Form SymptomaticForm
                    InputField Symptoms1
                        #singlechoice
                            question = 'signss of respiratory'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Symptoms2
                        #singlechoice
                            question = 'throat pain'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Symptoms3
                        #singlechoice
                            question = 'odynophagia'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Symptoms4
                        #singlechoice
                            question = 'drooling'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Symptoms5
                        #singlechoice
                            question = 'stridor'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField Symptoms6
                        #singlechoice
                            question = 'hoarseness'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
        Stage ClassTwo
            #mandatory
            owner = 'Setting.Clinician'
            label = 'Laryngoscopy'
            
            Precondition
                previousStep = 'Symptomatic'
                condition = 'Symptomatic.AssessSymptomatic.Symptoms1 + Symptomatic.AssessSymptomatic.Symptoms2 + Symptomatic.AssessSymptomatic.Symptoms3 + Symptomatic.AssessSymptomatic.Symptoms4 + Symptomatic.AssessSymptomatic.Symptoms5 + Symptomatic.AssessSymptomatic.Symptoms6=0'
            
            HumanTask AssessClassTwo
                #mandatory #exactlyOne
                label = 'Direct or indirect laryngoscopy'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwo'
                
                Form ClassTwoForm
                    InputField ClTwo1
                        #singlechoice
                            question = 'Erythema at upper airway'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField ClTwo2
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
                previousStep = 'Symptomatic'
                condition = 'Symptomatic.AssessSymptomatic.Symptoms1 + Symptomatic.AssessSymptomatic.Symptoms2 + Symptomatic.AssessSymptomatic.Symptoms3 + Symptomatic.AssessSymptomatic.Symptoms4 + Symptomatic.AssessSymptomatic.Symptoms5 + Symptomatic.AssessSymptomatic.Symptoms6>0'
            Precondition
                previousStep = 'ClassTwo'
                condition = 'ClassTwo.AssessClassTwo.ClTwo1 + ClassTwo.AssessClassTwo.ClTwo2>0'
            
            HumanTask AssessClassTwoDiagnosed
                #mandatory #exactlyOne
                label = 'Next steps for patient Diagnosed with Class II'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwoDiagnosed'
                
                Form ClassTwoDiagnosedForm
                    InputField CLDiagnosed1
                        #singlechoice 
                            question = 'Early intubation for airway protection'
                            Option 'Yes' value='0'
                            Option 'Yes' value='1'
                    InputField CLDiagnosed2
                        #singlechoice 
                            question = 'Admit to ICU for bronchoscopy or consider to transfer to burn center'
                            Option 'Yes' value='0'
                            Option 'Yes' value='1'
                    InputField CLDiagnosed3
                        #singlechoice 
                            question = 'Transfer to burn center'
                            Option 'Yes' value='0'
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
                condition = 'ClassTwo.AssessClassTwo.ClTwo1 + ClassTwo.AssessClassTwo.ClTwo2 =0'
            
            HumanTask AssessClassTwoNotDiagnosed
                #mandatory #exactlyOne
                label = 'Next steps for patient not Diagnosed with Class II'
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'AssessClassTwoNotDiagnosed'
                
                Form ClassTwoNotDiagnosedForm
                    InputField CLNotDiagnosed1
                        #singlechoice
                            question = 'If high-risk, consider 24-hour observation to rule out lower airway injury'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
                    InputField CLNotDiagnosed2
                        #singlechoice
                            question = 'If high-risk, bronchoscopy to rule out lower airway injury'
                            Option 'No' value='0'
                            Option 'Yes' value='1'
"""