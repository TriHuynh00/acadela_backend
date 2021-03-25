from acadela.sacm import util

import sys
from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class Entity():
    def __init__(self, id, description, attribute = [], isPrefixed = True):
        if isPrefixed:
            self.id = util.prefixing(id)
        else:
            self.id = id

        self.description = description

        self.attribute = attribute

