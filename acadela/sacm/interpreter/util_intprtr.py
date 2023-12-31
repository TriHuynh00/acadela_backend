import sys

from sacm import default_state, util
from sacm.interpreter import sentry, stage
from sacm.interpreter.directive import interpret_directive

def parse_activation(directive):
    manualActivationExpression = None

    activation = interpret_directive(directive.activation) \
        if util.is_attribute_not_null(directive, 'activation') \
        else default_state.defaultAttrMap['activation']

    if activation is not None and \
            activation\
                .startswith(default_state.ACTIVATE_WHEN):

        manualActivationExpression = \
            prefix_path_value(directive \
                .activation[
                    len(default_state.ACTIVATE_WHEN) + 2 :-1
                ],
                False
            )
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
        if not str(pathSections[i]).startswith(util.prefix):
            prependedPath += str('.' + util.prefixing(pathSections[i]))

    if isAllValuePrefixed is False:
        prependedPath += str('.' + pathSections[-1])

    print("Prepended Path After =", prependedPath)

    return prependedPath




