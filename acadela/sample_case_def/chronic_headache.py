treatmentPlanStr = """
#aca0.1
import extfile.redGreenUiRef as rgu
import extfile.template.body3ViewsTemplate as bTemplate

workspace Umcg

define case MI1_Headache
    prefix = 'MI1'
    version = 14
    label = 'Chronic Headache Treatment'
    
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
        CaseOwner UmcgClinicians #exactlyOne
            label = 'Dr. Michel Clinician'   

        Attribute WorkplanDueDate
            #exactlyOne #date.after(TODAY)
            label = 'Workplan Due Date'

        CasePatient UmcgPatients #exactlyOne
            label = 'Patient'
          
        Attribute Clinician
            #exactlyOne #Link.Users(UmcgClinicians) 
            label = 'Clinician'
      
    SummaryPanel
        Section PainAreaSummary #left
            label = "Pain Area:"
            InfoPath Questioning.QuestionPatientCondition.PainArea

    Stage Observation
        #mandatory
        owner = 'Setting.CaseOwner'
        label = 'Observation'

        HumanTask CheckBreath
            #mandatory
            label = 'Observe Breath Pattern'
            dueDateRef = 'Setting.WorkplanDueDate'
         
            Form BreathCheckForm
                #mandatory
                 
                InputField BreathPattern
                    #singleChoice
                    question = "What is the breathing pattern of the patient?"
                    option 'Light' value = '0'
                    option 'Short' value = '1'
                    option 'Chest breathing' value = '2'
                    option 'Diaphragmatic breathing' value = '3'
                    option 'Deep' value = '4'
                
        HumanTask CheckBehavior
            #mandatory
            label = 'Observe Behaviors'
            dueDateRef = 'Setting.WorkplanDueDate'
         
            Form BehaviorCheckForm
                #mandatory
                 
                InputField WalkPattern
                    #singleChoice
                    question = "How does the patient walk?"
                    option 'Stiff' value = '0'
                    option 'Fragmentated' value = '1'
                    option 'Bent over' value = '2'
                    option 'Smooth' value = '3'
                    option 'Stretched' value = '4'
                    option 'Heavy' value = '5'
                    option 'Upstraight & head up' value = '6'

                InputField ShakeHandPattern
                    #singleChoice #atLeastOne #notMandatory 
                    question = "How does the patient shake hand?"
                    option 'Weak' value = '0'
                    option 'Normal' value = '1'
                    option 'Strong' value = '2'
                    option 'With eye contact' value = '3'
                    option 'No eye contact' value = '4'
                    option 'Brief' value = '5'
        
                InputField PatientTension
                    #singleChoice
                    question = "How tense is the patient?"
                    option 'Confused' value = '0'
                    option 'Fluffy' value = '1'
                    option 'Relaxed' value = '2'
                    option 'Tense' value = '3'
                    option 'Chaotic' value = '4'
            
                    
    Stage Questioning
        #mandatory
        owner = 'Setting.Clinician'
        label = 'Questioning'
        
        Precondition
            previousStep = 'Observation'
            
            HumanTask QuestionPatientCondition
                #mandatory
                owner = 'Setting.Clinician'
                dueDateRef = 'Setting.WorkplanDueDate'
                label = 'Question Patient Condition'
                
                Form PatientConditionForm
                    #mandatory
                    InputField HowHeadacheStart
                        #text #left
                        label = "How did it start?"

                    InputField WhenHeadacheStart
                        #text #center
                        label = "When did it start?"

                    InputField HeadacheFrequency
                        #text #center
                        label = "How often is the headache?"
                
                    InputField PainQuality
                        #singleChoice #atLeastOne #left
                        question = "What is the pain quality?"
                        option "Wavy" value = '1'
                        option "Tingling" value = '2'
                        option "Burning" value = '3'
                        option "Stinging (like a needle pointing)" value = '4'
                        option "Pain around the head" value = '5'
                        option "Pain on the eyes" value = '6'

                    InputField PainArea
                        #singleChoice #atLeastOne #left
                        question = "Where is/are the location of the pain(s)?"
                        option "Shoulder" value = 'SHOULDER'
                        option "In the head" value = 'INHEAD'
                        option "On top of the head" value = 'TOPHEAD'
                        option "Temple" value = 'TEMPLE'
                        option "Forehead" value = 'FOREHEAD'
                        option "Head Crown" value = 'HEADCROWN'
                        option "Nape" value = 'NAPE'
                        
                    InputField WorseningSituation
                        #singleChoice #atLeastOne 
                        question = "What emotion(s) makes your pain worse?"
                        option "Angry" value = '1'
                        option "Fear" value = '2'
                        option "Sad/Sorrow" value = '3'
                        option "Stressful" value = '4'
                    
                    InputField OtherWorseningSituation
                        #text #notmandatory
                        Label = "Are their other emotions or things that worsen your headache?"
                        
                    InputField SleepCondition
                        #singleChoice 
                        question = "How is your sleep condition?"
                        option "I got nightmare frequently" value = '1'
                        option "I cannot sleep well" value = '1'
                        option "Rarely sleep well" value = '1'
                        option "Often sleep well" value = '2'
                        option "Good" value = '3'
                        option "Very good" value = '4'
                        
                    InputField WhatMakesBetter
                        #text 
                        label = "What can help you feel less painful?"
                    
                    InputField TreatmentProposal
                        #text
                        label = "Proposed Treatment:"

                    OutputField bodystyle
                        #string
                        label = "Massage Style"
                        uiRef = "hidden"
                        expression = 'let massageSites = PainArea in
                            let styleTemple = if massageSites.contains("TEMPLE")
                                then ".temple{fill:red} .shoulder{fill:red} .nape{fill:red}" else "" in styleTemple
                            '

                    InputField bodytemplate
                        #string #exactlyOne
                        label = "Body Template"
                        uiRef = 'hidden'
                        defaultValue = use bTemplate.body3ViewsTemplate

                    OutputField bodyVisual
                        #string
                        label = "Potential Massage Points"
                        uiRef = 'svg'
                        expression = 'replace(bodytemplate, "#dynamicstylevars{}", bodystyle)'

    Stage TreatmentApproval
        #mandatory
        label = "Treatment Approval"

        Precondition
            previousStep = "Questioning"
        
        HumanTask DiscussTreatment
            #mandatory
            label = "Discuss Treatment With Patient"
            
            Form TreatmentDiscussionForm
                #mandatory
                InputField PatientConsent
                    #singleChoice
                    question = "Does the patient agree with the proposed treatment?"
                    option "No" value = '0'
                    option "Yes" value = '1'
                    option "Undecided" value = '2'
                    option "Other" value = '3'
                
                InputField DisagreementReason
                    #text #notmandatory
                    label = "What is the patient's concern with the treatment process?"
                
                InputField AcupunctureConsent
                    #singleChoice
                    question = "Does the patient agree with using Acupuncture?"
                    option "No" value = '0'
                    option "Yes" value = '1'

                InputField GuashaConsent
                    #singleChoice
                    question = "Does the patient agree with using Guasha?"
                    option "No" value = '0'
                    option "Yes" value = '1'
                    
                InputField MassageConsent
                    #singleChoice
                    question = "Does the patient agree with the use of Massage?"
                    option "No" value = '0'
                    option "Yes" value = '1'

    Stage Massaging
        #mandatory
        label = "Massaging"

        Precondition
            previousStep = "TreatmentApproval"
            condition = "TreatmentApproval.DiscussTreatment.MassageConsent = 1"

        HumanTask MassageHead
            #mandatory
            label = 'Massage Head'

            Form HeadMassageForm
                #mandatory

                InputField HeadMassagePosition
                    #singleChoice #atLeastOne
                    question = "Massage the following positions:"
                    option "Left Shoulder" value = '1'
                    option "Right Shoulder" value = '2'
                    option "Center Upper Back" value = '3'
                    option "Left Nape" value = '4'
                    option "Right Nape" value = '5'
                    option "Neck" value = '6'
                    option "Jaw" value = '7'
                    option "Upper Eyes" value = '8'
                    option "Occipital Bone" value = '9'
                    option "Head Crown" value = "10"
                    option "Close to Kidney" value = "11"
                    option "Temple" value = "12"
                    option "Others" value = "13"

                InputField OtherMassagePosition
                    #text #notMandatory
                    label = 'Apply massage to the following positions:'

                InputField ApplyHeat
                    #singleChoice
                    question = "Using Heat Lamp during the massage:"
                    option "No" value = '0'
                    option "Yes" value = '1'
        
    Stage Acupuncture
        #mandatory
        label = "Acupuncture"

        Precondition
            previousStep = "TreatmentApproval"
            condition = "TreatmentApproval.DiscussTreatment.AcupunctureConsent = 1"

        HumanTask AcupuncturePosition
            #mandatory
            label = 'Apply Acupuncture:'

            Form AcuPosForm
                #mandatory
                InputField AcupuncturePos
                #singleChoice #atLeastOne
                Question = 'Apply Acupuncture to Positions:'
                    Option "Below Left Ear" value = '1'
                    Option "Below Right Ear" value = '2'
                    Option "Left Nape" value = '3'
                    Option "Right Nape" value = '4'
    
    Stage Guasha
        #mandatory
        label = "Guasha"

        Precondition
            previousStep = "TreatmentApproval"
            condition = "TreatmentApproval.DiscussTreatment.GuashaConsent = 1"

        HumanTask ApplyGuasha
            #mandatory
            label = 'Apply Guasha:'

            Form ApplyGuashaForm
                #mandatory
                InputField GuashaUsage
                #text
                label = 'Apply Guasha to the following positions:'

    Stage Discharge
        #mandatory
        label = "Discharge"

        Precondition
            previousStep = "Observation"

        HumanTask DischargePatient
            #mandatory
            label = 'Discharge'

            Form DischargeForm
                #mandatory
                InputField DoctorNote
                #text
                label = 'Doctor Note:'
"""

