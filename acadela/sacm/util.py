from acadela.sacm.default_state import settingName

prefix = ""

def cname(o):
    return o.__class__.__name__

def set_case_prefix(casePrefix):
    global prefix
    prefix = casePrefix + "_"

def prefixing(name):
    return str(prefix + name)

def prefixingSetting(name):
    return str(name).replace(settingName + '.', \
                             prefixing(settingName) + '.')

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
    elif getattr(object, attrName) is '' or \
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