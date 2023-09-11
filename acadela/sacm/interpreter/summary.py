from sacm import util, default_state
from sacm.default_state import defaultAttrMap

import json
import sys

from sacm.case_object.summary import SummarySection
import sacm.interpreter.directive as directiveInterpreter

from os.path import dirname

this_folder = dirname(__file__)


def interpret_summary(summary, model, isPrefixed = True):
    summaryId = summary.name

    if isPrefixed:
        summaryId = util.prefixing(summary.name)

    print("Summary Section directive", summary.directive)

    position = directiveInterpreter.interpret_directive(summary.directive) \
        if util.is_attribute_not_null(summary, 'directive') \
        else defaultAttrMap['position']

    print("Summary Section position", position)

    summaryParamList = []

    for summaryParam in summary.paramList:
        # TODO [Validation]: if each level in the summaryParam is accessible
        summaryParamPathLvl = str(summaryParam.path).split('.')
        sacmSummaryParamPath = ''
        for i in range(0, len(summaryParamPathLvl) - 1):
            sacmSummaryParamPath += \
                util.prefixing(summaryParamPathLvl[i]) \
                + '.'

        sacmSummaryParamPath += summaryParamPathLvl[-1]

        summaryParamList.append(sacmSummaryParamPath)
    lineNumber = model._tx_parser.pos_to_linecol(summary._tx_position)
    summarySection = SummarySection(summaryId,
                                    summary.description.value,
                                    summaryParamList,
                                    lineNumber,
                                    position=position)
    print ('Summary Section', vars(summarySection))

    return summarySection

def sacm_compile(summarySectionList):
    summaryJsonList = []
    print('summary section number: ', len(summarySectionList))

    for summarySect in summarySectionList:
        summaryJson = {
            '$': {},
            'SummaryParamDefinition': []
        }

        summaryAttr = summaryJson['$']

        summaryAttr['id'] = summarySect.id
        summaryAttr['description'] = summarySect.description
        summaryAttr['position'] = summarySect.position

        for summaryParam in summarySect.summaryParamList:

            summaryJson['SummaryParamDefinition'].append(
                {
                    '$': {
                        'path': summaryParam
                    }
                }
            )

        summaryJsonList.append(summaryJson)



    return summaryJsonList
        



