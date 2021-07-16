obesityTreatmentPlanStr = """
    #aca0.1
    import extfile.form as iForm
    import extfile.taskCharlsonTest
    import extfile.redGreenUiRef as rgu

    workspace Umcg

    define case OT1_ObesityTreatment
        prefix = 'OT1'
        version = 1
        label = 'ObesityTreatment'
        
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
                label = 'case owner is UMCG Professionals'

            Attribute WorkplanDueDate
                #exactlyOne #date.after(TODAY)
                label = 'Workplan Due Date'
                externalId = 'dueDateConnie'

            CasePatient UmcgPatients #exactlyOne
                label = 'CasePatient'

            Attribute EvalDueDate
                #maxOne #date.after(TODAY)
                label = 'Evaluation Due Date'

            Attribute MaxDoctor
                #maxOne #number(3-5)
                label = "Maximum number of doctor per patient"
                
            Attribute Clinician
                #exactlyOne #Link.Users(UmcgPatients) 
                label = 'Clinician'
                

        Trigger
            On activate invoke 'http://integration-producer:8081/v1/activate'
            On complete invoke 'localhost:3001/connecare'

        SummaryPanel
            Section BMIHeightAndWeight #left
                label = "Height and Weight of Patient"
                InfoPath AdmitPatient.MeasureBMI.Height
                InfoPath AdmitPatient.MeasureBMI.Weight

            Section BMIScore #center
                label = "Height and Weight of Patient"
                InfoPath AdmitPatient.MeasureBMI.BMIScore

        Stage AdmitPatient
            #mandatory #repeatSerial
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
                        CustomFieldValue = "GCS1_Setting.CasePatient"
                        label = "Assigned Patient"
                        
                    Field SelectDoctor
                        #custom
                        CustomFieldValue = "GCS1_Setting.Clinician"
                        label = "Assigned Clinician"

            HumanTask MeasureBMI
                #mandatory
                label = 'Measure BMI score'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'HumanTask1External'
                //dynamicDescriptionRef = ''

                Trigger
                    On complete invoke 'http://127.0.0.1:3001/connecare' method Post

                use Form iForm.BMIForm

        Stage Treatment
            #mandatory #autoActivate
            owner = 'Setting.CaseOwner'
            label = 'Treatment'

            Precondition
                previousStep = 'AdmitPatient' 

            HumanTask RecordPatientData
                #mandatory #exactlyOne
                label = 'Record Basic Patient Info'
                owner = 'Setting.CaseOwner'

                Trigger
                    On activate 
                    invoke 'https://server1.com/api1' 
                    method Post
                    with failureMessage 'Cannot complete the data creation task!'

                    On complete 
                    invoke 'https://server1.com/api2' 
                    method Post
                    with failureMessage 'Cannot complete the completion of data creation!'

                Form RecordInfoForm
                    field AdmittedTimes
                        #number(<10) #mandatory
                        label = 'How many times have the patient been admitted to our hospitals'

                    DynamicField AdtimePlus
                        #mandatory #left #number
                        label = 'Admitted Times Plus 1'

                        expression = 'AdmittedTimes + 1'
                        uiRef = use rgu.redGreenUiRef
                        externalId = 'BmiPlus'   


            DualTask MeasureBloodPressure
                #mandatory #repeatSerial //#manualActivate
                label = 'Measure Blood Pressure and inform doctor in emergency situation'
                owner = 'Setting.CaseOwner'
                externalId = 'HumanTask1External'

                Precondition
                    previousStep = 'AdmitPatient' 

                Form BloodPressureForm
                    #readOnly

                    field Systolic 
                        #humanDuty #number(0-300)
                        label = 'Measure Systolic blood pressure'

                    field Diastolic 
                        #humanDuty #number(0-300)
                        label = 'Measure Diastolic blood pressure'

                    field BloodPressureAnalysis
                        #systemDuty #number(0-300)
                        label = 'Automatically alert when blood pressure is critically high'
"""