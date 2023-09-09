from sacm import util, default_state

from os.path import dirname
import sys

from sacm.case_object.workflow_item import WorkflowItem

this_folder = dirname(__file__)


class Task():
    def __init__(self, id, description,
                 multiplicity,
                 valueType,
                 taskType,
                 fieldList,
                 dynamicFieldList,
                 ownerPath,
                 dueDatePath,
                 repeatable,
                 mandatory,
                 activation,
                 manualActivationExpression,
                 externalId,
                 additionalDescription,
                 dynamicDescriptionPath,
                 preconditionList,
                 hookList,
                 lineNumber,
                 entityAttachPath = None,
                 entityDefinitionId = None,
                 isPrefixed = True,
                 ):

        if isPrefixed:
            id = util.prefixing(id)

        if entityDefinitionId is None:
            entityDefinitionId = id

        self.attrType = valueType
        self.fieldList = fieldList
        self.dynamicFieldList = dynamicFieldList
        self.dueDatePath = dueDatePath

        WorkflowItem.__init__(self, id,
                          description,
                          multiplicity,
                          taskType,
                          ownerPath,
                          additionalDescription,
                          externalId,
                          repeatable,
                          mandatory,
                          activation,
                          manualActivationExpression,
                          dynamicDescriptionPath,
                          preconditionList,
                          hookList,
                          lineNumber,
                          entityDefinitionId,
                          entityAttachPath)

    # def print(self):
    #     print("\n\tTask {}"
    #           "\n\t\tDirectives "
    #           "\n\t\t\tmandatory = {}"
    #           "\n\t\t\trepeatable = {}"
    #           "\n\t\t\tactivation = {}"
    #           "\n\t\t\tmultiplicity = {}"
    #           "\n\t\tdescription = {}"
    #           "\n\t\townerPath = {}"
    #           "\n\t\tdueDatePath = {}"
    #           "\n\t\texternalId = {}"
    #           "\n\t\tdynamicDescriptionPath = {}"
    #           .format(self.id,
    #                   mandatory,
    #                   repeatable,
    #                   activation,
    #                   multiplicity,
    #                   attrList.description.value,
    #                   (None if attrList.ownerPath is None else attrList.ownerPath.value),
    #                   dueDatePath,
    #                   ("None" if attrList.externalId is None else attrList.externalId.value),
    #                   ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))


