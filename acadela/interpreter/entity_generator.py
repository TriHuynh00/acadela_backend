from acadela.interpreter import json_util
from acadela.interpreter import util
import acadela.interpreter.attribute as attributeInterpreter

from acadela.caseobject.entity import Entity


import json
import requests
import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')


def generate_case_data_entity(settingEntity,
                              stageList = None,
                              caseEntity = None):
    interpret_setting_object(settingEntity)

def interpret_setting_object(settingObj):
    settingDescription = "Settings" \
        if settingObj.description == None \
        else settingObj.description.value

    settingEntity = Entity("Settings", settingDescription)

    settingJson = create_entity_json_object(settingEntity)

    print("Setting Entity: \n", json.dumps(settingJson, indent=4))

    print("\tCase Owner \n\t\tgroup = '{}' \n\t\tdesc = '{}'".format(
        settingObj.caseOwner.group,
        settingObj.caseOwner.attr.description.value
    ))

    for attr in settingObj.attrList:
        attributeInterpreter.interpret_attribute_object(attr)
        print("Attr ID " + attr.name)
        print("#Directives ", attr.attrProp.directive.type)

# Create an EntityDefinition based on a given id & description
def create_entity_json_object(entity):
    entityJson = {}
    entityJson["$"] = {
        "id": entity.id,
        "description": entity.description
    }
    return entityJson
