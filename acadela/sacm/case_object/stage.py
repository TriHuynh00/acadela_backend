from acadela.sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class Stage():
    def __init__(self, id, description,
                 ownerPath = None,
                 repeatable = default_state.attrMap['repeat'],
                 mandatory = default_state.attrMap['mandatory'],
                 activation = default_state.attrMap['activation'],
                 multiplicity = default_state.attrMap['multiplicity'],
                 manualActivationExpression = None,
                 externalId = None,
                 dynamicDescriptionPath = None,
                 entityAttachPath = None,
                 taskList = [],
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

        if entityAttachPath is None:
            self.entityAttachPath = self.id
        else:
            self.entityAttachPath = entityAttachPath

        self.description = description
        self.ownerPath = ownerPath
        self.repeatable = repeatable
        self.mandatory = mandatory
        self.activation = activation
        self.multiplicity = multiplicity
        self.manualActivationDescription = manualActivationExpression
        self.externalId = externalId
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.taskList = taskList



