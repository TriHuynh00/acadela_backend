
import acadela.sacm.util as util
import acadela.sacm.default_state as defaultState

import acadela.sacm.interpreter.attribute as attributeInterpreter
import acadela.sacm.interpreter.summary as summaryInterpreter

from acadela.sacm.case_object.entity import Entity
from acadela.sacm.case_object.attribute import Attribute
from acadela.sacm.case_object.case_definition import CaseDefinition

import sys

from os.path import dirname

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

caseOwnerAttr = None
casePatientAttr = None

# Generate the Case Data Entity, containing settings, CaseDefinition
def interpret_case_definition(id, description,
                              summary, hookList,
                              intprtSetting, stageAsAttributeList,
                              notes = None):
    global caseOwnerAttr
    global casePatientAttr

    settingEntity = intprtSetting['settingAsEntity']

    caseOwnerPath = '{}.{}'.format(settingEntity.id,\
                                   caseOwnerAttr.id)

    caseClientPath = None\
        if casePatientAttr is None\
        else '{}.{}'.format(settingEntity.id,\
                            casePatientAttr.id)

    caseDataEntity = interpret_case_data(intprtSetting['settingAsAttribute'],
                                         stageAsAttributeList)

    caseHookEvents = interpret_case_hook(hookList)

    print("Case Hook Events", caseHookEvents)

    # TODO: CREATE SUMMARYSECTION INTERPRETER
    summarySectionList = []
    for summarySection in summary.sectionList:
        summarySectionList.append(
            summaryInterpreter.interpret_summary(summarySection))

    caseDefinition = CaseDefinition(id, description,
                        caseOwnerPath,
                        caseDataEntity.id,
                        summarySectionList,
                        caseHookEvents,
                        entityDefinitionId = settingEntity,
                        entityAttachPath = settingEntity,
                        clientPath = caseClientPath)

    return {
        'caseDefinition': caseDefinition,
        'caseDataEntity': caseDataEntity
    }

def interpret_case_data(settingAsAttribute, stageAsAttributes):

    caseDataEntity = Entity("CaseData",\
                            "Case Data")

    caseDataEntity.attribute = stageAsAttributes

    caseDataEntity.attribute.append(settingAsAttribute)

    return caseDataEntity

def interpret_setting_entity(settingObj):
    settingDescription = "Settings" \
        if settingObj.description is None \
        else settingObj.description.value

    settingName = util.prefixing("Settings")

    settingEntity = Entity(settingName,
                           settingDescription)

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

    settingType = defaultState.entityLinkType + "." \
                  + settingName

    settingAsAttribute = Attribute(settingName,
                                   settingObj.description,
                                   type=settingType)

    print("Setting Attribute", vars(settingAsAttribute))

    # settingJson = create_entity_json_object(settingEntity)
    # settingJson["Attribute"] = settingAttributeJson
    # print("Setting Entity: \n", json.dumps(settingJson, indent=4))
    return {
        'settingAsEntity': settingEntity,
        'settingAsAttribute': settingAsAttribute
    }

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
            print ("Attribute type of ", attribute.id, "is", util.cname(attribute) )
            if util.cname(attribute) == 'Attribute':
                attributeList.append(
                    attributeInterpreter.
                        create_attribute_json_object(attribute))
            elif util.cname(attribute) == 'DerivedAttribute':
                # TODO: Compile Derived Attribute
                pass

    entityJson["AttributeDefinition"] = attributeList

    return entityJson

def interpret_case_hook(hookList):
    hookEvents = {}
    for hook in hookList:
        hookEvents[hook.event] = hook.url

    return hookEvents
