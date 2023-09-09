from sacm import util, default_state

from os.path import dirname

from sacm.case_object.workflow_item import WorkflowItem

this_folder = dirname(__file__)


class Stage(WorkflowItem):
    def __init__(self, id, description,
                 multiplicity,
                 type,
                 ownerPath,
                 taskList,
                 additionalDescription,
                 externalId,
                 repeatable,
                 mandatory,
                 activation,
                 manualActivationExpression,
                 dynamicDescriptionPath,
                 preconditionList,
                 stageHookList,
                 lineNumber,
                 entityDefinitionId = None,
                 entityAttachPath=None,
                 isPrefixed = True
                 ):

        if isPrefixed:
            id = util.prefixing(id)

        if entityDefinitionId is None:
            entityDefinitionId = id

        if entityAttachPath is None:
            entityAttachPath = id

        self.taskList = taskList

        WorkflowItem.__init__(self, id,
                              description,
                              multiplicity,
                              type,
                              ownerPath,
                              additionalDescription,
                              externalId,
                              repeatable,
                              mandatory,
                              activation,
                              manualActivationExpression,
                              dynamicDescriptionPath,
                              preconditionList,
                              stageHookList,
                              lineNumber,
                              entityDefinitionId,
                              entityAttachPath)



