
class WorkflowItem:
    def __init__(self, id, 
         description,
         multiplicity,
         type,
         ownerPath,
         additionalDescription,
         externalId,
         repeatable,
         mandatory,
         activation,
         manualActivationExpression,
         dynamicDescriptionPath,
         preconditionList,
         hookList,
         lineNumber,
         entityDefinitionId,
         entityAttachPath,
         ):

        self.id = id
        self.description = description
        self.multiplicity = multiplicity
        self.type = type
        self.ownerPath = ownerPath
        self.additionalDescription = additionalDescription
        self.externalId = externalId
        self.repeatable = repeatable
        self.mandatory = mandatory
        self.activation = activation
        self.manualActivationExpression = manualActivationExpression
        self.dynamicDescriptionPath = dynamicDescriptionPath
        self.preconditionList = preconditionList
        self.hookList = hookList
        self.lineNumber = lineNumber
        self.entityDefinitionId = entityDefinitionId
        self.entityAttachPath = entityAttachPath

    
        
