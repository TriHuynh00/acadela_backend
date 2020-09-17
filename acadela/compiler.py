from textx import metamodel_from_str, metamodel_from_file, get_children_of_type, TextXSyntaxError
import sys, os
from os.path import join, dirname

from interpreter import Interpreter
from syntaxerrorhandler import SyntaxErrorHandler

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.
this_folder = dirname(__file__)

mm = metamodel_from_file(join(this_folder, 'TreatmentPlan.tx'), classes=None, ignore_case=True)

model_str = """
    workspace staticId = 'c023' id = 'Lleida_Cancer' 
    define case COPD_Plan
        group staticId = 'g01' id = 'doctorGroup'
        group staticId = 'g02' id = 'nurseGroup'
        user staticId = 'u01' id = 'Jane'
        user staticId = 'u02' id = 'Kim'
        
        attributelist
            entity Settings
                description = 'Settings desc'
                multiplicity = 'exactlyOne'
                type = "Link.Type.Settings"
            entity Identifications
                description = 'Identitfication desc'
                multiplicity = 'many'
        CaseDefinition Leida
"""

# workspace staticId = 'c023' id = 'Lleida_Cancer'
#     define case COPD_Plan
#         multiplicity = 3
#         prefix = 'COPD1'
#         uiReference = colors(5<=green<7<red<13)

# Meta-model knows how to parse and instantiate models.
model = None

try:
    model = mm.model_from_str(model_str)

    point_interpreter = Interpreter(model)

    point_interpreter.interpret()

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)

# Collect all points starting from the root of the model
points = get_children_of_type("Point", model)
for point in points:
    print('Point: {}'.format(point))
