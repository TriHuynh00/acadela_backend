from os.path import dirname
from sacm.default_state import defaultAttrMap
import sacm.util as util
import sys

this_folder = dirname(__file__)


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
        self.isReadOnly = isReadOnly
        self.isMandatory = isMandatory
        self.position = position
        self.part = part

