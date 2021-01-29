from acadela.interpreter import util

import json
import requests
import sys
from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class Entity():
    def __init__(self, id, description, attribute = []):

        self.id = util.prefixing(id)
        self.description = description
        self.attribute = attribute

