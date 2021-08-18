from os.path import dirname
import sys

this_folder = dirname(__file__)


# Sentry (Precondition)
class Precondition:
    def __init__(self, stepList,
                 expression = None):
        self.stepList = stepList
        self.expression = expression
