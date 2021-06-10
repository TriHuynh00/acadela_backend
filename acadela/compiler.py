import sys
import textx.scoping.providers as scoping_providers
import acadela.test_case_template as caseTemplateStr

from textx import metamodel_from_file, TextXSyntaxError
from os.path import join, dirname, abspath

sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\sacm')
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\acadela\\exception_handler')

from acadela.sacm.interpreter.case_template import CaseInterpreter
from acadela.sacm.exception_handler.syntax_error_handler import SyntaxErrorHandler

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.

def convert_import_path(i):
    return i.replace(".", "/") + ".aca"


this_folder = dirname(__file__)

# Meta-model knows how to parse and instantiate models.
model = None

try:
    input = caseTemplateStr.inputStrSimple
    # if len(sys.argv) > 1:
    #     input = sys.argv[1];


    def importURI_to_scope_name(import_obj):
        # this method is responsible to deduce the module name in the
        # language from the importURI string
        # e.g. here: import "file.ext" --> module name "file".
        return import_obj.importURI.split('.')[0]


    def custom_scope_redirection(obj):
        from textx import textx_isinstance
        if textx_isinstance(obj, mm["Stage"]):
            if obj.ref is None:
                from textx.scoping import Postponed
                return Postponed()
            return [obj.ref]
        else:
            return []


    mm = metamodel_from_file(join(this_folder, 'CompactTreatmentPlan.tx'),
                             ignore_case=True)

    mm.register_scope_providers(
        {
            "*.*": scoping_providers\
                .FQNImportURI(importURI_converter=convert_import_path,
                          importAs=True)
        }
    )

    rootImportPath = join(abspath(dirname(__file__)), 'aa')
    print("rootImportPart", rootImportPath)
    model = mm.model_from_str(input, rootImportPath)
    # model = mm.model_from_str(input)
    acaInterpreter = CaseInterpreter(mm, model)

    runNetworkOp = True
    acaInterpreter.interpret(runNetworkOp)

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)


