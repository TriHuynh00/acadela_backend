from acadela.sacm import util
from acadela.sacm.interpreter import util_intprtr

from acadela.sacm.default_state import defaultAttrMap
from acadela.sacm.case_object.stage import Stage
from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.attribute import Attribute

from acadela.sacm.interpreter.directive import interpret_directive
from acadela.sacm.interpreter.sentry import interpret_precondition
from acadela.sacm.interpreter.task import sacm_compile as compile_task

from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def interpret_stage(stage, taskList, taskAsAttributeList = None,):

    print("\n Stage Info")
    directive = stage.directive

    preconditionList = []

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

    mandatory = interpret_directive(directive.mandatory)\
        if util.is_attribute_not_null(directive, 'mandatory')\
        else defaultAttrMap['mandatory']

    activation = interpret_directive(directive.activation)\
        if util.is_attribute_not_null(directive, 'activation')\
        else defaultAttrMap['activation']

    preconditionObj = stage.preconditionList \
        if util.is_attribute_not_null(stage, 'preconditionList') \
        else None

    if preconditionObj is not None:
        print("Stage Precondition", [sentry for sentry in preconditionObj])
        for sentry in preconditionObj:
            preconditionList.append(interpret_precondition(sentry))

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
                        stage.dynamicDescriptionPath.value,
                        preconditionList)

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
            # []
            #
            # for precondition in stage.preconditionList:
            #
            #     sentryJson = {}
            #
            #     if util.is_attribute_not_null(precondition, 'expression'):
            #         sentryJson['$'] = {
            #             'expression': precondition.expression
            #         }
            #
            #     sentryJson['precondition'] = []
            #
            #     for processId in precondition.stepList:
            #
            #         preconditionJson = \
            #         {
            #             'processDefinitionId': processId,
            #         }
            #
            #         sentryJson['precondition'].append(
            #             {
            #                 '$': preconditionJson
            #             }
            #         )
            #
            #     stageJson['SentryDefinition'].append(sentryJson)

        # parse the tasks
        jsonTasks = compile_task(stage.taskList)

        if len(jsonTasks['humanTaskList']) > 0:
            stageJson['HumanTaskDefinition'] = jsonTasks['humanTaskList']

        if len(jsonTasks['autoTaskList']) > 0:
            stageJson['AutomatedTaskDefinition'] = jsonTasks['autoTaskList']

        if len(jsonTasks['dualTaskList']) > 0:
            stageJson['DualTaskDefinition'] = jsonTasks['dualTaskList']

        stageJsonList.append(stageJson)

    return stageJsonList

