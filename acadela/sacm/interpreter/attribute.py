from sacm import util
from sacm.default_state import defaultAttrMap, USER_OR_GROUP_LINK_TYPE

import json
import sys
from sacm.case_object.attribute import Attribute
import sacm.interpreter.directive as directive

from os.path import dirname

this_folder = dirname(__file__)


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

    attrObj = Attribute(id=attrId, content=attribute.attrProp.description.value)

    # interpret directives
    if attribute.attrProp.directive is not None:

        if attribute.attrProp.directive.type is not None:
            print("Attr ID {}, type {}".format(attrId, attribute.attrProp.directive.type))
            attrObj.type = directive.interpret_directive(attribute.attrProp.directive.type)

        elif attrClassName == 'CaseOwner'\
                or attrClassName == 'CasePatient':
            attrObj.description = attribute.attrProp.description.value
            attrObj.type = USER_OR_GROUP_LINK_TYPE + '({})'.format(attribute.group)

        else:
            attrObj.type = defaultAttrMap['type']

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
            attribute.externalId.value

    if util.is_attribute_not_null(attribute, 'defaultValues'):
        attrObj.defaultValues = attribute.defaultValues.value

    return attrObj

def sacm_compile(attribute):
    attrObj = {"$": {}}
    thisAttr = attrObj["$"]
    thisAttr['id'] = attribute.id

    print("Attr Description class name", util.cname(attribute.description))

    thisAttr['description'] = attribute.description

    # if util.cname(attribute.description) == 'Description':
    #     thisAttr['description'] = attribute.description.value
    # elif util.cname(attribute.description) == 'Question':
    #     thisAttr['description'] = attribute.description.text
    #
    # else:
    #     thisAttr['description'] = attribute.description

    util.compile_attributes(thisAttr, attribute,
        ['defaultValues', 'additionalDescription', 'externalId'
         'mandatory', 'multiplicity', 'uiReference'])

    if util.is_attribute_not_null(attribute, 'type'):
        thisAttr['type'] = attribute.type

        if attribute.type == 'enumeration':

            optionList = []
            for option in attribute.enumerationOptions:

                optionJson = {}
                optionJson['value'] = option.value
                optionJson['description'] = option.description

                if option.additionalDescription is not None:
                    optionJson['additionalDescription']\
                        = option.additionalDescription

                if option.externalId is not None:
                    optionJson['externalId']\
                        = option.externalId

                optionList.append({"$": optionJson})
            attrObj['EnumerationOption'] = optionList
    else:
        thisAttr['type'] = defaultAttrMap['type']

    print("Attribute JSON")
    print(json.dumps(attrObj, indent=4))
    return attrObj
