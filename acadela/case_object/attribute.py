from acadela.acadela_interpreter import util

import json
import requests
import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


class Attribute():
    def __init__(self, id, description, # compulsory attributes
                 multiplicity='any', type='notype', # directives
                 additionalDescription = None, # below are optional
                 uiReference = None,
                 externalId = None,
                 defaultValues = None):
        self.id = id
        self.description = description
        self.multiplicity = multiplicity
        self.type = type
        self.additionalDescription = additionalDescription
        self.uiReference = uiReference
        self.externalId = externalId
        self.defaultValues = defaultValues


