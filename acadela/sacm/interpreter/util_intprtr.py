import acadela.sacm.util as util
import sys

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