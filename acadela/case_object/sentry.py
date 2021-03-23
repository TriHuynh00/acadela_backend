from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# Sentry (Precondition)
class Precondition:
    def __init__(self, stepList,
                 expression = None):
        self.stepList = stepList
        self.expression = expression
