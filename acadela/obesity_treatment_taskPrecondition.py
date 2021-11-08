treatmentPlanStr = """
    workspace Umcg

    define case OT1_ObesityTreatment
        prefix = 'OT1'
        version = 1
        label = 'ObesityTreatment'
        
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician'//staticId = 'asdf234'
            group UmcgClinicians name = 'Umcg Clinician'
            group UmcgProfessionals name = 'Umcg Professional'
            group UmcgPatients name = 'Umcg Patient' 

            //user williamst
            //user michelf
            //user hopkinsc

        // A comment
            /* a multiline
             * Comment
             */

        Setting
            // label = 'Case Configuration'

            Attribute WorkplanDueDate
                #exactlyOne #date.after(TODAY)
                label = 'Workplan Due Date'
                externalId = 'dueDateConnie'
            CaseOwner UmcgProfessionals #exactlyOne
                label = 'UMCG Professionals'

            CasePatient UmcgPatients #exactlyOne
                label = 'CasePatient'

            Attribute EvalDueDate
                #maxOne #date.after(TODAY)
                label = 'Evaluation Due Date'

            Attribute MaxDoctor
                #maxOne #number(3-5)
                label = 'Maximum number of doctor per patient'
                
            Attribute Clinicians
                #exactlyOne #Link.Users(UmcgClinicians) 
                label = 'Clinician'
                

        Trigger
            On activate invoke 'http://integration-producer:8081/v1/activate'
            On complete invoke 'localhost:3001/connecare'

        SummaryPanel
            Section BMIHeightAndWeight #left
                label = 'Height and Weight of Patient'
                InfoPath Evaluation.MeasureBMI.Height
                InfoPath Evaluation.MeasureBMI.Weight

            Section BMIScore #center
                label = 'BMI Score'
                InfoPath Evaluation.MeasureBMI.BMIScore
                
            Section CaloriesIntake #left
                label = 'Today Intake Calories'
                InfoPath Treatment.PlanDiet.TotalIntakeCalo
                
            Section CaloriesIntake #left
                label = 'Today Consumed Calories'
                InfoPath Treatment.PlanExercise.CaloBurn

        Stage AdmitPatient
            #mandatory #noRepeat
            owner = 'Setting.CaseOwner'
            label = 'Admit Patient'
            group UmcgPhysicians name = 'Umcg Physician'//staticId = 'asdf234'

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
                        CustomFieldValue = 'Setting.CasePatient'
                        label = 'Assigned Patient'
                        
                    Field SelectDoctor
                        #custom
                        CustomFieldValue = 'Setting.Clinicians'
                        label = 'Assigned Clinician'

        Stage Evaluation
            #mandatory
            
            owner = 'Setting.CaseOwner'
            label = 'Evaluation'
            
            Precondition
            previousStep = 'AdmitPatient'

            HumanTask MeasureBMI
                #mandatory #manualActivate #repeatParallel 
                label = 'Measure BMI score'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'MeasureBMI'
                
                //use Form iForm.BMIForm
                
                Form BMIForm
                    #mandatory
                    
                    field Height
                        #number(0-3) #exactlyOne
                        label ='Height of patient in m'
                
                    field Weight
                        #number(0-300) #exactlyOne
                        label ='Weight of patient in kg'
                
                    field AgeRange
                        #singlechoice #exactlyOne
                        Question = 'What is your age range?'
                            Option 'less than 10' value = '1' additionalDescription = 'child' externalId = 'childBMI'
                            Option '10-30' value = '1.2'
                            Option '30-50' value = '1.5'
                            Option 'over 50' value = '1.7'
                
                
                    DynamicField BmiScore
                        #mandatory #number
                        label ='BMI Calculation in kilogram and meters'
                        expression = 'Weight / (Height * Height)'
                
                    DynamicField BmiScorePlus
                        #mandatory #left #number
                        label = 'BMI Calculation with age counted'
                        expression = 'BmiScore + AgeRange'
                        uiRef = 'colors(5<orange<=18<green<=25<red<100)'
           
            HumanTask FinalBMI
                #mandatory #noRepeat 
                label = 'Health Check'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.WorkplanDueDate'
                externalId = 'HealthCheck'
                
                Precondition
                    previousStep = 'MeasureBMI'
                    //condition = 'Evaluation.MeasureBMI.BmiScore <= 23'
                    
                Form HealthEvalForm
                    #mandatory
                    
                    field GeneralHealthEvaluation
                        #text #exactlyOne
                        label ='General Health Examination:'
                        
                    field HealthCode
                        #number(0-5) #exactlyOne
                        label ='Health Status Code:'
            
        Stage Treatment
            #mandatory #repeatParallel
            owner = 'Setting.CaseOwner'
            label = 'Treatment'

            Precondition
                previousStep = 'AdmitPatient' 
                
            HumanTask PlanDiet
                #mandatory
                label = 'Plan Diet'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.EvalDueDate'
                externalId = 'PlanDiet'

                Form Diet
                    #mandatory
                    Field Breakfast
                        #singlechoice
                        question = 'Breakfast:'
                        // The Mayo Clinic
                        option 'Milky Fruity Oatmeal' value = '400' 
                                additionalDescription = '1/2 cup cooked oatmeal 
                                with 1 cup milk and 2 tablespoons raisins, 
                                1/4 cup mango, calorie-free beverage'
                                
                        // https://www.medicalnewstoday.com/articles/weight-loss-meal-plan#7-day-meal-plan
                        option 'Vegan Energetica Smoothie' value = '500'
                                additionalDescription = 'Smoothie made with protein powder, berries, and oat milk'
                        
                        option 'Spinato Scrambled Egg' value = '450'
                                additionalDescription = 'Scrambled egg with spinach & tomato'

                    Field Lunch 
                        #singlechoice
                        question = 'Dinner:'
                        
                        option 'Veggie Hummus Wrap' value = '660' 
                                additionalDescription = 'Hummus and vegetable wrap'
                                 
                        option 'Vegetable Soup and Oatcakes' value = '600'
                                additionalDescription = 'Vegetable soup with two oatcakes'
                        
                        option 'Corn, Lettuce and Chicken Salad' value = '500'
                                additionalDescription = 'Chicken salad with lettuce and corn'

                    Field Dinner 
                        #singlechoice
                        question = 'Dinner:'
                        
                        option 'Spicy Caulibean Rice' value = '550' 
                                additionalDescription = 'Bean chilli with cauliflower ‘rice’'
                                 
                        option 'Fried Chicken and Soba Noodles' value = '600'
                                additionalDescription = 'Chicken stir fry and soba noodles'
                        
                        option 'Saucy Veggie Lentil' value = '650'
                                additionalDescription = 'Roasted Mediterranean vegetables, puy lentils, & tahini dressing'

                    
                    Field Exercise
                        #singlechoice #mandatory
                        
                        question = 'What is the morning exercise for today?'
                            option 'Push Up' value = '100'
                            option 'Jogging' value = '50'
                            option 'Martial Art - Basic' value = '70'
                            option 'Aerobic' value = '60'
                        
                    Field Duration 
                        #number(1-60) #mandatory
                        label = 'Duration (minute):'
                               
                    DynamicField TotalIntakeCalo
                        #number
                        label = 'Total Intake Calories (kCal):'
                        
                        expression = 'Breakfast + Lunch + Dinner'
                        uiRef = 'colors(0<=orange<1200<green<=1600<red<=10000)'
                        
                                            
                    DynamicField CaloBurn
                        #mandatory #number
                        label = 'Estimated Burned Calories'

                        expression = 'Duration * Exercise'
                        uiRef = 'colors(0<=orange<=1400<green<=1800<red<=10000)'
                        
            HumanTask MeasureBloodSugar
                #mandatory #exactlyOne
                label = 'Measure Blood Sugar'
                owner = 'Setting.CaseOwner'
                dueDateRef = 'Setting.EvalDueDate'
                externalId = 'BloodSugar'

                Form BloodSugarForm
                    field BloodGlucose
                        #mandatory #number(0-40)
                        label = 'Measure Blood Glucose (mmol/L)'
                        
                    DynamicField BloodSugarAnalysis
                        #mandatory #number
                        label = 'Blood Sugar Score'
                        expression = 'BloodGlucose'
                        uiRef = 'colors(0<green<=6.3<orange<=10<red<=40)'
                        
        Stage Discharge
            // Using manualActivationExpression + activation = EXPRESSION does not 
            // help trigger a stage/task conditionally
            #mandatory #exactlyOne #manualActivate
            owner = 'Setting.CaseOwner'
            label = 'Discharge'
                            
            Precondition
                previousStep = 'FinalBMI'
                // TODO: Try Setting condition
                //condition = 'Evaluation.FinalBMI.HealthCode<3'
                
            
            HumanTask DischargePatient
                #mandatory //#activateWhen('Evaluation.FinalBMI.HealthCode<3')
                label = 'Discharge Patient'
                
                Precondition
                    previousStep = 'FinalBMI'
                    owner = 'Setting.CaseOwner'

                    
                Form DischargeForm
                    Field DoctorNote 
                        #text #mandatory
                        label = 'Post-Treatment Recommendation:'
"""