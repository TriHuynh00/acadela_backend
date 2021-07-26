from acadela.sacm.interpreter import util_intprtr

from acadela.sacm import util
from acadela.sacm.interpreter.sentry import interpret_precondition
import acadela.sacm.interpreter.hook as hookInterpreter
import acadela.sacm.interpreter.directive as direc_intprtr
import acadela.sacm.interpreter.field as fieldInterpreter

from acadela.sacm import default_state

import acadela.sacm.constant.task_type as TASKTYPE

from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.task import Task
from acadela.sacm.case_object.attribute import Attribute


def interpret_task(task, stageId):

    taskId = util.prefixing(task.name)
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
        if util.is_attribute_not_null(attrList, 'dueDatePath'):
            dueDatePath = util.prefixingSetting( \
                attrList.dueDatePath.value)


    ownerPath = None \
        if attrList.ownerPath is None \
        else attrList.ownerPath.value

    ownerPath = util.prefixingSetting(ownerPath)

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
            hook = util.getRefOfObject(hook)
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

    activationParse = util_intprtr.parse_activation(directive)

    activation = activationParse['activation']
    manualActivationExpression = \
        activationParse['manualActivationExpression']

    repeatable = default_state.defaultAttrMap['repeat'] \
        if not hasattr(directive, 'repeatable') \
        else direc_intprtr. \
                interpret_directive(directive.repeatable)

    mandatory = default_state.defaultAttrMap['mandatory']\
        if not hasattr(directive, 'mandatory')\
        else direc_intprtr.\
                interpret_directive(directive.mandatory)

    multiplicity = default_state.defaultAttrMap['multiplicity']\
        if directive.multiplicity is None\
        else direc_intprtr.\
                interpret_directive(directive.multiplicity)
    
    typeValue = default_state.ENTITY_LINK_TYPE + '.' + taskId

    externalId = None\
        if attrList.externalId is None\
        else attrList.externalId.value

    extraDescription = None \
        if attrList.additionalDescription is None \
        else attrList.additionalDescription.value

    # Interpret task fields (TaskParam)
    taskForm = util.getRefOfObject(task.form)

    for field in taskForm.fieldList:
        field = util.getRefOfObject(field)
        formDirective = taskForm.directive
        interpretedFieldTuple = None

        fieldPath = "{}.{}.{}".format(
            stageId,
            taskId,
            field.name)

        if util.cname(field) == "Field":

            interpretedFieldTuple = fieldInterpreter\
                .interpret_field(field, fieldPath,\
                                 taskType, formDirective)

            fieldList.append(interpretedFieldTuple['fieldAsTaskParam'])

        elif util.cname(field) == "DynamicField":

            interpretedFieldTuple = fieldInterpreter \
                .interpret_dynamic_field(field, fieldPath,
                                         taskType, formDirective)

            dynamicFieldList.append(interpretedFieldTuple['fieldAsTaskParam'])
            # dynamicFieldList.append(dynamicFieldList)

        fieldAsAttributeList.append(interpretedFieldTuple['fieldAsAttribute'])

    taskAsEntity = Entity(taskId, attrList.description.value,
                        fieldAsAttributeList, isPrefixed=False)

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
                      entityAttachPath,
                      isPrefixed=False)

    taskAsAttribute = Attribute(taskId,
                                attrList.description,
                                multiplicity, typeValue,
                                externalId = externalId)

    return {
        'task': taskObject,
        'taskAsEntity': taskAsEntity,
        'taskAsAttribute': taskAsAttribute
    }

def sacm_compile(taskList):
    jsonTaskList = []
    # humanTaskList = []
    # autoTaskList = []
    # dualTaskList = []

    for task in taskList:
        taskJson = {
            '$': {}
        }

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

        if task.taskType == TASKTYPE.HUMAN:
            taskJson['#name'] = default_state.HUMAN_TASK_DEF

        elif task.taskType == TASKTYPE.AUTO:
            taskJson['#name'] = default_state.AUTO_TASK_DEF

        elif task.taskType == TASKTYPE.DUAL:
            taskJson['#name'] = default_state.DUAL_TASK_DEF

        if util.is_attribute_not_null(task, 'preconditionList'):
            if len(task.preconditionList) > 0 != None:
                taskJson['SentryDefinition'] = \
                    util_intprtr.parse_precondition(task)

        if util.is_attribute_not_null(task, 'hookList'):
            if len(task.hookList) > 0:
                taskJson['HttpHookDefinition'] = \
                    hookInterpreter.sacm_compile(task.hookList)

        # compile Task Params
        print (task.id, "fields size:", len(task.fieldList))
        if len(task.fieldList) > 0:
            taskFields = task.fieldList

            for dynaField in task.dynamicFieldList:
                taskFields.append(dynaField)

            taskJson['TaskParamDefinition'] = \
                fieldInterpreter.sacm_compile(taskFields)

        jsonTaskList.append(taskJson)

    return jsonTaskList
        # 'humanTaskList': humanTaskList,
        # 'autoTaskList': autoTaskList,
        # 'dualTaskList': dualTaskList


