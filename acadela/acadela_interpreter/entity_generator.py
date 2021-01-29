from acadela.acadela_interpreter import json_util
from acadela.acadela_interpreter import util
import acadela.acadela_interpreter.attribute as attributeInterpreter

from acadela.caseobject.entity import Entity


import json
import requests
import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

# TODO: Generate JSON from Entity & Attribute Objects
# Generate all the entities needed to construct the case
def generate_all_case_entities(settingObj,
                                stageList = None):
    allEntitiesList = []
    allEntitiesList.extend(generate_case_data_entities(settingObj))

    return allEntitiesList;

# Generate the Case Data Entity, containing settings, CaseDefinition
def generate_case_data_entities(settingObj):
    generatedEntities = []

    settingEntity = interpret_setting_entity(settingObj)

    generatedEntities.append(settingEntity)

    return generatedEntities

def interpret_setting_entity(settingObj):
    settingDescription = "Settings" \
        if settingObj.description == None \
        else settingObj.description.value

    settingEntity = Entity("Settings", settingDescription)

    print("\tCase Owner \n\t\tgroup = '{}' \n\t\tdesc = '{}'".format(
        settingObj.caseOwner.group,
        settingObj.caseOwner.attr.description.value
    ))

    for attr in settingObj.attrList:
        print("Attr ID " + attr.name)
        print("#Directives ", attr.attrProp.directive.type)
        attrObj = attributeInterpreter.interpret_attribute_object(attr)
        settingEntity.attribute.append(attrObj)

        # settingAttributeJson = []
        # attrObjJson = attributeInterpreter.create_attribute_json_object(attrObj)
        # settingAttributeJson.append(attrObjJson)

    # settingJson = create_entity_json_object(settingEntity)
    # settingJson["Attribute"] = settingAttributeJson
    # print("Setting Entity: \n", json.dumps(settingJson, indent=4))
    return settingEntity

# Create an EntityDefinition based on a given id & description
def create_entity_json_object(entity):
    entityJson = {}
    entityJson["$"] = {
        "id": entity.id,
        "description": entity.description
    }

    attributeList = []
    if hasattr(entity, "attribute"):
        for attribute in entity.attribute:
            attributeList.append(
                attributeInterpreter.
                    create_attribute_json_object(attribute))

    entityJson["AttributeDefinition"] = attributeList

    return entityJson
