from acadela.sacm import util
import acadela.sacm.default_state as default_state

import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# Acadela-SACM Dictionary: Fast Lookup than if-else statement
staticDirectivesDict = {
    # Multiplicity
    '#maxOne': 'maximalOne',
    # Type
    '#text': 'string',
    '#selector': 'enumeration',
    # Mandatory
    '#mandatory': 'true',
    '#notmandatory': 'false',
    # Read-Only
    '#readOnly': 'true',
    '#notReadOnly': 'false',
    # DualTask Part
    '#humanDuty': 'HUMAN',
    '#systemDuty': 'AUTOMATED',
    # Repeatable
    '#noRepeat': 'ONCE',
    '#repeatSerial': 'SERIAL',
    '#repeatParallel': 'PARALLEL',
    # Activation (#activateWhen (aka. Expression)
    # is a dynamic directive)
    '#manualActivate': 'MANUAL',
    '#autoActivate': 'AUTOMATIC'
}

def interpret_directive(directiveObj):
    if directiveObj is None:
        return None

    # Static directives do not have parentheses
    # while dynamic ones have
    if util.cname(directiveObj) == "str":
        if directiveObj.find("(") > -1:
            return interpret_dynamic_directive(directiveObj, util.cname(directiveObj))
        else:
            return interpret_static_directive(directiveObj)
    elif util.cname(directiveObj) == "NumType":
        return interpret_dynamic_directive(directiveObj, util.cname(directiveObj))

# translate directive in Acadela to SACM value
def interpret_static_directive(directive):
    try:
        directiveValue = staticDirectivesDict[directive]
        return directiveValue
    except KeyError:
        return directive.replace('#', '')


# Parse parameterized directives
def interpret_dynamic_directive(directiveObj, directiveType):
    # Type directives
    if directiveType == "str":
        if directiveObj.startswith('link.'):
            typeAndValue = directiveObj.split('.')[1]
            if typeAndValue.startswith('Entity'):
                typeAndValue.replace('Entity', 'EntityDefinition', 1)

            return "Link." + typeAndValue

    elif directiveType == "NumType":

        numberType = "number"

        if directiveObj.comparator != None:
            # Parse min/max form
            comparator = directiveObj.comparator
            num = directiveObj.num

            if comparator == ">":
                return numberType + ".min({})".format(num + 1)
            elif comparator == ">=":
                return numberType + ".min({})".format(num)
            elif comparator == "<":
                return numberType + ".max({})".format(num - 1)
            elif comparator == "<=":
                return numberType + ".max({})".format(num)
            else:
                return numberType

        # Parse min AND max form
        elif directiveObj.min is not None and \
            directiveObj.max is not None:
            if int(str(directiveObj.min)) < int(str(directiveObj.max)):
                minMaxStr = ".min({}).max({})".format(
                    directiveObj.min, directiveObj.max)
                return numberType + minMaxStr
            else:
                raise Exception("The minimum number should be smaller than maximum number")
                return None

    else:
        return directiveObj.replace('#', '')

def interpret_num_type(directiveObj):
    numberType = "number"

    if directiveObj.comparator != None:
        # Parse min/max form
        comparator = directiveObj.comparator
        num = directiveObj.num

        if comparator == ">":
            return numberType + ".min({})".format(num + 1)
        elif comparator == ">=":
            return numberType + ".min({})".format(num)
        elif comparator == "<":
            return numberType + ".max({})".format(num - 1)
        elif comparator == "<=":
            return numberType + ".max({})".format(num)
        else:
            return numberType

    # Parse min AND max form
    elif directiveObj.min is not None and \
            directiveObj.max is not None:
        if int(str(directiveObj.min)) < int(str(directiveObj.max)):
            minMaxStr = ".min({}).max({})".format(
                directiveObj.min, directiveObj.max)
            return numberType + minMaxStr
        else:
            raise Exception("The minimum number should be smaller than maximum number")
            return None