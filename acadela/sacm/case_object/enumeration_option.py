from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


# A combination of attribute description and Enumeration Option
class EnumerationOption:
    def __init__(self, description, value,
                    additionalDescription=None,
                    externalId=None):
        self.description = description
        self.value = value
        self.additionalDescription = additionalDescription
        self.externalId = externalId
