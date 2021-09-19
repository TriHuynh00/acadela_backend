import re

from sacm.case_object.sentry import Precondition
import sacm.util as util
from sacm.interpreter import util_intprtr

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

def auto_parse_conditional_expression(entryCondition, stageList):
    subjAndPredicate = re.split('[<>=][=]*', entryCondition)

    subject = re.findall('[\w+\.]+\w+', subjAndPredicate[0])[0]

    predicate = str.strip(subjAndPredicate[1])
    operator = re.findall('[<>=][=]*', entryCondition)[-1]

    print("entryCond=", entryCondition,
          "subject=", subject,
          "operator=", operator,
          "predicate=", predicate)

    subElements = subject.split(".")

    if len(subElements) <= 2:
        for element in subElements:
            subject = util_intprtr.prefix_path_value(subject, True)
    else:
        for stage in stageList:
            if stage.id == subElements[-1]:
                subject = util_intprtr.prefix_path_value(subject, True)
                break
            for task in stage.taskList:
                if task.id == subElements[-1]:
                    subject = util_intprtr.prefix_path_value(subject, True)
                    break
        # No task or stage matches the path element, so this is a field
        subject = util_intprtr.prefix_path_value(subject, False)

    if str.isdigit(predicate):
        subject = 'number(' + subject + ', 0)'
    elif str.isdecimal(predicate):
        subject = 'number(' + subject + ', 2)'

    entryCondition = subject + operator + predicate

    print("Entry Condition after parse to number:", entryCondition)
    return entryCondition

