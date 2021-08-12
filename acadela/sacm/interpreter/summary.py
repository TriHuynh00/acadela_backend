from acadela.sacm import util, default_state
from acadela.sacm.default_state import defaultAttrMap

import json
import sys

from acadela.sacm.case_object.summary import SummarySection
import acadela.sacm.interpreter.directive as directiveInterpreter

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def interpret_summary(summary, isPrefixed = True):
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

    summarySection = SummarySection(summaryId,
                                    summary.description.value,
                                    summaryParamList,
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
        



