from acadela.sacm.case_object.sentry import Precondition
import acadela.sacm.util as util
import acadela.sacm.interpreter.util_intprtr as util_intprtr

def interpret_precondition(preconditionObj, process=None):
    sentryStepList = []
    entryCondition = None

    for step in preconditionObj.stepList:
        # stepStr = str(step)
        # stepObjList =  stepStr.split('.')
        # for stepObj in stepObjList:
        #     stepStr = stepStr.replace(stepObj, \
        #                         util.prefixing(stepObj))

        stepStr = util_intprtr.prefix_path_value(str(step), True)
        # stepStr = str(step)
        sentryStepList.append(stepStr)

    if util.is_attribute_not_null(preconditionObj, 'entryCondition'):
        entryCondition = util_intprtr.prefix_path_value(
                            preconditionObj.entryCondition,
                            False
        )

    return Precondition(sentryStepList, entryCondition)


