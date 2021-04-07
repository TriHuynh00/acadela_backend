from acadela.sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class Task():
    def __init__(self, id, description,
                 taskType,
                 fieldList = [],
                 dynamicFieldList = [],
                 ownerPath = None,
                 dueDatePath = None,
                 repeatable = default_state.attrMap['repeat'],
                 mandatory = default_state.attrMap['mandatory'],
                 activation = default_state.attrMap['activation'],
                 manualActivationExpression = None,
                 externalId = None,
                 dynamicDescriptionPath = None,
                 precondition = None,
                 hook = None,
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

        self.taskType = taskType
        self.description = description
        self.fieldList = fieldList
        self.dynamicFieldList = dynamicFieldList
        self.ownerPath = ownerPath
        self.dueDatePath = dueDatePath
        self.repeatable = repeatable
        self.mandatory = mandatory
        self.activation = activation
        self.manualActivationDescription = manualActivationExpression
        self.entityAttachPath = entityAttachPath
        self.externalId = externalId
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.precondition = precondition
        self.hook = hook


