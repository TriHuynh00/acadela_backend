import re

from sacm.case_object.sentry import Precondition
import sacm.util as util
import sacm.interpreter.util_intprtr as util_intprtr

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
        # entryCondition = util_intprtr.prefix_path_value(
        #                     preconditionObj.entryCondition,
        #                     False)
        entryCondition = preconditionObj.entryCondition

    return Precondition(sentryStepList, entryCondition)

def auto_parse_conditional_expression(entryCondition):
    subjAndPredicate = re.split('[<>(<=)(>=)==]', entryCondition)

    predicate = str.strip(subjAndPredicate[1])
    operator = re.findall('[<>(<=)(>=)==]', entryCondition)[-1]

    print("operator=", operator, "predicate=", predicate)

    if str.isdigit(predicate):
        subjAndPredicate[0] = 'number(' + subjAndPredicate[0] + ', 0)'
    elif str.isdecimal(predicate):
        subjAndPredicate[0] = 'number(' + subjAndPredicate[0] + ', 2)'

    entryCondition = subjAndPredicate[0] + operator + predicate

    print("Entry Condition after parse to number:", entryCondition)
    return entryCondition

