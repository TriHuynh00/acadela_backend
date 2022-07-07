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
