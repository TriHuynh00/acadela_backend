from acadela.sacm.case_object.sentry import Precondition

def interpret_precondition(preconditionObj):
    return Precondition(preconditionObj.stepList,
                        preconditionObj.entryCondition)


