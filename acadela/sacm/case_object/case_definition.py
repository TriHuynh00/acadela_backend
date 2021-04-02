from acadela.sacm import util

import sys
from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class CaseDefinition():
    def __init__(self, id, description,
                 ownerPath,
                 rootEntityDefinitionId, # Case Data ID
                 summarySectionList,
                 caseHookEvents,
                 entityDefinitionId = None,
                 entityAttachPath = None,
                 clientPath = None,
                 notesDefaultValue = None,
                 isPrefixed = True):

        if isPrefixed:
            self.id = util.prefixing(id)
        else:
            self.id = id

        self.description = description

        self.rootEntityId = rootEntityDefinitionId

        self.ownerPath = ownerPath
        self.clientPath = clientPath

        self.summarySectionList = summarySectionList

        self.entityDefitionId = entityDefinitionId
        self.entityAttachPath = entityAttachPath

        self.notesDefaultValue = notesDefaultValue
        self.caseHookEvents = caseHookEvents
        # self.onActivateHookUrl = onActivateHookUrl
        # self.onCompleteHookUrl = onCompleteHookUrl
        # self.onTerminateHookUrl = onTerminateHookUrl
        # self.onDeleteHookUrl = onDeleteHookUrl
