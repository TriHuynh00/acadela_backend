from os.path import dirname
from sacm.default_state import defaultAttrMap
import sacm.util as util
import sys

this_folder = dirname(__file__)


# TaskParamDefinition
class Field:
    def __init__(self, id, description,
                 question,
                 multiplicity,
                 type,
                 path,
                 isReadOnly,
                 isMandatory,
                 position,
                 uiRef,
                 externalId,
                 part):

        self.id = id
        self.description = description
        self.question = question
        self.path = path
        self.isReadOnly = isReadOnly
        self.isMandatory = isMandatory
        self.position = position
        self.part = part
        self.multiplicity = multiplicity
        self.uiRef = uiRef
        self.externalId = externalId
        self.type = type
