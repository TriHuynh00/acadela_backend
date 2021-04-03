from acadela.sacm import util, default_state

import json
import sys

from acadela.sacm.case_object.summary import SummarySection
import acadela.sacm.interpreter.directive as directiveInterpreter

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

def interpret_summary(summary, isPrefixed = True):
    summaryId = summary.id

    if isPrefixed:
        summaryId = util.prefixing(summary.id)

    position = None\
        if not hasattr(summary.directive, 'position')\
        else directiveInterpreter.interpret_directive(summary.directive.position)

    summaryParamList = []

    for summaryParam in summary.paramList:
        summaryParamList.append(summaryParam.path)

    summarySection = SummarySection(summaryId,
                                    summary.description,
                                    summaryParamList,
                                    position=position)
    print ('Summary Section', vars(summarySection))

    return summarySection
