from acadela.sacm import util
import acadela.sacm.interpreter.sentry as preconditionInterpreter
import acadela.sacm.interpreter.hook as hookInterpreter
import acadela.sacm.interpreter.directive as direc_intprtr
import acadela.sacm.interpreter.field as fieldInterpreter

from acadela.sacm.default_state import attrMap

from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.task import Task
from acadela.sacm.case_object.attribute import Attribute


def interpret_task(task, stageId):
    taskHookList = []
    taskType = util.cname(task)

    precondition = None
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

    preconditionObj = None \
        if not hasattr(attrList, "precondition") \
        else attrList.precondition

    if preconditionObj is not None:

        print("Precondition", [step for step in preconditionObj.stepList])
        precondition = \
            preconditionInterpreter.interpret_precondition(preconditionObj)

    if hasattr(task, "hookList"):
        for hook in task.hookList:
            interpretedHook = hookInterpreter.interpret_http_hook(hook)
            print("HttpHook", vars(interpretedHook))
            taskHookList.append(interpretedHook)

    # Interpret Directive

    activation = attrMap['activation']\
        if not hasattr(directive, 'activation')\
        else direc_intprtr.\
                interpret_directive(directive.activation)
    manualActivationExpression = None

    if activation is not None and \
            activation.startswith("activateWhen"):
        manualActivationExpression = activation.split('(')[1][:-1]

    repeatable = attrMap['repeat'] \
        if not hasattr(directive, 'repeatable') \
        else direc_intprtr. \
            interpret_directive(directive.repeatable)

    mandatory = direc_intprtr.\
        interpret_directive(directive.mandatory)

    multiplicity = attrMap['multiplicity']\
        if directive.multiplicity is None\
        else direc_intprtr.\
            interpret_directive(directive.multiplicity)
    
    typeValue = attrMap['type'] \
        if not hasattr(directive, 'type') \
        else direc_intprtr. \
            interpret_directive(directive.type)

    externalId = None\
        if attrList.externalId is None\
        else attrList.externalId.value

    # Interpret task fields (TaskParam)

    for field in task.form.fieldList:
        interpretedFieldTuple = None
        if util.cname(field) == "Field":
            fieldPath = "{}.{}.{}".format(
                util.prefixing(stageId),
                task.id,
                field.id)

            interpretedFieldTuple = fieldInterpreter\
                .interpret_field(field, fieldPath, taskType)

            fieldList.append(interpretedFieldTuple['fieldAsTaskParam'])

        elif util.cname(field) == "DynamicField":
            interpretedFieldTuple = fieldInterpreter \
                .interpret_dynamic_field(field, fieldPath, taskType)
            dynamicFieldList.append(interpretedFieldTuple['fieldAsTaskParam'])

        fieldAsAttributeList.append(interpretedFieldTuple['fieldAsAttribute'])

    taskEntity = Entity(task.id, attrList.description.value,
                        fieldAsAttributeList)

    entityAttachPath = '{}.{}'.format(util.prefixing(stageId),\
                                      task.id)
    taskObject = Task(task.id, attrList.description.value,
                      util.cname(task),
                      fieldList,
                      ownerPath,
                      dueDatePath,
                      repeatable,
                      mandatory,
                      activation,
                      manualActivationExpression,
                      dynamicDescriptionPath,
                      precondition,
                      taskHookList,
                      entityAttachPath)

    taskAsAttribute = Attribute(task.id,
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
          .format(task.id,
                  mandatory,
                  repeatable,
                  activation,
                  multiplicity,
                  attrList.description.value,
                  (None if attrList.ownerPath is None else attrList.ownerPath.value),
                  dueDatePath,
                  ("None" if attrList.externalId is None else attrList.externalId.value),
                  ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))

    return { "taskAsEntity": taskEntity,
             "task": taskObject,
             "taskAsAttribute": taskAsAttribute }