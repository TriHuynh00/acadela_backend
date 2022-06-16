treatmentPlanStr = """
#aca0.1
workspace Umcg

define case MRI_Schizophrenia
    prefix = 'MRI'
    version = 2
    label = 'Schizophrenia Treatment'
    
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
        // label = "Case Configuration"
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
        Section MedicalInformation #stretched
            label = "Medical Information:"
            InfoPath Identification.MedicalInfo.Age
            InfoPath Identification.MedicalInfo.Gender
            InfoPath Identification.MedicalInfo.PsychosisTime
            InfoPath Identification.MedicalInfo.ConcomitantDisease
            InfoPath Identification.MedicalInfo.RiskGroup
            
        Section PatientPreferences #stretched
            label = "Patient Preferences:"
            InfoPath Identification.PatientPreferences.TreatmentGoal
            InfoPath Identification.PatientPreferences.PreviouslyUsedDrugs
            InfoPath Identification.PatientPreferences.AvoidSideEffect
            InfoPath Identification.PatientPreferences.PreferredDrugType
            InfoPath Identification.PatientPreferences.OtherImportances
            
        Section LastTherapySession #stretched
            label = "Patient Preferences:"
            InfoPath ShareDecisionMaking.OpenTherapySession.SelectedAntipsychotics
            InfoPath ShareDecisionMaking.OpenTherapySession.AvoidSideEffect
            InfoPath ShareDecisionMaking.OpenTherapySession.TolerableSideEffect
            
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

        HumanTask MedicalInfo
            #mandatory
            label = "Medical Information"
            Form MedicalInfoForm
                #mandatory
                InputField Age
                    #number
                    label = 'Age:'
                    
                InputField Gender
                    #singlechoice
                    question = 'Gender:'
                        option 'Male' value = '0'
                        option 'Female' value = '1'
                        option 'Other' value = '2'
                        
                InputField PsychosisTime
                    #number
                    label = 'Length of Psychosis (Months):'
                    
                InputField ConcomitantDisease
                    #singlechoice #atLeastOne #left
                    additionalDescription = 'Is any of the following concomitant diseases known to you?'
                    question = 'Known Concomitant Disease:'
                        Option "Cardiac Diseases" value = "1"
                        Option "Epilepsy" value = "2"
                        Option "Liver Diseases" value = "3"
                        Option "Kidney Diseases" value = "4"
                        Option "Adipositas" value = "5"
                        Option "Diabetes" value = "6"
                        Option "Fat Metabolism Disorder" value = "7"
                        Option "Blood Count Changes" value = "8"
                        Option "Cognitive Changes/Dementias" value = "9"
                        
                InputField RiskGroup
                    #singlechoice #atLeastOne #left
                    question = 'Which sub-group does the patient belongs to?'
                        option 'Adolescence' value = '1'
                        option 'Senior' value = '2'
                        option 'Comorbid Substance Abuse' value = '3'
                        option 'Predominantly Negative Symptoms' value = '4'
                        option 'Psychologically Stable Patient' value = '5'
                        option 'Therapy resistance' value = '6'
                        option 'Pregnant' value = '7'         
        
        HumanTask PatientPreferences
            #mandatory
            label = 'Record Medical Profile'
            
            Form PrefForm
                #mandatory
                
                InputField TreatmentGoal
                    #text
                    label = 'What would I like to achieve after the treatment? (Treatment Goal):'
                
                InputField PreviouslyUsedDrugs
                    #singlechoice #left #atLeastOne 
                    Question = 'Previously Used Antipsychotics:'
                        Option "Amisulprid" value = "1"
                        Option "Aripirazol" value = "2"
                        Option "Cariprazin" value = "3"
                        Option "Clozapin" value = "4"
                        Option "Haloperidol" value = "5"
                        Option "Olanzapin" value = "6"
                        Option "Paliperidon" value = "7"
                        Option "Risperidon" value = "8"
                        Option "Perphenazin" value = "9"
                        Option "Quetiapin" value = "10"
                        Option "Sertindol" value = "11"
                        Option "Ziprasidon" value = "12"
                        
                
                InputField RetakePreviouslyUsedDrugs
                    #singlechoice #atLeastOne #center 
                    Question = 'Which Drugs would be Used again:'
                        Option "Amisulprid" value = "Amisulprid"
                        Option "Aripirazol" value = "Aripirazol"
                        Option "Cariprazin" value = "Cariprazin"
                        Option "Clozapin" value = "Clozapin"
                        Option "Haloperidol" value = "Haloperidol"
                        Option "Olanzapin" value = "Olanzapin"
                        Option "Paliperidon" value = "Paliperidon"
                        Option "Risperidon" value = "Risperidon"
                        Option "Perphenazin" value = "Perphenazin"
                        Option "Quetiapin" value = "Quetiapin"
                        Option "Sertindol" value = "Sertindol"
                        Option "Ziprasidon" value = "Ziprasidon"
                
                InputField PrepareDrugTypeTaken
                    #singlechoice #stretched
                    Question = 'Medications can be administered as tablets, drops, or injections (usually several weeks apart). Do you want to start thinking about this now?'
                        Option "Yes" value = "1"
                        Option "No" value = "0"
                    
                InputField PreferredDrugType
                    #singlechoice #left #atLeastOne
                    Question = 'Preferred Drug Types:'
                        Option "Syringes" value = "1"
                        Option "Pills" value = "2"
                        Option "Drops" value = "3"
                        
                InputField AvoidSideEffect
                    #stretched #singlechoice #atLeastOne
                    Question = 'Side Effects to be Avoided:'
                        Option 'Dry Mouth, Blurred Vision, Constipation' value = '1'
                        Option 'Muscular Stiffness, Movement Disorders, Tremor' value = '2'
                        Option 'Reduction of Sexual Desire, Sexual Dysfunction, Menstrual Cramps' value = '3'
                        Option 'Weight Gain' value = '4'
                        Option 'Fatigue' value = '5'
                        Option 'Restless Legs' value = '6'
                        
                InputField OtherImportances
                    #text #notmandatory
                    label = 'Other Important Notes:'
                    
    Stage ShareDecisionMaking
        #mandatory #repeatSerial
        owner = 'Setting.Clinician'
        label = 'Share Decision Making'
        
        Precondition
            previousStep = 'Identification'
            
        Precondition
            previousStep = 'ShareDecisionMaking'
                        
        HumanTask OpenTherapySession
            #mandatory #repeatParallel #atLeastOne
            label = 'Arrange Therapy Session'
            owner = 'Setting.Clinician'
            dueDateRef = 'Setting.WorkplanDueDate'
            
            Form SDMForm
                #mandatory
                InputField SelectedAntipsychotics
                    #singlechoice #atleastone
                    Question = 'Selected Antipsychotics:'
                        Option "Amisulprid" value = "1"
                        Option "Aripirazol" value = "2"
                        Option "Cariprazin" value = "3"
                        Option "Clozapin" value = "4"
                        Option "Haloperidol" value = "5"
                        Option "Olanzapin" value = "6"
                        Option "Paliperidon" value = "7"
                        Option "Risperidon" value = "8"
                        Option "Perphenazin" value = "9"
                        Option "Quetiapin" value = "10"
                        Option "Sertindol" value = "11"
                        Option "Ziprasidon" value = "12"
                
                InputField PsiacCheck
                    #longtext
                    label = 'PSIAC Verification of Conflicted Drugs'
                
                InputField AvoidSideEffect
                    #left #singlechoice #atLeastOne #notmandatory
                    Question = 'Side Effects to be Avoided:'
                        Option 'Dry Mouth, Blurred Vision, Constipation' value = '1'
                        Option 'Muscular Stiffness, Movement Disorders, Tremor' value = '2'
                        Option 'Reduction of Sexual Desire, Sexual Dysfunction, Menstrual Cramps' value = '3'
                        Option 'Weight Gain' value = '4'
                        Option 'Fatigue' value = '5'
                        Option 'Restless Legs' value = '6'
                        Option 'Epilepsy' value = '7'
                        
                InputField TolerableSideEffect
                    #right #singlechoice #atLeastOne #notmandatory
                    Question = 'Side Effects to be Tolerated:'
                        Option 'Dry Mouth, Blurred Vision, Constipation' value = '1'
                        Option 'Muscular Stiffness, Movement Disorders, Tremor' value = '2'
                        Option 'Reduction of Sexual Desire, Sexual Dysfunction, Menstrual Cramps' value = '3'
                        Option 'Weight Gain' value = '4'
                        Option 'Fatigue' value = '5'
                        Option 'Restless Legs' value = '6'
                
                InputField Comment
                    #notmandatory #stretched
                    label = 'Comment:'
                    
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