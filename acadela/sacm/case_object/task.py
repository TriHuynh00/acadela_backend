from acadela.sacm import util, default_state

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class Task():
    def __init__(self, id, description,
                 taskType,
                 taskParamList = [],
                 ownerPath = None,
                 dueDatePath = None,
                 repeatable = default_state.defaultAttributeMap['repeat'],
                 mandatory = default_state.defaultAttributeMap['mandatory'],
                 activation = default_state.defaultAttributeMap['activation'],
                 manualActivationExpression = None,
                 externalId = None,
                 dynamicDescriptionPath = None,
                 isPrefixed = True,
                 precondition = None,
                 hook = None):

        if isPrefixed:
            self.id = util.prefixing(id)
        else:
            self.id = id

        self.taskType = taskType
        self.description = description
        self.taskParamList = taskParamList
        self.ownerPath = ownerPath
        self.dueDatePath = dueDatePath
        self.repeatable = repeatable
        self.mandatory = mandatory
        self.activation = activation
        self.manualActivationDescription = manualActivationExpression
        self.externalId = externalId
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.precondition = precondition
        self.hook = hook


