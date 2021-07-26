from acadela.sacm import util
from acadela.sacm.interpreter import util_intprtr

from acadela.sacm import default_state
from acadela.sacm.case_object.stage import Stage
from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.attribute import Attribute

from acadela.sacm.interpreter.directive import interpret_directive
from acadela.sacm.interpreter.sentry import interpret_precondition
import acadela.sacm.interpreter.task as taskIntprtr

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

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

    # activation = default_state.defaultAttrMap['activation']
    # if directive.activation is not None and \
    #         directive.activation.startswith('#' + default_state.ACTIVATE_WHEN):
    #
    #     manualActivationExpression = \
    #         directive.activation[len(default_state.ACTIVATE_WHEN) + 2:-1]
    #
    #
    #     activation = default_state.EXPRESSION
    #
    #     print ("activation mode", activation, "value", manualActivationExpression)
    # else:
    #     activation = interpret_directive(directive.activation)\
    #         if util.is_attribute_not_null(directive, 'activation')\
    #         else default_state.defaultAttrMap['activation']

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
             stageJson['SentryDefinition'] = \
                 util_intprtr.parse_precondition(stage)

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

