from acadela.sacm import util, default_state
from acadela.sacm.case_object.stage import Stage
from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.attribute import Attribute

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def interpret_stage(stage, taskAsAttributeList, taskList):

    print("\n Stage Info")
    directive = stage.directive

    type = None if not hasattr(directive, 'type')\
                else directive.type

    manualActivationExpression = None

    if directive.activation is not None and \
            directive.activation.startswith("activateWhen"):
        manualActivationExpression = \
            directive.activation.split('(')[1][:-1]

    attachPath = util.prefixing(stage.id)

    stageAsEntity = Entity(stage.id, stage.description.value,
                         taskAsAttributeList)

    stageObject = Stage(stage.id, stage.description.value,
                        stage.ownerpath.value,
                        directive.repeatable,
                        directive.mandatory,
                        directive.activation,
                        directive.multiplicity,
                        manualActivationExpression,
                        stage.externalId.value,
                        stage.dynamicDescriptionPath.value,
                        taskList = taskList)

    stageAsAttribute = Attribute(stageObject.id,
                            stage.description,
                            directive.multiplicity,
                            type,
                            #uiReference = stage.uiReference.value,
                            additionalDescription = stage.additionalDescription,
                            externalId = stage.externalId.value)

    print('stageEntity', vars(stageAsEntity))
    print('stageAsAttribute', vars(stageAsAttribute))
    print('stage', vars(stageObject))
    # print("\tDirectives: "
    #       "\n\t\t mandatory = {}"
    #       "\n\t\t repeatable = {}"
    #       "\n\t\t activation = {}"
    #       "\n\t\t multiplicity = {}".
    #       format(directive.mandatory,
    #              directive.repeatable,
    #              directive.activation,
    #              directive.multiplicity))
    # print("\tDescription: " + stage.description.value)
    # print("\tOwnerPath: " + stage.ownerpath.value)
    # print("\tDynamic Description Path: " + stage.dynamicDescriptionPath.value)
    # print("\tExternal ID: " + stage.externalId.value)

    return {
        'stageAsEntity': stageAsEntity,
        'stage': stageObject,
        'stageAsAttribute': stageAsAttribute
    }
