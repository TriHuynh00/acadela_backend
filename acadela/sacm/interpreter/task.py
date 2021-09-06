from sacm.interpreter import util_intprtr

from sacm import util
from sacm.interpreter.sentry import interpret_precondition
import sacm.interpreter.hook as hookInterpreter
import sacm.interpreter.directive as direc_intprtr
import sacm.interpreter.field as fieldInterpreter

from sacm import default_state

import sacm.constant.task_type as TASKTYPE

from sacm.case_object.entity import Entity
from sacm.case_object.task import Task
from sacm.case_object.attribute import Attribute


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
            dueDatePath = util_intprtr.prefix_path_value(
                attrList.dueDatePath.value, False
            )

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
            preconditionList.append(
                interpret_precondition(sentry, process = task)
            )

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

    # For DynamicFields (DerivedAttribute), number should be rounded with round()
    # string should be converted to number with number(string, 0)
    for dynamicField in dynamicFieldList:
        dynaExpression = fieldInterpreter\
            .auto_convert_expression(
                dynamicField,
                fieldList
            )

        for attrField in fieldAsAttributeList:
            if attrField.id == dynamicField.id:
                attrField.expression = dynaExpression
                break

        print("dynaExpression =", dynaExpression)


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

def sacm_compile(taskList, stageList):
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
             'manualActivationExpression',
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
                    util_intprtr.parse_precondition(task, stageList)

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


