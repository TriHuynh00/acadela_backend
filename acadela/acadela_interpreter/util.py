prefix = ""

def cname(o):
    return o.__class__.__name__

def set_case_prefix(casePrefix):
    global prefix
    prefix = casePrefix + "_"

def prefixing(name):
    return str(prefix + name)

# If an attribute of an object is empty
# Assign None or a predefined value into it
def assign_default_attribute_value(object, attribute, defaultValue = None):
    if hasattr(object, attribute):
        if defaultValue is None:
            return None
        else:
            return defaultValue