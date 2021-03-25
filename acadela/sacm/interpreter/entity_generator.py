import acadela.sacm.interpreter.attribute as attributeInterpreter

from acadela.sacm.case_object.entity import Entity

import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

caseOwnerAttr = None
casePatientAttr = None

# TODO: Generate JSON from Entity & Attribute Objects

# Generate the Case Data Entity, containing settings, CaseDefinition
def generate_case_data_entities_and_props(settingObj, stages):
    generatedEntities = []
    entitiesAndCaseProp = {}

    settingEntity = interpret_setting_entity(settingObj)

    caseDataEntity = Entity("CaseData",
                            "Case Data");



    caseDataEntity.attribute.append(settingEntity)

    # TODO: Add other Tasks and Stages as entities
    for stage in stages:
        print("Stage Info "
              "\n\tID: {}"
              "\n\tDescription: {}"
              .format(stage.id,
                      stage.description.value))

    generatedEntities.append(settingEntity)

    entitiesAndCaseProp['Entities'] = generatedEntities
    entitiesAndCaseProp['CaseOwner'] = caseOwnerAttr
    entitiesAndCaseProp['CasePatient'] = casePatientAttr

    return entitiesAndCaseProp

def interpret_setting_entity(settingObj):
    settingDescription = "Settings" \
        if settingObj.description == None \
        else settingObj.description.value

    settingEntity = Entity("Settings", settingDescription)

    for attr in settingObj.attrList:
        print("Attr ID " + attr.name)
        print("#Directives ", attr.attrProp.directive)
        attrObj = attributeInterpreter.interpret_attribute_object(attr)
        settingEntity.attribute.append(attrObj)

    print("\tCase Owner "
          "\n\t\tgroup = '{}' "
          "\n\t\tdesc = '{}' "
          "\n\t\tdirective = '{}'".format(
            settingObj.caseOwner.group,
            settingObj.caseOwner.attrProp.description.value,
            settingObj.caseOwner.attrProp.directive
    ))

    if settingObj.caseOwner is not None:
       global caseOwnerAttr
       caseOwnerAttr = attributeInterpreter.interpret_attribute_object(settingObj.caseOwner)
       settingEntity.attribute.append(caseOwnerAttr)

    if settingObj.casePatient is not None:
        global casePatientAttr
        casePatientAttr = attributeInterpreter.interpret_attribute_object(settingObj.casePatient)
        settingEntity.attribute.append(casePatientAttr)
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

