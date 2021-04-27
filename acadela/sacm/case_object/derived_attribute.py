from os.path import dirname
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class DerivedAttribute:
    def __init__(self, id, description,
                 additionalDescription = None,
                 expression = None,
                 uiRef = None,
                 externalId = None,
                 explicitType = None):

        self.id = id
        self.description = description
        self.additionalDescription = additionalDescription
        self.expression = expression
        self.uiReference = uiRef
        self.externalId = externalId
        self.explicitAttributeType = explicitType


