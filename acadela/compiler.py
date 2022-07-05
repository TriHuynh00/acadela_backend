import sys
import pprint
import logging
import re
import textx.scoping.providers as scoping_providers
# import obesity_treatment as caseTemplateStr
# import sample_case_def.hypertensionTreatmentPlan as caseTemplateStr
import sample_case_def.test_case_template as caseTemplateStr
import config.general_config as generalConf
import json
import os
from textx import *
from textx.export import *
from os.path import join, dirname, abspath

from sacm.interpreter.case_template import CaseInterpreter
from sacm.exception_handler.syntax_error_handler.syntax_error_handler import SyntaxErrorHandler

this_folder = dirname(__file__)

# Meta-model knows how to parse and instantiate models.
model = None

# True = run User/Group validation check in SACM
runNetworkOp = generalConf.CONN_SOCIOCORTEX

def analyze_dsl_language(metamodelPath, model, metamodel):
    # print("Treatment Plan Grammar")
    #
    # pprint.pprint(metamodel.namespaces['CompactTreatmentPlan'])
    #
    # print("Attribute Element")
    # pprint.pprint(vars(metamodel
    #                    .namespaces['CompactTreatmentPlan']
    #                    ['Attribute']))

    # mm = get_metamodel(model)
    # print (vars(mm['Case']._tx_attrs['hookList']))
    # print (mm.namespaces['CompactTreatmentPlan']['Case']._tx_attrs)

    # Analyze model structure
    pprint.pprint(model._tx_parser.parse_tree[0])


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
    #logging.basicConfig(filename='run.log', level=generalConf.LOG_LEVEL_NONE)

    input = caseTemplateStr.treatmentPlanStr

    if len(sys.argv) > 1:
        input = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2] == "validate":
            runNetworkOp = False
        else:
           runNetworkOp = True 

    metamodelPath = join(this_folder, 'CompactTreatmentPlan.tx')

    mm = metamodel_from_file(metamodelPath,
                             ignore_case=True)

    mm.register_scope_providers(
        {
            "*.*": scoping_providers \
                .FQNImportURI(importURI_converter=convert_import_path,
                              importAs=True)
        }
    )

    rootImportPath = join(abspath(dirname(__file__)), generalConf.MODEL_PLACEHOLDER)
    logging.info("rootImportPart" + rootImportPath)

    # metamodel_export(mm, 'entity.pu', renderer=PlantUmlRenderer())
    model = mm.model_from_str(input, rootImportPath)

    # extract_attributes(mm)
    # analyze_dsl_language(metamodelPath, model, mm)

    acaInterpreter = CaseInterpreter(mm, model,input)
    # ------------- HERE CHECK EXPRESSION
    acaInterpreter.interpret(runNetworkOp)
    
except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e, input, metamodelPath, mm)

except OSError as e:
    import_found = False
    split_path_imported=str(e).split("acadela/")
    if len(split_path_imported)>1:
        path_file = split_path_imported[1].split(".")[0].replace("/",".")
        print(path_file)
        # find the line with the import in case template
        file_name = split_path_imported[len(split_path_imported)-1]
        
        for index, item in enumerate(input.split("\n")):
            if path_file in item:
                line_str = item.strip()
                line_index = index + 1
                import_found = True
                print(item.strip(),index)
                raise Exception(f"Cannot import {path_file} at line {line_index}. File does not exist.\n\n {e}")
                
        if not import_found:
            raise Exception(f"Cannot import {path_file}. File does not exist.\n\n {e}")
    elif not import_found:
        print(e)
