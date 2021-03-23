from acadela.acadela_interpreter import util
from acadela.default_state import config

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
                 repeatable = config.defaultAttributeMap['repeat'],
                 mandatory = config.defaultAttributeMap['mandatory'],
                 activation = config.defaultAttributeMap['activation'],
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

        if activation is not None and \
                activation.startswith("activateWhen"):
            self.manualActivationDescription = activation.split('(')[1][:-1]
        else:
            self.manualActivationDescription = None

        self.externalId = externalId
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.precondition = precondition
        self.hook = hook


