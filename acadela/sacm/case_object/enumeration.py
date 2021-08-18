from os.path import dirname
import sys

this_folder = dirname(__file__)


# A combination of attribute description and Enumeration Option
class Enumeration:
    def __init__(self, questionText, enumerationOptions):
        self.questionText = questionText
        self.options = enumerationOptions
