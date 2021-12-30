treatmentPlanStr = """
    #aca0.1
    import extfile.form as iForm
    import extfile.taskCharlsonTest
    import extfile.redGreenUiRef as rgu
    
    workspace Umcg

    define case MT1_Groningen
        prefix = 'TT1'
        version = 2
        label = 'TestTreatment'
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
            
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Admit Patient'
            //dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            //externalId = 'SelectPatient'

            use task TestCharlson

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
                        uiRef = 'privatelink'
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

input_str2 = r"""
    #aca0.1
    //import extfile.caseGCS1 as caseG
    import extfile.discharge as dStage
    import extfile.form as iForm
    import extfile.taskCharlsonTest
    import extfile.field
    import extfile.hook
    import extfile.redGreenUiRef as rgu

    workspace Umcg

    define case MT1_Groningen
        prefix = 'MT1'
        version = 1
        label = 'MockTreatment'
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

        Trigger
            On activate invoke 'http://integration-producer:8081/v1/activate'
            On delete invoke 'http://integration-producer:8081/v1/delete'

        SummaryPanel
            Section BMIHeightAndWeight #left
                label = "Height and Weight of Patient"
                InfoPath AdmitPatient.MeasureBMI.Height
                InfoPath AdmitPatient.MeasureBMI.Weight

            Section BMIScore #center
                label = "Height and Weight of Patient"
                InfoPath AdmitPatient.MeasureBMI.BMIScore

        Stage AdmitPatient
            #mandatory
            owner = 'Setting.CaseOwner'
            label = 'Admit Patient'
            //dynamicDescriptionRef = 'Setting.WorkPlanDueDate'
            //externalId = 'SelectPatient'

            use task TestCharlson

            HumanTask MeasureBMI
                #mandatory
                label = 'Measure BMI score'
                owner = 'Setting.UmcgProfessionals'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'HumanTask1External'
                

                Trigger
                    use Hook hook1
                //    On activate invoke 'http://integration-producer:8081/v1/activate' method Post

                use Form iForm.BMIForm                              

        Stage Treatment
            #mandatory #manualActivate
            owner = 'Setting.CaseManager'
            label = 'Treatment'

            Precondition
                previousStep = 'AdmitPatient' 

            AutoTask RecordPatientData
                #mandatory #exactlyOne
                label = 'Record Basic Patient Info'

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
                        #mandatory #readOnly #left #number
                        label = 'Admitted Times Plus 1'

                        expression = 'AdmittedTimes + 1'
                        uiRef = use rgu.redGreenUiRef
                        externalId = 'BmiPlus'   


            DualTask MeasureBloodPressure
                #mandatory #repeatSerial #manualActivate
                label = 'Measure Blood Pressure and inform doctor in emergency situation'
                owner = 'Setting.UmcgProfessionals'
                externalId = 'HumanTask1External'

                Precondition
                    previousStep = 'AdmitPatient' 

                Form BloodPressureForm
                    field Systolic 
                        #readonly #humanDuty #number(0-300)
                        label = 'Measure Systolic blood pressure'

                    field Diastolic 
                        #readonly #humanDuty #number(0-300)
                        label = 'Measure Diastolic blood pressure'

                    field BloodPressureAnalysis
                        #readonly #systemDuty #number(0-300)
                        label = 'Automatically alert when blood pressure is critically high'

        use stage dStage.Discharge
"""