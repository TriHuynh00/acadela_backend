# TaskParamDefinition
# class InputField:
#     def __init__(self, id, description,
#                  question,
#                  multiplicity,
#                  type,
#                  path,
#                  isReadOnly,
#                  isMandatory,
#                  position,
#                  uiRef,
#                  externalId,
#                  part,
#                  lineNumber):
#
#         self.id = id
#         self.description = description
#         self.question = question
#         self.path = path
#         self.isReadOnly = isReadOnly
#         self.isMandatory = isMandatory
#         self.position = position
#         self.part = part
#         self.multiplicity = multiplicity
#         self.uiReference = uiRef
#         self.externalId = externalId
#         self.type = type
#         self.lineNumber = lineNumber
from sacm.case_object.field import Field

class InputField(Field):
    def __init__(self, id, description,
                 question,
                 multiplicity,
                 type,
                 path,
                 isReadOnly,
                 isMandatory,
                 position,
                 uiRef,
                 externalId,
                 part,
                 defaultValue,
                 defaultValues,
                 lineNumber):

        self.question = question
        self.multiplicity = multiplicity
        self.type = type
        Field.__init__(self, id, description,
                       uiRef,
                       externalId,
                       path,
                       position,
                       part,
                       isReadOnly,
                       isMandatory,
                       defaultValue,
                       defaultValues,
                       lineNumber)
