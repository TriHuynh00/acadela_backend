from acadela.sacm import util
from acadela.sacm.case_object.enumeration_option import EnumerationOption
from acadela.sacm.default_state import defaultAttrMap
import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


class Attribute():
    def __init__(self, id, content,  # compulsory attributes
                 multiplicity = defaultAttrMap['multiplicity'],
                 type = defaultAttrMap['type'],  # directives
                 additionalDescription = None,  # below are optional
                 uiReference = None,
                 externalId = None,
                 defaultValues = None):
        self.id = id

        self.enumerationOptions = []
        self.description = None

        print('Attribute Content', util.cname(content))
        if util.cname(content) == 'str':
            self.description = content
        if util.cname(content) == "Description":
            self.description = content.value
        elif util.cname(content) == "Enumeration":
            self.description = content.questionText
            for option in content.options:
                additionalDescription = \
                    None if not hasattr(option, "additionalDescription") \
                         else option.additionalDescription

                externalId = \
                    None if not hasattr(option, "externalId") \
                        else option.additionalDescription

                self.enumerationOptions.append(
                    EnumerationOption(option.description,
                                      option.value,
                                      additionalDescription,
                                      externalId)
                )

        self.multiplicity = multiplicity
        self.type = type
        self.additionalDescription = additionalDescription
        self.uiReference = uiReference
        self.externalId = externalId
        self.defaultValues = defaultValues




