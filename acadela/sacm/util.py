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
def set_value_if_null(attribute, defaultValue):
    if attribute is None:
        return defaultValue
    else:
        return attribute