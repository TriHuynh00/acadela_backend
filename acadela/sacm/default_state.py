import sys

defaultAttrMap = {
    'multiplicity': 'any',
    'type': 'notype',
    'mandatory': 'false',
    'readOnly': 'false',
    'repeatable': 'ONCE',
    'activation': 'automatic',
    'position': 'STRETCHED'
}

entityLinkType = 'Link.EntityDefinition'
userOrGroupLinkType = 'Link.Users'

settingName = 'Setting'
HumanTaskDef = 'HumanTaskDefinition'
DualTaskDef = 'DualTaskDefinition'
AutoTaskDef = 'AutomatedTaskDefinition'