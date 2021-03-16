from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util
from acadela.case_object.entity import Entity
from acadela.case_object.task import Task

import json
import sys

# Dynamic Field is DerivedAttribute in SACM
def interpret_dynamic_field(field):
    fieldEntityList = []
    fieldObjectList = []

    directive = field.directive

    # taskObject = Task(field.id, attrList.description.value,
    #                   util.cname(field),
    #                   None,  # to be replaced by taskParamList
    #                   ownerPath,
    #                   dueDatePath,
    #                   directive.repeatable,
    #                   directive.mandatory,
    #                   directive.activation,
    #                   dynamicDescriptionPath,
    #
    #                   )

    print("\n\tField {}"
          "\n\t\tfieldTypes = {}"
          "\n\t\tDirectives "
          "\n\t\t\tmandatory = {}"
          "\n\t\t\treadOnly = {}"
          "\n\t\t\tposition = {}"
          "\n\t\t\texplicitType = {}"
          "\n\t\tdescription = {}"
          "\n\t\tadditionalDescription = {}"
          "\n\t\tuiRef = {}"
          "\n\t\texpression = {}"
          "\n\t\texternalId = {}"
          # "\n\t\townerPath = {}"
          # "\n\t\tdueDatePath = {}"
          # "\n\t\texternalId = {}"
          # "\n\t\tdynamicDescriptionPath = {}"
          .format(field.id,
                  util.cname(field),
                  directive.mandatory,
                  "None" if directive.readOnly is None else directive.readOnly,
                  "None" if directive.position is None else directive.position,
                  "None" if directive.explicitType is None else directive.multiplicity,
                  field.description.value,
                  "None" if field.additionalDescription is None else field.additionalDescription.value,
                  "None" if field.uiRef is None else field.uiRef,
                  "None" if field.expression is None else field.expression,
                  "None" if field.externalId is None else field.externalId))

    return {"taskEntity": fieldEntityList, "taskObject": fieldObjectList}
