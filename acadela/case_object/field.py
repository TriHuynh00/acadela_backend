from acadela.acadela_interpreter import util
from acadela.default_state import config

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TaskParamDefinition
class Field:
    def __init__(self, path,
                 isReadOnly = None,
                 isMandatory = None,
                 position = None,
                 part = None):

        self.path = path
        self.readOnly = isReadOnly
        self.mandatory = isMandatory
        self.position = position
        self.part = part
