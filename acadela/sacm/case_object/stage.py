from sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)


class Stage():
    def __init__(self, id, description,
                 multiplicity,
                 type,
                 ownerPath,
                 taskList,
                 additionalDescription,
                 externalId,
                 repeatable,
                 mandatory,
                 activation,
                 manualActivationExpression,
                 dynamicDescriptionPath,
                 preconditionList,
                 lineNumber,
                 entityDefinitionId = None,
                 entityAttachPath=None,
                 isPrefixed = True
                 ):

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

        self.type = type
        self.description = description
        self.additionalDescription = additionalDescription
        self.ownerPath = ownerPath
        self.repeatable = repeatable
        self.mandatory = mandatory
        self.activation = activation
        self.multiplicity = multiplicity
        self.manualActivationDescription = manualActivationExpression
        self.externalId = externalId
        self.dynamicDescriptionPath = dynamicDescriptionPath

        self.taskList = taskList
        self.preconditionList = preconditionList
        self.lineNumber = lineNumber



