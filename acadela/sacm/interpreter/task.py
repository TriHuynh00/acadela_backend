from acadela.sacm import util
import acadela.sacm.interpreter.sentry as preconditionInterpreter
import acadela.sacm.interpreter.hook as hookInterpreter
import acadela.sacm.interpreter.directive as direc_intprtr
import acadela.sacm.default_state as default_state

from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.task import Task


def interpret_task(task):
    taskEntityList = []
    taskObjectList = []
    taskHookList = []
    precondition = None

    directive = task.directive
    attrList = task.attrList
    dueDatePath = None

    if util.cname(task) != 'AutomatedTask':
        if attrList.dueDatePath is not None:
            dueDatePath = attrList.dueDatePath.value

    taskEntity = Entity(task.id, attrList.description.value)

    #TODO add fields as task attributes

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

    activation = default_state.defaultAttributeMap['activation']\
        if not hasattr(directive, 'activation')\
        else direc_intprtr.\
                interpret_directive(directive.activation)
    manualActivationExpression = None

    if activation is not None and \
            activation.startswith("activateWhen"):
        manualActivationExpression = activation.split('(')[1][:-1]

    repeatable = default_state.defaultAttributeMap['repeat'] \
        if not hasattr(directive, 'repeatable') \
        else direc_intprtr. \
            interpret_directive(directive.repeatable)

    mandatory = direc_intprtr.\
        interpret_directive(directive.mandatory)

    multiplicity = default_state.defaultAttributeMap['multiplicity']\
        if directive.multiplicity is None\
        else direc_intprtr.\
            interpret_directive(directive.multiplicity)

    taskObject = Task(task.id, attrList.description.value,
                      util.cname(task),
                      None, # to be replaced by taskParamList
                      ownerPath,
                      dueDatePath,
                      repeatable,
                      mandatory,
                      activation,
                      manualActivationExpression,
                      dynamicDescriptionPath,
                      precondition,
                      taskHookList)

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

    return {"taskEntity": taskEntityList, "taskObject": taskObjectList}