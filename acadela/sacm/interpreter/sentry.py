from acadela.sacm.case_object.sentry import Precondition
import acadela.sacm.util as util

def interpret_precondition(preconditionObj):
    sentryStepList = []
    for step in preconditionObj.stepList:
        stepStr = str(step)
        stepObjList =  stepStr.split('.')
        for stepObj in stepObjList:
            stepStr = stepStr.replace(stepObj, \
                                util.prefixing(stepObj))
        # TODO [Validation]: Check Sentry ID matches with Stage/Task/Field Object
        sentryStepList.append(stepStr)


    return Precondition(sentryStepList,
                        preconditionObj.entryCondition)


