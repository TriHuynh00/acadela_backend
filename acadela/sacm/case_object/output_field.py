from os.path import dirname

from sacm.case_object.field import Field
from sacm.default_state import defaultAttrMap
import sacm.util as util
import sys

this_folder = dirname(__file__)


# TaskParamDefinition
class OutputField:
    def __init__(self, id, description,
                 explicityType,
                 additionalDescription,
                 expression,
                 uiRef,
                 externalId,
                 path,
                 position,
                 part,
                 readOnly,
                 mandatory,
                 defaultValue,
                 defaultValues,
                 lineNumber):

        self.explicitType = explicityType
        self.expression = expression
        Field.__init__(self, id, description,
                       uiRef,
                       externalId,
                       path,
                       position,
                       part,
                       readOnly,
                       mandatory,
                       defaultValue,
                       defaultValues,
                       lineNumber,
                       additionalDescription)

