from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util

import json
import sys
import time
import numpy

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

staticDirectivesDict = {
    # Multiplicity
    '#maxOne': 'maximalOne',
    # Type
    '#text': 'string',
    '#selector': 'enumeration'
}

def is_static_directive(directive: str):
    # Static directives do not have parentheses
    # while dynamic ones have
    if directive.find("(") > -1:
        return False
    else:
        return True

def interpret_static_directive(directive: str):
    try:
        directiveValue = staticDirectivesDict[directive]
        return directiveValue
    except KeyError:
        return directive.replace('#', '')
