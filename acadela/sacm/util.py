from sacm.default_state import SETTING_NAME

prefix = ""

def cname(o):
    return o.__class__.__name__

def set_case_prefix(casePrefix):
    global prefix
    prefix = casePrefix + "_"

def prefixing(name):
    return str(prefix + name)

def unprefix(name):
    global prefix
    return str(name).replace(prefix, "", 1)

def prefixingSetting(name):
    return str(name).replace(SETTING_NAME + '.', \
                             prefixing(SETTING_NAME) + '.')

# If an attribute of an object is empty
# Assign None or a predefined value into it
def set_default_value_if_null(attribute, defaultValue):
    if attribute is None:
        return defaultValue
    else:
        if hasattr(attribute, 'value'):
            return attribute.value

        return attribute

def is_attribute_not_null(object, attrName):
    if not hasattr(object, attrName):
        return False
    elif getattr(object, attrName) == '' or \
            getattr(object, attrName) == 'None' or \
            getattr(object, attrName) is None:
        return False
    else:
        return True

def compile_attributes(keyObject, object, attributeList):
    for attribute in attributeList:
        if is_attribute_not_null(object, attribute):
            keyObject[attribute] = getattr(object, attribute)

def getRefOfObject(object):
    if is_attribute_not_null(object, 'ref'):
        return object.ref
    else:
        return object