from acadela.referencer.workspace import WorkspaceReferencer
from acadela.sacm import util
from acadela.sacm.interpreter import case_definition

import acadela.sacm.interpreter.attribute as attrIntrprtr

import json

class WorkspaceInterpreter:
    def __init__(self):
        self.workspaceFinder = WorkspaceReferencer()
        self.jsonEntityList = []

    def findStaticId(self, workspaceId):
        workspaceStaticId = self.workspaceFinder.findWorkspaceStaticIdByRefId(workspaceId)

        # TODO: Make a customized message for each of the workspace error
        if workspaceStaticId == "invalidGetWorkspaceRequest" \
        or workspaceStaticId == "workspaceIdNotFound":
            return "Error " + workspaceStaticId
        else:
            return workspaceStaticId

    def interpret_entity_sacm(self, targetEntity, parentEntity):

        # TODO: Crafting entityType based on casePrefix
        # if entity.attrProp.type is not None:
        #     entityType = entity.type.value

        print('entity', targetEntity.name)

        print('\tdescription: {}\n'.format(targetEntity.description.value))

        entityProp = {}

        entityProp["$"] = {
            "id": targetEntity.name,
            "description": targetEntity.description.value
        }

        # self.jsonEntityList["$"]["AttributeDefinition"]

        attrDefList = []

        if len(targetEntity.attrList) > 0:
            for attrElem in targetEntity.attrList:

                for entityAttr in attrElem.attr:
                    # If this entityAttr has an entity, append it to the entity list
                    if util.cname(entityAttr) == "Entity":
                        self.interpret_entity_sacm(entityAttr, parentEntity)

                    attrObj = {"$": {}}
                    entityAttrProp = entityAttr.attrProp

                    thisAttr = attrObj["$"]
                    thisAttr['id'] = entityAttr.id
                    thisAttr['description'] = entityAttr.description.value
                    if entityAttrProp.defaultValues is not None:
                        thisAttr['defaultValues'] = entityAttrProp.defaultValues.value

                    if entityAttrProp.additionalDescription is not None:
                        thisAttr['additionalDescription'] = \
                            entityAttrProp.additionalDescription.value

                    if entityAttrProp.type is not None:
                        thisAttr['type'] = entityAttrProp.type.value

                    if entityAttrProp.multiplicity is not None:
                        print(entityAttrProp.multiplicity)
                        thisAttr['multiplicity'] = entityAttrProp.multiplicity

                    print("\tEntity Attributes: ", json.dumps(thisAttr, indent=4))

                    attrDefList.append(attrObj)

            entityProp["AttributeDefinition"] = attrDefList
        self.jsonEntityList.append(entityProp)


    def workspacePropToJson(self, workspace, caseObjTree, entityList):
        workspaceObjList = {}
        workspaceObjList["$"] = \
            {
                "staticId": workspace.staticId,
                "id": workspace.id
            }
        entityJsonList = []
        for entity in entityList:
            print('Parse Entity', entity.id)
            entityJsonList.append(
                case_definition.create_entity_json_object(entity))


        # for task in caseObjTree["tasks"]:
        #     for field in task.fieldList:
        #         attrIntrprtr.create_attribute_json_object(field)

        workspaceObjList["EntityDefinition"] = entityJsonList


        # print("#entities = ", len(case.entityList))
        # for entity in case.entityList:
        #     self.interpretEntity(entity, entity)

        # workspaceObjList["EntityDefinition"] = \
        #     self.jsonEntityList

        return workspaceObjList