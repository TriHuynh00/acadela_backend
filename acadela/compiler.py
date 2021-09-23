import sys
import pprint
import logging

import textx.scoping.providers as scoping_providers
#import obesity_treatment as caseTemplateStr
# import sample_case_def.hypertensionTreatmentPlan as caseTemplateStr
import sample_case_def.smoke_inhalation as caseTemplateStr
import config.general_config as generalConf

from textx import *
from os.path import join, dirname, abspath

from sacm.interpreter.case_template import CaseInterpreter
from sacm.exception_handler.syntax_error_handler import SyntaxErrorHandler

this_folder = dirname(__file__)

# Meta-model knows how to parse and instantiate models.
model = None

# True = run User/Group validation check in SACM
runNetworkOp = not generalConf.CONN_SOCIOCORTEX

def analyze_dsl_language(metamodelPath, model, metamodel):

    print("Treatment Plan Grammar")

    pprint.pprint(metamodel.namespaces['CompactTreatmentPlan'])

    print("Attribute Element")
    pprint.pprint(vars(metamodel
                       .namespaces['CompactTreatmentPlan']
                                  ['Attribute']))
    # mm = get_metamodel(model)
    # print (vars(mm['Case']._tx_attrs['hookList']))
    # print (mm.namespaces['CompactTreatmentPlan']['Case']._tx_attrs)

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.

def convert_import_path(i):
    return i.replace(".", "/") + ".aca"

    def importURI_to_scope_name(import_obj):
        # this method is responsible to deduce the module name in the
        # language from the importURI string
        # e.g. here: import "file.ext" --> module name "file".
        return import_obj.importURI.split('.')[0]


try:
    logging.basicConfig(filename='run.log', level=generalConf.LOG_LEVEL_NONE)

    input = caseTemplateStr.treatmentPlanStr

    if len(sys.argv) > 1:
        input = sys.argv[1]

    metamodelPath = join(this_folder, 'CompactTreatmentPlan.tx')

    mm = metamodel_from_file(metamodelPath,
                             ignore_case=True)

    mm.register_scope_providers(
        {
            "*.*": scoping_providers\
                .FQNImportURI(importURI_converter=convert_import_path,
                          importAs=True)
        }
    )

    rootImportPath = join(abspath(dirname(__file__)), 'aa')
    logging.info("rootImportPart" + rootImportPath)
    model = mm.model_from_str(input, rootImportPath)

    # analyze_dsl_language(metamodelPath, model, mm)

    acaInterpreter = CaseInterpreter(mm, model)

    acaInterpreter.interpret(runNetworkOp)

    print("")
except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)
    # print(vars(e.expected_rules[0]))


