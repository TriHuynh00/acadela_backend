class Field:
    def __init__(self, id, description,
                 uiRef,
                 externalId,
                 path,
                 position,
                 part,
                 isReadOnly,
                 isMandatory,
                 defaultValue,
                 defaultValues,
                 lineNumber):

        self.id = id
        self.description = description
        self.uiReference = uiRef
        self.externalId = externalId
        self.path = path
        self.isReadOnly = isReadOnly
        self.isMandatory = isMandatory
        self.position = position
        self.part = part
        self.lineNumber = lineNumber
        self.defaultValue = defaultValue
        self.defaultValues = defaultValues
