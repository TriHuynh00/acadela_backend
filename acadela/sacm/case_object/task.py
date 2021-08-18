from sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)


class Task():
    def __init__(self, id, description,
                 multiplicity,
                 valueType,
                 taskType,
                 fieldList,
                 dynamicFieldList,
                 ownerPath,
                 dueDatePath,
                 repeatable,
                 mandatory,
                 activation,
                 manualActivationExpression,
                 externalId,
                 addtionalDescription,
                 dynamicDescriptionPath,
                 preconditionList,
                 hookList,
                 entityAttachPath = None,
                 entityDefinitionId = None,
                 isPrefixed = True):

        if isPrefixed:
            self.id = util.prefixing(id)
        else:
            self.id = id

        if entityDefinitionId is None:
            self.entityDefinitionId = self.id
        else:
            self.entityDefinitionId = entityDefinitionId

        self.multiplicity = multiplicity
        self.valueType = valueType

        self.taskType = taskType
        self.description = description
        self.fieldList = fieldList
        self.dynamicFieldList = dynamicFieldList
        self.ownerPath = ownerPath
        self.dueDatePath = dueDatePath
        self.repeatable = repeatable
        self.isMandatory = mandatory
        self.activation = activation
        self.manualActivationExpression = manualActivationExpression
        self.entityAttachPath = entityAttachPath
        self.externalId = externalId
        self.addtionalDescription = addtionalDescription
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.preconditionList = preconditionList
        self.hookList = hookList

    # def print(self):
    #     print("\n\tTask {}"
    #           "\n\t\tDirectives "
    #           "\n\t\t\tmandatory = {}"
    #           "\n\t\t\trepeatable = {}"
    #           "\n\t\t\tactivation = {}"
    #           "\n\t\t\tmultiplicity = {}"
    #           "\n\t\tdescription = {}"
    #           "\n\t\townerPath = {}"
    #           "\n\t\tdueDatePath = {}"
    #           "\n\t\texternalId = {}"
    #           "\n\t\tdynamicDescriptionPath = {}"
    #           .format(self.id,
    #                   mandatory,
    #                   repeatable,
    #                   activation,
    #                   multiplicity,
    #                   attrList.description.value,
    #                   (None if attrList.ownerPath is None else attrList.ownerPath.value),
    #                   dueDatePath,
    #                   ("None" if attrList.externalId is None else attrList.externalId.value),
    #                   ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))


