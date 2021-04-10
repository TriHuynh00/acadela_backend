from acadela.sacm import util
from acadela.sacm.default_state import defaultAttrMap
from acadela.sacm.case_object.stage import Stage
from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.attribute import Attribute

from acadela.sacm.interpreter.directive import interpret_directive

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def interpret_stage(stage, taskList, taskAsAttributeList = None,):

    print("\n Stage Info")
    directive = stage.directive

    type = None if not hasattr(directive, 'type')\
                else directive.type

    manualActivationExpression = None

    if directive.activation is not None and \
            directive.activation.startswith("activateWhen"):
        manualActivationExpression = \
            directive.activation.split('(')[1][:-1]

    extraDescription = util.set_default_value_if_null(
        stage.additionalDescription, None)
    # TODO add custom attach path
    # attachPath = util.prefixing(stage.id)

    stageAsEntity = Entity(stage.id, stage.description.value,
                         taskAsAttributeList)

    repeatable = interpret_directive(directive.repeatable)\
        if util.is_attribute_not_null(directive, 'repeatable')\
        else defaultAttrMap['repeatable']

    #util.set_default_value_if_null(directive.repeatable,
     #                   defaultAttrMap['repeat'])

    # mandatory = util.set_default_value_if_null(\
    #     directive.mandatory,
    #     defaultAttrMap['mandatory'])

    mandatory =  interpret_directive(directive.mandatory)\
        if util.is_attribute_not_null(directive, 'mandatory')\
        else defaultAttrMap['mandatory']

    activation = util.set_default_value_if_null(directive.activation,
                        defaultAttrMap['activation'])

    stageObject = Stage(stage.id, stage.description.value,
                        directive.multiplicity,
                        type,
                        stage.ownerpath.value,
                        taskList,
                        extraDescription,
                        stage.externalId.value,
                        repeatable,
                        mandatory,
                        activation,
                        manualActivationExpression,
                        stage.dynamicDescriptionPath.value)

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

def sacm_compile(stageList):
    stageJsonList = []

    for stage in stageList:
        stageJson = {
            '$': {},
            'HttpHookDefinition': []
        }

        stageAttr = stageJson['$']

        stageAttr['id'] = stage.id
        stageAttr['description'] = stage.description
        stageAttr['mandatory'] = stage.mandatory

        # TODO Parse HookDef and other stage elements

        stageJsonList.append(stageJson)

    return stageJsonList