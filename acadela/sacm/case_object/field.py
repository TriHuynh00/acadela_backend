from os.path import dirname
import acadela.sacm.default_state as defaultState
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TaskParamDefinition
class Field:
    def __init__(self, path,
                 isReadOnly = None,
                 isMandatory = None,
                 position = defaultState.defaultAttributeMap['position'],
                 part = None):

        self.path = path
        self.readOnly = isReadOnly
        self.mandatory = isMandatory
        self.position = position
        self.part = part
