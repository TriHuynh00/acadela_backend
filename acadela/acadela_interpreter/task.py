from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util
from acadela.case_object.entity import Entity
from acadela.case_object.task import Task

import json
import sys

def interpret_task(taskList):
    taskEntityList = []
    taskObjectList = []

    for task in taskList:
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

        taskObject = Task(task.id, attrList.description.value,
                          util.cname(task),
                          None, # to be replaced by taskParamList
                          ownerPath,
                          dueDatePath,
                          directive.repeatable,
                          directive.mandatory,
                          directive.activation,
                          dynamicDescriptionPath,

                          )

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