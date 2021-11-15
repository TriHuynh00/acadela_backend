from sacm.default_state import defaultAttrMap

from os.path import dirname
import sys

this_folder = dirname(__file__)


class SummarySection:
    def __init__(self, id, description,
                 summaryParamList,
                 lineNumber,
                 position=defaultAttrMap['position']):
        self.id = id
        self.description = description
        self.summaryParamList = summaryParamList
        self.position = position
        self.lineNumber = lineNumber