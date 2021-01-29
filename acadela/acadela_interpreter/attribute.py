from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util

import json
import requests
import sys
from acadela.caseobject.attribute import Attribute

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TODO: check if attribute ID already exists in case template's attribute list
# Params:
#   attribute: represents the parsed/artificial attribute object
#   isIdPrefixed: True - the attribute ID is prepended with case prefix.
#                 False - the attribute ID is kept in its original form
def interpret_attribute_object(attribute, isIdPrefixed = False):

    attrId = attribute.name
    if isIdPrefixed:
        attrId = util.prefixing(attrId)

    attrObj = Attribute(id=attrId, description=attribute.description.value)

    # interpret directives
    if attribute.attrProp.directive is not None:
        if attribute.attrProp.directive.type is not None:
            attrObj.type = attribute.attrProp.directive.type

        if attribute.attrProp.directive.multiplicity is not None:
            attrObj.multiplicity = attribute.attrProp.directive.multiplicity

    # interpret optional elements
    if hasattr(attribute, 'additionalDescription'):
        attrObj.additionalDescription = \
            attribute.additionalDescription.value

    if hasattr(attribute, 'uiReference'):
        attrObj.uiReference = \
            attribute.uiReference.value

    if hasattr(attribute, 'externalId'):
        attrObj.externalId = \
            attribute.additionalDescription.value

    if hasattr(attribute, 'defaultValues'):
        attrObj.defaultValues = attribute.defaultValues.value

    return attrObj

def create_attribute_json_object(attribute):
    attrObj = {"$": {}}
    thisAttr = attrObj["$"]
    thisAttr['id'] = attribute.id
    thisAttr['description'] = attribute.description
    if attribute.defaultValues is not None:
        thisAttr['defaultValues'] = attribute.defaultValues

    if attribute.additionalDescription is not None:
        thisAttr['additionalDescription'] = \
            attribute.additionalDescription

    if attribute.externalId is not None:
        thisAttr['externalId'] = \
            attribute.externalId

    if attribute.type is not None:
        thisAttr['type'] = attribute.type
    if attribute.multiplicity is not None:
        thisAttr['multiplicity'] = attribute.multiplicity

    print("Attribute JSON")
    print(json.dumps(attrObj, indent=4))
    return attrObj
