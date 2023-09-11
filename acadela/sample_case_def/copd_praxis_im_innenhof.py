treatmentPlanStr = """
#aca0.1

workspace Umcg
    define case PII1_COPD
        prefix = 'PII1'
        version = 7
        label = 'COPD Treatment'
        
        Responsibilities
            group UmcgPhysicians name = 'Umcg Physician' //staticId = 'asdf234' 
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
              Section BloodPressureMeasurement #left
                  label = "Systolic Pressure:"
                  InfoPath Evaluation.MeasureBloodPressure.Systolic
      
              Section Diastolic #left
                  label = "Diastolic"
                  InfoPath Evaluation.MeasureBloodPressure.Diastolic 
                  
              Section DoctorNote #left
                  label = "Recommendations"
                  InfoPath Discharge.DischargePatient.DoctorNote
          
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
                            
          Stage Exercise
              #mandatory #repeatSerial #atLeastOne
              label = "Exercise"
              
              Precondition
                  previousStep = 'Identification'
                  
              Precondition
                  previousStep = 'Exercise'
                  
              HumanTask QuestionPreExercise
                  #mandatory #atLeastOne
                  label = "Pre-exercise Questionnaire"
                  
                  Form PreExerciseForm
                      #mandatory 
                      InputField StressOrShortBreath
                          #singlechoice #stretched
                          question = 'Do you feel stressed or short of breath today?'
                              option 'Not at all' value = '4'
                              option 'A little' value = '3'
                              option 'So-so' value = '2'
                              option 'Yes' value = '1'
                              option 'Too much' value = '0'
                          uiRef = "colors(0<=red<=1<yellow<=2<=green<=4)"
                      
                      InputField BreathingStruggle
                          #singlechoice #stretched 
                          question = 'Do you struggle to breath?'
                              option 'Not at all' value = '4'
                              option 'A little' value = '3'
                              option 'So-so' value = '2'
                              option 'Yes' value = '1'
                              option 'Too much' value = '0'
                          uiRef = 'colors(0<=red<=1<yellow<=2<=green<=4)'
                          
                      InputField SleepStatus
                          #singlechoice #stretched
                          question = 'How was your sleep last night?'
                              option 'Good' value = '2'
                              option 'Medium' value = '1'
                              option 'Bad' value = '0'
                          uiRef = 'colors(0<=red<1<=yellow<2<=green<=10)'
                      
                      InputField HaveMucus
                          #left #singlechoice
                          question = 'Do you have mucus today?'
                              option 'No' value = '0'
                              option 'Yes' value = '1'
                              
                      InputField CoughOutMucus
                          #left #singlechoice
                          question = 'Can you cough your mucus out?'
                              option 'No' value = '0'
                              option 'Yes' value = '1'
              
              HumanTask BreathingExercise
                  #mandatory #atLeastOne
                  label = 'Conduct Breathing Exercise'
                  
                  precondition
                      previousStep = 'QuestionPreExercise'
                  
                  Form ExerciseEvalForm
                      #mandatory
                      InputField ShoulderIncrease
                          #left #singlechoice
                          question = 'The shoulder position is accurate.'
                              option 'No' value = '0'
                              option 'Almost' value = '1'
                              option 'Yes' value = '2'
                              
                      InputField BellyExpansion
                          #left #singlechoice
                          question = 'The belly contraction and expansion is accurate.'
                              option 'No' value = '0'
                              option 'Almost' value = '1'
                              option 'Yes' value = '2'
                              
                      InputField SittingPosture
                          #stretched #singlechoice
                          question = 'The sitting posture of the patient is accurate.'
                              option 'No' value = '0'
                              option 'Almost' value = '1'
                              option 'Yes' value = '2'
                              option 'Not Applicable' value = '-1'
                              
                      InputField ExerciseComment
                          #stretched #notmandatory
                          label = 'Comment'
                          
              HumanTask QuestionPostExercise
                  #mandatory #atLeastOne
                  label = 'Post-exercise Questionnaire'
                  
                  precondition
                      previousStep = 'BreathingExercise'
                      
                  
                  Form PostExerciseForm
                      #mandatory
                      InputField StressOrShortBreath
                          #singlechoice #stretched
                          question = 'Do you feel stressed or short of breath today?'
                              option 'Not at all' value = '4'
                              option 'A little' value = '3'
                              option 'So-so' value = '2'
                              option 'Yes' value = '1'
                              option 'Too much' value = '0'
                          uiRef = 'colors(0<=red<=1<yellow<=2<=green<=4)'
                      
                      InputField BreathingStruggle
                          #singlechoice #stretched
                          question = 'Do you struggle to breath?'
                              option 'Not at all' value = '4'
                              option 'A little' value = '3'
                              option 'So-so' value = '2'
                              option 'Yes' value = '1'
                              option 'Too much' value = '0'
                          uiRef = 'colors(0<=red<=1<yellow<=2<=green<=4)'    
                              
                      InputField CoughOutMucus
                          #left #singlechoice
                          question = 'Can you cough your mucus out?'
                              option 'No' value = '0'
                              option 'Yes' value = '1'
                      
                  
          Stage Discharge
              #mandatory #manualActivate
              owner = 'Setting.CaseOwner'
              label = 'Discharge'
              
              precondition
                  previousStep = 'Identification'
              
              HumanTask DischargePatient
                  #mandatory
                  owner = 'Setting.CaseOwner'
                  label = 'Discharge Patient'
                  
                  Form DischargeForm
                      InputField DoctorNote 
                          #text
                          label = 'Post-Treatment Recommendation:'
        
"""

