from acadela.sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

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
        self.manualActivationDescription = manualActivationExpression
        self.entityAttachPath = entityAttachPath
        self.externalId = externalId
        self.addtionalDescription = addtionalDescription
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.preconditionList = preconditionList
        self.hookList = hookList


