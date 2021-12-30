
import sacm.util as util
import sacm.default_state as defaultState

import sacm.interpreter.attribute as attributeInterpreter
import sacm.interpreter.derived_attribute as derAttrInterpreter
import sacm.interpreter.summary as summaryInterpreter
import sacm.interpreter.stage as stageInterpreter

from sacm.case_object.entity import Entity
from sacm.case_object.attribute import Attribute
from sacm.case_object.case_definition import CaseDefinition

import sys

from os.path import dirname

from sacm.case_object.http_hook import HttpTrigger

this_folder = dirname(__file__)


caseOwnerAttr = None
casePatientAttr = None
settingName = defaultState.SETTING_NAME

hookEventMap = {
    'available': 'onAvailableHTTPHookURL',
    'enable': 'onEnableHttpHTTPHookURL',
    'activate': 'onActivateHTTPHookURL',
    'complete': 'onCompleteHTTPHookURL',
    'terminate': 'onTerminateHTTPHookURL',
    'delete': 'onDeleteHTTPHookURL'
}

# onAvailableHTTPHookURL: cd.$.onAvailableHTTPHookURL,
# onEnableHttpHTTPHookURL: cd.$.onEnableHttpHTTPHookURL,
# onActivateHTTPHookURL: cd.$.onActivateHTTPHookURL,
# onCompleteHTTPHookURL: cd.$.onCompleteHTTPHookURL,
# onTerminateHTTPHookURL: cd.$.onTerminateHTTPHookURL,
# onDeleteHTTPHookURL: cd.$.onDeleteHTTPHookURL,

# Generate the Case Data Entity, containing settings, CaseDefinition
def interpret_case_definition(case, intprtSetting,
                              stageAsAttributeList,
                              stageList, model):
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

    caseHookEvents = interpret_case_hook(case.hookList, model)

    print("Case Hook Events", caseHookEvents)

    summarySectionList = []
    for summarySection in case.summary.sectionList:
        summarySectionList.append(
            summaryInterpreter.interpret_summary(summarySection,model))

    caseDefinition = CaseDefinition(case.name, case.description.value,
                        caseOwnerPath,
                        caseDataEntity.id,
                        summarySectionList,
                        caseHookEvents,
                        settingEntity.id,
                        settingEntity.id,
                        stageList,
                        clientPath = caseClientPath,
                        version = case.version,
                        notesDefaultValue = case.notes,
                        isPrefixed=False)

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

def interpret_setting_entity(settingObj, model):
    global settingName

    print("Setting name is ", settingName,settingObj.__dict__)
    settingDescription = settingName \
        if settingObj.description is None \
        else settingObj.description.value

    settingEntity = Entity(settingName,
                           settingDescription)

    for attr in settingObj.attrList:
        print("Attr ID " + attr.name)
        print("#Directives ", attr.attrProp.directive)
        attrObj = attributeInterpreter.interpret_attribute_object(attr)
        attrObj.lineNumber = model._tx_parser.pos_to_linecol(attr._tx_position)
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
       caseOwnerAttr.lineNumber = model._tx_parser.pos_to_linecol(settingObj.caseOwner._tx_position)
       settingEntity.attribute.append(caseOwnerAttr)

    if settingObj.casePatient is not None:
        global casePatientAttr
        casePatientAttr = attributeInterpreter.interpret_attribute_object(settingObj.casePatient)
        casePatientAttr.lineNumber = model._tx_parser.pos_to_linecol(settingObj.casePatient._tx_position)
        settingEntity.attribute.append(casePatientAttr)
        # settingAttributeJson = []
        # attrObjJson = attributeInterpreter.create_attribute_json_object(attrObj)
        # settingAttributeJson.append(attrObjJson)

    settingName = util.prefixing(settingName)

    settingType = defaultState.ENTITY_LINK_TYPE + "." \
                  + settingName

    settingAsAttribute = Attribute(settingName,
                                   settingDescription,
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
    derivedAttrList = []

    if hasattr(entity, "attribute"):
        for attribute in entity.attribute:
            if attribute is not None:
                print("Attribute type of ", attribute.id,
                      "is", util.cname(attribute))

                if util.cname(attribute) == 'Attribute':
                    attributeList.append(
                        attributeInterpreter.sacm_compile(attribute)
                    )

                elif util.cname(attribute) == 'DerivedAttribute':
                    derivedAttrList.append(
                        derAttrInterpreter.sacm_compile(attribute)
                    )

    entityJson["AttributeDefinition"] = attributeList

    if len(derivedAttrList) > 0:
        entityJson["DerivedAttributeDefinition"] = derivedAttrList

    return entityJson

def interpret_case_hook(hookList, model):
    hookEvents = []
    for hook in hookList:
        print("hoook:",hook.__dict__)
        line_number = model._tx_parser.pos_to_linecol(hook._tx_position)
        print("LINENMUBER",line_number)
        hookEvents.append(HttpTrigger(hook.event, hook.url,
                                      None,line_number))

    return hookEvents


def sacm_compile_case_def(case):
    global hookEventMap

    caseDefJson = {
        '$': {},
        'SummarySectionDefinition': [],
        'StageDefinition': []
    }

    caseDefAttr = caseDefJson['$']

    # Mandatory Case Definition Attribute
    caseDefAttr['id'] = case.id
    caseDefAttr['description'] = case.description
    caseDefAttr['ownerPath'] = case.ownerPath
    caseDefAttr['entityDefinitionId'] = case.rootEntityId
    caseDefAttr['newEntityDefinitionId'] = case.entityDefinitionId
    caseDefAttr['newEntityAttachPath'] = case.entityAttachPath

    # Optional Case Definition Attribute
    if util.is_attribute_not_null(case, 'clientPath'):
        caseDefAttr['clientPath'] = case.clientPath

    if util.is_attribute_not_null(case, 'notesDefaultValue'):
        caseDefAttr['notesDefaultValue'] = case.notesDefaultValue

    # Parsing Hooks
    if util.is_attribute_not_null(case, 'caseHookEvents'):
        for hook in case.caseHookEvents:
            hookEventSacm = hookEventMap[hook.on]
            if hookEventSacm is not None:
                caseDefAttr[hookEventSacm] = str(hook.url)

    if util.is_attribute_not_null(case, 'version'):
        caseDefAttr['version'] = case.version

    # Parsing SummarySection
    caseDefJson['SummarySectionDefinition'] = \
        summaryInterpreter.sacm_compile(case.summarySectionList)

    # Parsing Stage
    caseDefJson['StageDefinition'] = \
        stageInterpreter.sacm_compile(case.stageList)

    return caseDefJson


# "id": "GCS1_Groningen",
# "description": "Groningen CS1",
# "ownerPath": "GCS1_Settings.CaseOwner",
# "clientPath": "GCS1_Settings.Patient",
# "entityDefinitionId": "GCS1_CaseData",
# "newEntityDefinitionId": "GCS1_Settings",
# "newEntityAttachPath": "GCS1_Settings",
# "onCompleteHTTPHookURL": "http://integration-producer:8081/v1/producer/point-to-point/sacm/case/terminate",
# "onTerminateHTTPHookURL": "http://integration-producer:8081/v1/producer/point-to-point/sacm/case/terminate",
# "onDeleteHTTPHookURL": "http://integration-producer:8081/v1/producer/point-to-point/sacm/case/terminate"