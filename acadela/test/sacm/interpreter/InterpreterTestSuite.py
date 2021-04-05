import unittest

import sys
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


objectDefinitionCode = """
        define HumanTask TestCharlson
            #manualActivate #mandatory
            description = 'Charlson Comorbidity Form'
            Form //CharlsonForm
                field Charlson1
                    #selector #mandatory
                    Question = 'Do you have diabetes?'
                        Option 'No' value = '0'
                        Option 'Yes' value = '1'

                field Charlson2
                    #selector #mandatory
                    Question = 'Do you have hearth attacks?'
                        Option 'No' value = '0'
                        Option 'Yes' value = '1'
    """

baseCodeWithoutField = """
    #aca0.1
    import discharge from '/stages/discharge.aca' 
    workspace Umcg

    //ObjectDefinitionCode

    define case GCS1_Groningen
        prefix = 'GCS1'
        version = 1
        description = 'a obesity treatment care plan'
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional' 
            group UmcgPatients name = 'Umcg Patient' 

            user matthijs
            user williamst

        // A comment
            /* a multiline
             * Comment
             */

        Setting
            // description = "Case Configuration"
            CaseOwner UmcgProfessionals #exactlyOne
                description = 'case owner is UMCG Professionals'

            Attribute WorkplanDueDate
                #exactlyOne #date.after(TODAY)
                description = 'Workplan Due Date'
                externalId = 'dueDateConnie'

            CasePatient UmcgPatient #exactlyOne
                description = 'the patient of this case'

            Attribute EvalDueDate
                #maxOne #date.after(TODAY)
                description = 'Evaluation Due Date'

            Attribute MaxDoctor
                #maxOne #number(3-5)
                description = "Maximum number of doctor per patient"

        Trigger
            On activate invoke 'http://integration-producer:8081/v1/activate'
            On delete invoke 'http://integration-producer:8081/v1/delete'

        SummaryPanel
            Section BMIHeightAndWeight #left
                description = "Height and Weight of Patient"
                InfoPath Identification.MeasureBMI.Height
                InfoPath Identification.MeasureBMI.Weight

            Section BMIScore #center
                description = "Height and Weight of Patient"
                InfoPath Identification.MeasureBMI.BMIScore

        Stage AdmitPatient
            #mandatory #manualActivate
            owner = 'Settings.CaseManager'
            description = 'Admit Patient into Treatment'
            dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            externalId = 'SelectPatient'

            HumanTask MeasureBMI
                #mandatory
                description = 'Measure BMI score'
                owner = 'Settings.UmcgProfessionals'
                dueDateRef = 'Settings.WorkplanDueDate'
                externalId = 'HumanTask1External'
                dynamicDescriptionRef = 'Settings.PatientNumber'

                Trigger
                    On activate invoke 'http://integration-producer:8081/v1/activate' method Post

    """
