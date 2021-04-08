from os.path import dirname
from acadela.sacm.default_state import defaultAttrMap
import acadela.sacm.util as util
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TaskParamDefinition
class DynamicField:
    def __init__(self, id, description,
                 explicityType,
                 additionalDescription,
                 expression,
                 uiReference,
                 externalId,
                 path,
                 isReadOnly,
                 isMandatory,
                 position,
                 part):

        self.id = id
        self.description = description
        self.explicitType = explicityType
        self.additionalDescription = additionalDescription
        self.expression = expression
        self.uiReference = uiReference
        self.externalId = externalId
        # Task Param
        self.path = path
        self.readOnly = isReadOnly
        self.mandatory = isMandatory
        self.position = position
        self.part = part

