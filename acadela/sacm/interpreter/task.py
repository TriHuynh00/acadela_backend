from acadela.sacm.interpreter import util_intprtr

from acadela.sacm import util
from acadela.sacm.interpreter.sentry import interpret_precondition
import acadela.sacm.interpreter.hook as hookInterpreter
import acadela.sacm.interpreter.directive as direc_intprtr
import acadela.sacm.interpreter.field as fieldInterpreter

from acadela.sacm.default_state import defaultAttrMap

import acadela.sacm.constant.task_type as TASKTYPE

from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.task import Task
from acadela.sacm.case_object.attribute import Attribute


def interpret_task(task, stageId):
    
    taskId = util.prefixing(task.id)
    stageId = util.prefixing(stageId)
    
    taskHookList = []
    taskType = util.cname(task)

    preconditionList = []
    directive = task.directive
    attrList = task.attrList
    dueDatePath = None
    fieldList = []
    dynamicFieldList = []

    fieldAsAttributeList = []

    if util.cname(task) != 'AutomatedTask':
        if attrList.dueDatePath is not None:
            dueDatePath = attrList.dueDatePath.value

    ownerPath = None \
        if attrList.ownerPath is None \
        else attrList.ownerPath.value

    dynamicDescriptionPath = None \
        if attrList.dynamicDescriptionPath is None \
        else attrList.dynamicDescriptionPath.value

    # preconditionObj = None \
    #     if not hasattr(attrList, "preconditionList") \
    #     else attrList.preconditionList
    #
    # if preconditionObj is not None:
    #
    #     precondition.append(interpret_precondition(preconditionObj))

    if hasattr(task, "hookList"):
        for hook in task.hookList:
            interpretedHook = hookInterpreter.interpret_http_hook(hook)
            print("HttpHook", vars(interpretedHook))
            taskHookList.append(interpretedHook)

    preconditionObj = attrList.preconditionList \
        if util.is_attribute_not_null(attrList, 'preconditionList') \
        else None

    if preconditionObj is not None:
        print("Task Precondition", [sentry for sentry in preconditionObj])
        for sentry in preconditionObj:
            preconditionList.append(interpret_precondition(sentry))

    print("Task Sentry List", preconditionList)
    # Interpret Directive

    activation = defaultAttrMap['activation']\
        if not hasattr(directive, 'activation')\
        else direc_intprtr.\
                interpret_directive(directive.activation)
    manualActivationExpression = None

    if activation is not None and \
            activation.startswith("activateWhen"):
        manualActivationExpression = activation.split('(')[1][:-1]

    repeatable = defaultAttrMap['repeat'] \
        if not hasattr(directive, 'repeatable') \
        else direc_intprtr. \
                interpret_directive(directive.repeatable)

    mandatory = defaultAttrMap['mandatory']\
        if not hasattr(directive, 'mandatory')\
        else direc_intprtr.\
                interpret_directive(directive.mandatory)

    multiplicity = defaultAttrMap['multiplicity']\
        if directive.multiplicity is None\
        else direc_intprtr.\
                interpret_directive(directive.multiplicity)
    
    typeValue = defaultAttrMap['type'] \
        if not hasattr(directive, 'type') \
        else direc_intprtr. \
            interpret_directive(directive.type)

    externalId = None\
        if attrList.externalId is None\
        else attrList.externalId.value

    extraDescription = None \
        if attrList.additionalDescription is None \
        else attrList.additionalDescription.value

    # Interpret task fields (TaskParam)

    for field in task.form.fieldList:
        interpretedFieldTuple = None
        if util.cname(field) == "Field":
            fieldPath = "{}.{}.{}".format(
                stageId,
                taskId,
                field.id)

            interpretedFieldTuple = fieldInterpreter\
                .interpret_field(field, fieldPath, taskType)

            fieldList.append(interpretedFieldTuple['fieldAsTaskParam'])

        elif util.cname(field) == "DynamicField":
            interpretedFieldTuple = fieldInterpreter \
                .interpret_dynamic_field(field, fieldPath, taskType)
            dynamicFieldList.append(interpretedFieldTuple['fieldAsTaskParam'])

        fieldAsAttributeList.append(interpretedFieldTuple['fieldAsAttribute'])

    taskEntity = Entity(taskId, attrList.description.value,
                        fieldAsAttributeList)

    entityAttachPath = '{}.{}'.format(stageId, taskId)

    taskObject = Task(taskId, attrList.description.value,
                      multiplicity, typeValue,
                      util.cname(task),
                      fieldList,
                      dynamicFieldList,
                      ownerPath,
                      dueDatePath,
                      repeatable,
                      mandatory,
                      activation,
                      manualActivationExpression,
                      externalId,
                      extraDescription,
                      dynamicDescriptionPath,
                      preconditionList,
                      taskHookList,
                      entityAttachPath)

    taskAsAttribute = Attribute(taskId,
                                attrList.description,
                                multiplicity, typeValue,
                                externalId = externalId)

    print("\n\tTask {}"
          "\n\t\tDirectives "
          "\n\t\t\tmandatory = {}"
          "\n\t\t\trepeatable = {}"
          "\n\t\t\tactivation = {}"
          "\n\t\t\tmultiplicity = {}"
          "\n\t\tdescription = {}"
          "\n\t\townerPath = {}"
          "\n\t\tdueDatePath = {}"
          "\n\t\texternalId = {}"
          "\n\t\tdynamicDescriptionPath = {}"
          .format(taskId,
                  mandatory,
                  repeatable,
                  activation,
                  multiplicity,
                  attrList.description.value,
                  (None if attrList.ownerPath is None else attrList.ownerPath.value),
                  dueDatePath,
                  ("None" if attrList.externalId is None else attrList.externalId.value),
                  ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))

    return taskObject

def sacm_compile(taskList):
    humanTaskList = []
    autoTaskList = []
    dualTaskList = []

    for task in taskList:
        taskJson = {
            '$': {}
        }

        if task.taskType == TASKTYPE.HUMAN:
            print("Task Type SACM is {}".format(task.taskType))
            taskAttr = taskJson['$']

            taskAttr['id'] = task.id
            taskAttr['description'] = task.description

            util.compile_attributes(taskAttr, task,
                ['ownerPath', 'dueDatePath', 'repeatable',
                 'isMandatory', 'activation',
                 'manualActivationDescription',
                 'entityDefinitionId', 'entityAttachPath',
                 'externalId', 'dynamicDescriptionPath'])

            if hasattr(task, 'preconditionList'):
                taskJson['SentryDefinition'] = \
                    util_intprtr.parse_precondition(task)

            humanTaskList.append(taskJson)


    return {
        'humanTaskList': humanTaskList,
        'autoTaskList': autoTaskList,
        'dualTaskList': dualTaskList
    }

