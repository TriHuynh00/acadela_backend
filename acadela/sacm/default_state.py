
defaultAttrMap = {
    'multiplicity': 'exactlyOne', # DONT SET TO 'any', it will break Precondition
    'type': 'notype',
    'mandatory': 'true',
    'readOnly': 'false',
    'repeatable': 'ONCE',
    'activation': 'AUTOMATIC',
    'position': 'STRETCHED'
}

CUSTOM_TYPE = 'custom'

DOCUMENT_LINK_TYPE = 'documentlink'
ENTITY_LINK_TYPE = 'Link.EntityDefinition'
USER_OR_GROUP_LINK_TYPE = 'Link.Users'

SETTING_NAME = 'Setting'
CASEOWNER_NAME = 'CaseOwner'
HUMAN_TASK_DEF = 'HumanTaskDefinition'
DUAL_TASK_DEF = 'DualTaskDefinition'
AUTO_TASK_DEF = 'AutomatedTaskDefinition'

ACTIVATE_WHEN = 'activateWhen'
EXPRESSION = 'EXPRESSION'