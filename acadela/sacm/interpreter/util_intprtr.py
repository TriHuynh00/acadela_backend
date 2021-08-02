import sys


from acadela.sacm import default_state, util
from acadela.sacm.interpreter.directive import interpret_directive


sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# Parse the sentry of a stage or task
def parse_precondition(process):
    if len(process.preconditionList) > 0:
        sentryList = []

        for precondition in process.preconditionList:

            sentryJson = {}

            if util.is_attribute_not_null(precondition, 'expression'):
                sentryJson['$'] = {
                    'expression': precondition.expression
                }

            sentryJson['precondition'] = []

            for processId in precondition.stepList:
                preconditionJson = \
                    {
                        'processDefinitionId': processId,
                    }

                sentryJson['precondition'].append(
                    {
                        '$': preconditionJson
                    }
                )

            sentryList.append(sentryJson)

        return sentryList
    
def parse_activation(directive):
    manualActivationExpression = None

    activation = default_state.defaultAttrMap['activation'] \
        if not hasattr(directive, 'activation') \
        else interpret_directive(directive.activation)

    if activation is not None and \
            activation\
                .startswith(default_state.ACTIVATE_WHEN):

        manualActivationExpression = \
            directive \
                .activation[
                    len(default_state.ACTIVATE_WHEN) + 2
                    :-1
                ]
        activation = default_state.EXPRESSION

        print("activation mode", activation, "value", manualActivationExpression)

    return {
        'activation': activation,
        'manualActivationExpression': manualActivationExpression
    }

def prefix_path_value(pathValue, isAllValuePrefixed = True):
    pathSections = pathValue.split('.')

    print("Path Sections =", pathSections)

    prependedPath = util.prefixing(pathSections[0])

    prefixScope = len(pathSections) \
                    if isAllValuePrefixed \
                    else len(pathSections) - 1

    print("Prepended Path =", prependedPath)

    for i in range(1, prefixScope):

        prependedPath += str('.' + util.prefixing(pathSections[i]))

    if isAllValuePrefixed is False:
        prependedPath += str('.' + pathSections[-1])

    return prependedPath




