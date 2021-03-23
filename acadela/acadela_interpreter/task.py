from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util
import acadela.acadela_interpreter.sentry as preconditionInterpreter
import acadela.acadela_interpreter.hook as hookInterpreter

from acadela.case_object.entity import Entity
from acadela.case_object.task import Task


import json
import sys

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

    taskObject = Task(task.id, attrList.description.value,
                      util.cname(task),
                      None, # to be replaced by taskParamList
                      ownerPath,
                      dueDatePath,
                      directive.repeatable,
                      directive.mandatory,
                      directive.activation,
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
                  directive.mandatory,
                  directive.repeatable,
                  directive.activation,
                  directive.multiplicity,
                  attrList.description.value,
                  (None if attrList.ownerPath is None else attrList.ownerPath.value),
                  dueDatePath,
                  ("None" if attrList.externalId is None else attrList.externalId.value),
                  ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))

    return {"taskEntity": taskEntityList, "taskObject": taskObjectList}