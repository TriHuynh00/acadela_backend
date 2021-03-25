from acadela.sacm import util
from acadela.sacm.case_object.enumeration_option import EnumerationOption

import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


class Attribute():
    def __init__(self, id, content, # compulsory attributes
                 multiplicity='any', type='notype', # directives
                 additionalDescription = None, # below are optional
                 uiReference = None,
                 externalId = None,
                 defaultValues = None):
        self.id = id

        self.enumerationOptions = []

        if util.cname(content) == "Description":
            self.description = content.value
        elif util.cname(content) == "Question":
            self.description = content.text

            for option in content.optionList:
                additionalDescription = \
                    None if not hasattr(option, "additionalDescription") \
                         else option.additionalDescription

                externalId = \
                    None if not hasattr(option, "externalId") \
                        else option.additionalDescription

                self.enumerationOptions.append(
                    EnumerationOption(option.key, option.value,
                                      additionalDescription,
                                      externalId)
                )



        self.description = content
        self.multiplicity = multiplicity
        self.type = type
        self.additionalDescription = additionalDescription
        self.uiReference = uiReference
        self.externalId = externalId
        self.defaultValues = defaultValues




