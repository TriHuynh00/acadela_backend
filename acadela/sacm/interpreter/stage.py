from sacm import util
from sacm.interpreter import util_intprtr

from sacm import default_state
from sacm.case_object.stage import Stage
from sacm.case_object.entity import Entity
from sacm.case_object.attribute import Attribute

from sacm.interpreter.directive import interpret_directive
from sacm.interpreter.sentry import interpret_precondition
import sacm.interpreter.task as taskIntprtr

from os.path import dirname
import sys

this_folder = dirname(__file__)


def interpret_stage(stage, taskList, taskAsAttributeList = None,):

    print("\n Stage Info")
    directive = stage.directive

    preconditionList = []

    type = default_state.ENTITY_LINK_TYPE + '.' \
           + util.prefixing(stage.name)

    manualActivationExpression = None

    extraDescription = util.set_default_value_if_null(
        stage.additionalDescription, None)
    # TODO add custom attach path
    # attachPath = util.prefixing(stage.name)

    stageAsEntity = Entity(stage.name, stage.description.value,
                         taskAsAttributeList)

    repeatable = interpret_directive(directive.repeatable)\
        if util.is_attribute_not_null(directive, 'repeatable')\
        else default_state.defaultAttrMap['repeatable']

    mandatory = interpret_directive(directive.mandatory)\
        if util.is_attribute_not_null(directive, 'mandatory')\
        else default_state.defaultAttrMap['mandatory']

    activationParse = util_intprtr.parse_activation(directive)

    activation = activationParse['activation']
    manualActivationExpression = \
        activationParse['manualActivationExpression']

    dynamicDescPath = stage.dynamicDescriptionPath.value \
        if util.is_attribute_not_null(stage.dynamicDescriptionPath, 'value') \
        else None

    externalId = stage.externalId.value \
        if util.is_attribute_not_null(stage.externalId, 'value') \
        else None

    preconditionObj = stage.preconditionList \
        if util.is_attribute_not_null(stage, 'preconditionList') \
        else None

    if preconditionObj is not None:
        print("Stage Precondition", [sentry for sentry in preconditionObj])
        for sentry in preconditionObj:
            preconditionList.append(interpret_precondition(sentry))

    ownerPathvalue = str(stage.ownerpath.value)\
        .replace(default_state.SETTING_NAME + ".", util.prefixing(default_state.SETTING_NAME + "."))

    stageObject = Stage(stage.name, stage.description.value,
                        directive.multiplicity,
                        type,
                        ownerPathvalue,
                        taskList,
                        extraDescription,
                        externalId,
                        repeatable,
                        mandatory,
                        activation,
                        manualActivationExpression,
                        dynamicDescPath,
                        preconditionList)

    stageAsAttribute = Attribute(stageObject.id,
                            stage.description,
                            directive.multiplicity,
                            type,
                            #uiReference = stage.uiReference.value,
                            additionalDescription = stage.additionalDescription,
                            externalId = externalId)

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
            '$': {}
        }

        stageAttr = stageJson['$']


        stageAttr['id'] = stage.id
        stageAttr['description'] = stage.description

        # if util.is_attribute_not_null(stage, 'repeatable'):
        #     stageAttr['repeatable'] = stage.repeatable
        #

        util.compile_attributes(stageAttr, stage,
                ['ownerPath', 'repeatable',
                 'mandatory', 'activation',
                 'manualActivationDescription',
                'entityDefinitionId', 'entityAttachPath',
                'externalId', 'dynamicDescriptionPath'])

        if len(stage.preconditionList) > 0:
            # TODO: Parse the subject of the expression
            # & prefix them based on their hierarchy level
             stageJson['SentryDefinition'] = \
                 util_intprtr.parse_precondition(stage, stageList)

        # parse the tasks
        print('len stageTaskList', len(stage.taskList))
        jsonTasks = taskIntprtr.sacm_compile(stage.taskList)

        # if len(jsonTasks['humanTaskList']) > 0:
        #     stageJson['HumanTaskDefinition'] = jsonTasks['humanTaskList']
        #
        # if len(jsonTasks['autoTaskList']) > 0:
        #     stageJson['AutomatedTaskDefinition'] = jsonTasks['autoTaskList']
        #
        # if len(jsonTasks['dualTaskList']) > 0:
        #     stageJson['DualTaskDefinition'] = jsonTasks['dualTaskList']

        if len(jsonTasks) > 0:
            stageJson['$$'] = jsonTasks

        stageJsonList.append(stageJson)

    return stageJsonList

