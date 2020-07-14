from textx import metamodel_from_str, metamodel_from_file, get_children_of_type, TextXSyntaxError
import sys, os
from os.path import join, dirname
from pointmodel.point import Point
from interpreter import Interpreter
from exceptionhandler.syntaxerrorhandler import SyntaxErrorHandler

# Create meta-model from the grammar. Provide `pointmodel` class to be used for
# the rule `pointmodel` from the grammar.
this_folder = dirname(__file__)

mm = metamodel_from_file(join(this_folder, 'TreatmentPlan.tx'), classes=None)

model_str = """
    define case 'COPD_Plan'
        prefix = 'COPD1'
        multiplicity = 3
        uiReference = colors(5<=green<7)
"""

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
