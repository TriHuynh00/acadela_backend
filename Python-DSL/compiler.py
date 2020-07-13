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
"""

# Meta-model knows how to parse and instantiate models.
model = None

try:
    model = mm.model_from_str(model_str)

    point_interpreter = Interpreter(model)

    point_interpreter.interpret()

except TextXSyntaxError as e:
    SyntaxErrorHandler.handleSyntaxError(e)



# Output:
# Moving to position 5,10
# Drawing line from 5,10 to 10,10
# Drawing line from 10,10 to 20,20
# Moving by 5,-7 to a new position 25,13
# Drawing circle at 25,13 with radius 10
# Drawing line from 25,13 to 10,10

# Collect all points starting from the root of the model
points = get_children_of_type("Point", model)
for point in points:
    print('Point: {}'.format(point))
