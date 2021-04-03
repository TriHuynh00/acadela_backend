from acadela.sacm.default_state import defaultAttributeMap

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class SummarySection:
    def __init__(self, id, description,
                 summaryParamList,
                 position = None):
        self.id = id
        self.description = description
        self.summaryParamList = summaryParamList
        self.position = defaultAttributeMap['position']