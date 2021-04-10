from acadela.sacm import util

import sys
from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class CaseDefinition():
    def __init__(self, id, description,
                 ownerPath,
                 rootEntityId, # Case Data ID
                 summarySectionList,
                 caseHookEvents,
                 entityDefinitionId,
                 entityAttachPath,
                 stageList,
                 clientPath = None,
                 notesDefaultValue = None,
                 version = 0,
                 isPrefixed = True):

        if isPrefixed:
            self.id = util.prefixing(id)
        else:
            self.id = id

        self.description = description

        self.rootEntityId = rootEntityId

        self.ownerPath = ownerPath
        self.clientPath = clientPath

        self.summarySectionList = summarySectionList

        self.entityDefinitionId = entityDefinitionId
        self.entityAttachPath = entityAttachPath

        self.stageList = stageList

        self.notesDefaultValue = notesDefaultValue
        self.caseHookEvents = caseHookEvents
        self.version = version
        # self.onActivateHookUrl = onActivateHookUrl
        # self.onCompleteHookUrl = onCompleteHookUrl
        # self.onTerminateHookUrl = onTerminateHookUrl
        # self.onDeleteHookUrl = onDeleteHookUrl
