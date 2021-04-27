from acadela.sacm import util, default_state

import json
import sys
from acadela.sacm.case_object.attribute import Attribute
import acadela.sacm.interpreter.directive as directive

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def sacm_compile(derivedAttribute):
    attrObj = {"$": {}}
    thisAttr = attrObj["$"]

    thisAttr['id'] = derivedAttribute.id

    thisAttr['description'] = derivedAttribute.description

    util.compile_attributes(thisAttr, derivedAttribute,
        ['additionalDescription', 'expression',
         'explicitAttributeType', 'uiReference',
         'externalId'])

    print("Attribute JSON")
    print(json.dumps(attrObj, indent=4))
    return attrObj