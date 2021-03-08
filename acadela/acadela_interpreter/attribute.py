from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util
from acadela.default_state import config

import json
import requests
import sys
from acadela.case_object.attribute import Attribute
import acadela.acadela_interpreter.directive as directive

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TODO: check if attribute ID already exists in case template's attribute list
# Params:
#   attribute: represents the parsed/artificial attribute object
#   isIdPrefixed: True - the attribute ID is prepended with case prefix.
#                 False - the attribute ID is kept in its original form
def interpret_attribute_object(attribute, isIdPrefixed = False):
    attrClassName = util.cname(attribute)
    if attrClassName == 'CaseOwner':
        attrId = 'CaseOwner'
    elif attrClassName == 'CasePatient':
        attrId = 'CasePatient'
    else:
        attrId = attribute.name

    if isIdPrefixed:
        attrId = util.prefixing(attrId)

    attrObj = Attribute(id=attrId, description=attribute.attrProp.description.value)

    # interpret directives
    if attribute.attrProp.directive is not None:

        if attribute.attrProp.directive.type is not None:
            attrObj.type = directive.interpret_directive(attribute.attrProp.directive.type)

        elif attrClassName == 'CaseOwner'\
                or attrClassName == 'CasePatient':
            attrObj.type = 'links.users({})'.format(attribute.group)

        else:
            attrObj.type = config.defaultAttributeMap['type']

        if attribute.attrProp.directive.multiplicity is not None:
            attrObj.multiplicity = directive.interpret_directive(attribute.attrProp.directive.multiplicity)

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
    if hasattr(attribute, 'defaultValues'):
        thisAttr['defaultValues'] = attribute.defaultValues

    if hasattr(attribute, 'additionalDescription'):
        thisAttr['additionalDescription'] = \
            attribute.additionalDescription

    if hasattr(attribute, 'externalId'):
        thisAttr['externalId'] = \
            attribute.externalId

    if hasattr(attribute, 'type'):
        thisAttr['type'] = attribute.type
    if hasattr(attribute, 'multiplicity'):
        thisAttr['multiplicity'] = attribute.multiplicity

    print("Attribute JSON")
    print(json.dumps(attrObj, indent=4))
    return attrObj
