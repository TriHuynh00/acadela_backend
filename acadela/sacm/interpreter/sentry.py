import re

from sacm.case_object.sentry import Precondition
import sacm.util as util
import sacm.default_state as default_state
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
    prefixedCondition = ''
    clauses = re.split('( and )|( or )', entryCondition)

    for clause in clauses:
        print ("Clause is", clause)
        clause = str(clause).strip()
        if clause in ['and', 'or', 'None']:
            if clause in ['and', 'or']:
                prefixedCondition += ' {} '.format(clause)
            continue

        subjAndPredicate = re.split('[<>=][=]*', clause)

        subjects = re.findall('[\w+\.]+\w+', subjAndPredicate[0])

        predicate = ''

        if len(subjAndPredicate) == 2:
            predicate = str.strip(subjAndPredicate[1])

        operator = ''
        operatorVals = re.findall('[<>=][=]*', clause)
        if len(operatorVals) > 0:
            operator = operatorVals[-1]

        print("entryCond=", entryCondition,
              "clause=", clause,
              "subjects=", subjects,
              "operator=", operator,
              "predicate=", predicate)

        subjectPhrase = subjAndPredicate[0]

        for subject in subjects:
            fieldType = ''

            subjectPrev = subject

            subElements = subject.split(".")

            if len(subElements) <= 1:
                subject = util_intprtr.prefix_path_value(subject, True)

            elif len(subElements) == 2:
                if str(subject).startswith(default_state.SETTING_NAME):
                    subject = util_intprtr.prefix_path_value(subject, False)
                else:
                    subject = util_intprtr.prefix_path_value(subject, True)
            else:
                for stage in stageList:
                    if stage.id == util.prefixing(subElements[-1]):
                        subject = util_intprtr.prefix_path_value(subject, True)
                        break
                    for task in stage.taskList:
                        # If the task is the last element of the path, prefix all elements
                        if task.id == util.prefixing(subElements[-1]):
                            subject = util_intprtr.prefix_path_value(subject, True)
                            break
                        # if the task is the second last element, check the type of the field in the task
                        elif task.id == util.prefixing(subElements[-2]) and len(subElements) > 1:
                            for field in task.fieldList:
                                if field.id == subElements[-1]:
                                    if 'number' in str(field.type):
                                        fieldType = 'number'
                                        # No task or stage matches the path element, so this is a field\
                                        break

                subject = util_intprtr.prefix_path_value(subject, False)

            if str.isdecimal(predicate.replace(')', '')) and fieldType != 'number':
                subject = 'number(' + subject + ', 2)'

            subjectPhrase = subjectPhrase.replace(subjectPrev, subject)

        prefixedCondition += subjectPhrase + operator + predicate

    print("Prefixed Condition after parse to number:", prefixedCondition)
    return prefixedCondition

