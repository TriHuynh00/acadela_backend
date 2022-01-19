# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from referencer.workspace import WorkspaceReferencer
from referencer.group import GroupReferencer
from referencer.user import UserReferencer

from sacm import util, json_util

from sacm.interpreter.group import GroupInterpreter
from sacm.interpreter.user import UserInterpreter
from sacm.interpreter.workspace import WorkspaceInterpreter
import sacm.interpreter.task as taskInterpreter
import sacm.interpreter.attribute as attributeInterpreter
import sacm.interpreter.case_definition as caseDefinition
from sacm.interpreter.stage import interpret_stage

from sacm.case_object.entity import Entity

from http_request import HttpRequest

import json
import requests
import sys
from sacm.exception_handler.semantic_error_handler import id_uniqueness_checker
from sacm.exception_handler.semantic_error_handler import path_validity_checker
from sacm.exception_handler.semantic_error_handler.url_validation import url_validator
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import field_expression_validator
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import ui_ref_validator
from sacm.exception_handler.semantic_error_handler.semantic_error_handler import SemanticErrorHandler

this_folder = dirname(__file__)


class CaseInterpreter():

    def __init__(self, metamodel, model, treatment_str):
        self.metamodel = metamodel
        self.model = model
        self.treatment_str = treatment_str
        self.refFinder = WorkspaceReferencer()
        self.groupFinder = GroupReferencer()
        self.groupInterpreter = GroupInterpreter()
        self.userInterpreter = UserInterpreter()
        self.workspaceInterpreter = WorkspaceInterpreter()
        self.userFinder = UserReferencer()

        self.workspace = ''
        self.groupList = []
        self.userList = []

        self.caseDefinition = None
        self.entityList = []
        self.stageList = []
        self.taskList = []
        self.attributeList = []
        self.jsonEntityList = []
        self.jsonAttributeList = []
        self.settingList = []

        self.caseObjectTree = None

    def compile_for_connecare(self, workspace, caseObjTree):
        caseObjList = {}

        caseDef = [caseDefinition. \
                       sacm_compile_case_def(caseObjTree['case'])]

        workspaceObjList = self.workspaceInterpreter \
            .workspacePropToJson(workspace, caseObjTree, self.entityList, caseDef)

        # Check if there is any Error being returned
        if workspaceObjList.get("Error") is None:
            caseObjList["Workspace"] = [workspaceObjList]
            # caseWorkspace = caseObjList["Workspace"]

        else:
            raise Exception("Invalid workspace {} with error: {}"
                            .format(workspace.staticId, workspaceObjList["Error"]))

        caseObjList['Group'] = json_util.basicIdentityListToJson(self.groupList)

        caseObjList['User'] = json_util.basicIdentityListToJson(self.userList)

        # caseDef = [caseDefinition. \
        #                sacm_compile_case_def(caseObjTree['case'])]
        #
        # caseObjList['CaseDefinition'] = caseDef

        caseDefJson = {"SACMDefinition": caseObjList}

        caseDefJsonFinal = {"jsonTemplate": caseDefJson}

        # print(json.dumps(caseDefJsonFinal, indent=4))
        print()
        return caseDefJsonFinal

    # Interpret the case object
    def interpret(self, runNetworkOp):
        model = self.model
        workspaceDef = model.defWorkspace
        print("WP type", util.cname(workspaceDef))
        print('importedObj', len(model.objList))
        # # Pure Object Import
        # if util.cname(workspace) != 'DefWorkSpace':
        #     for defObj in model.objList:
        #         if util.cname(defObj.object) == 'Entity':
        #             obj = defObj.object
        #             print(obj.name)
        #             for attr in obj.attr:
        #                print('{} = {}'.format(util.cname(attr), attr.value))
        # else:
        if util.cname(workspaceDef) == 'DefWorkspace':

            acaversion = model.versionTag
            print("ACA v =", acaversion)

            if runNetworkOp:
                workspaceStaticId = self.refFinder.findWorkspaceStaticIdByRefId(workspaceDef.workspace.name)

                if workspaceStaticId is None:
                    raise Exception('Workspace {} not found or not accessible'.format(workspaceStaticId))
                else:
                    workspaceDef.workspace.staticId = workspaceStaticId

                self.workspace = workspaceDef

            self.workspace = workspaceDef
            case = None
            caseCount = 0
            for wpObj in workspaceDef.workspaceObj:
                print('wpObj cname = ', util.cname(wpObj))

                if util.cname(wpObj) == 'Case':
                    case = util.getRefOfObject(wpObj)
                    caseCount += 1

            if caseCount > 1:
                raise Exception('Error: Multiple Case Definitions' \
                                'There are {} cases in the case definition.' \
                                'Only one case is allowed.'.format(caseCount))

            print('casePrefix = ' + case.casePrefix.value)
            util.set_case_prefix(case.casePrefix.value)

            # returnedMsg = self.workspaceInterpreter.findStaticId(workspace.name)

            # if "Error" in returnedMsg:
            #     raise Exception("StaticID not found for workspace {}, Reason: {}"
            #                     .format(workspace.name, returnedMsg))
            # else:
            #     workspace.staticId = returnedMsg

            if util.cname(case) == 'Case':
                print('Case', case.name)
                print(self.model._tx_parser.pos_to_linecol(case._tx_position))
            for group in case.responsibilities.groupList:
                print("Group", group.name)
                if runNetworkOp:
                    if self.groupInterpreter. \
                            find_static_id(group, workspaceDef.workspace.staticId) is not None:
                        self.groupList.append(group)
                    else:
                        raise Exception("cannot find static ID for group {} with name {} in workspace {}"
                                        .format(group.name, group.groupName, workspaceDef.workspace.staticId))
                else:
                    group.lineNumber = model._tx_parser.pos_to_linecol(group._tx_position)
                    self.groupList \
                        .append(group)

            for user in case.responsibilities.userList:
                print("User", user.name)
                if runNetworkOp:
                    if self.userInterpreter. \
                            findStaticId(user, self.groupList) is not None:
                        user.lineNumber = model._tx_parser.pos_to_linecol(user._tx_position)
                        self.userList.append(user)
                    else:
                        raise Exception(("cannot find static ID for user with reference ID {0}. " +
                                         "Please verify if the user reference ID is correct.")
                                        .format(user.name))
                else:
                    user.lineNumber = model._tx_parser.pos_to_linecol(user._tx_position)
                    self.userList.append(user)
            print()

            print('Workspace \n\tStaticID = {} \n\tID = {} \n'.format(
                workspaceDef.workspace.staticId, workspaceDef.workspace.name))

            for group in self.groupList:
                print("\tgroup: staticId = {}, name = {}".
                      format(group.staticId, group.name))

            print()

            for user in self.userList:
                print("\tuser: staticId = {}, id = {}".
                      format(user.staticId, user.name))

            print()
            ########################################
            # INTERPRET CLINICAL PATHWAYS ELEMENTS #
            ########################################
            stageAsAttributeList = []
            for caseStage in case.stageList:
                print("Stage", caseStage.name, "Task List size before parse", len(caseStage.taskList))
                if len(caseStage.preconditionList)>0:
                    for condition in caseStage.preconditionList:
                        print('Condition',condition.__dict__)

                stage = util.getRefOfObject(caseStage)

                taskAsAttributeList = []

                stageTasks = []

                for task in stage.taskList:
                    task = util.getRefOfObject(task)

                    iTask = taskInterpreter \
                        .interpret_task(self.model, task, stage.name)

                    taskAsAttributeList \
                        .append(iTask['taskAsAttribute'])

                    stageTasks.append(iTask['task'])

                    self.taskList.append(iTask['task'])

                    self.entityList \
                        .append(iTask['taskAsEntity'])

                interpretedStage = \
                    interpret_stage(self.model, stage,
                                    stageTasks,
                                    taskAsAttributeList)

                self.entityList \
                    .append(interpretedStage['stageAsEntity'])
            
                self.stageList \
                    .append(interpretedStage['stage'])

                stageAsAttributeList \
                    .append(interpretedStage['stageAsAttribute'])

            ############################################
            # END INTERPRET CLINICAL PATHWAYS ELEMENTS #
            ############################################

            interpretedSetting = caseDefinition \
                .interpret_setting_entity(case.setting, self.model)

            settingEntity = interpretedSetting['settingAsEntity']
            self.entityList.append(settingEntity)
            self.settingList.append(settingEntity)

            interpretedCase = caseDefinition.interpret_case_definition(
                case, interpretedSetting, stageAsAttributeList, self.stageList, self.model)

            self.entityList \
                .append(interpretedCase['caseDataEntity'])

            self.caseDefinition = interpretedCase['caseDefinition']
            
            # loop through stageasattributelist and add each to attributelist
            for attr in stageAsAttributeList:
                self.attributeList.append(attr)
                
            for attr in taskAsAttributeList:
                self.attributeList.append(attr)
            # Swap Entity so that the objects at higher
            # hierarchy are placed first. This avoid
            # creating non-existing parent entity when a
            # child entity is generated
            self.entityList.reverse()

            self.caseObjectTree = {
                "workspace": self.workspace,
                "groups": self.groupList,
                "users": self.userList,
                "entities": self.entityList,
                "stages": self.stageList,
                "tasks": self.taskList,
                'case': self.caseDefinition,
                "attributes": self.attributeList,
                "settings": self.settingList
            }
            #DO THE SEMANTIC ERROR CHECKS
            SemanticErrorHandler.handle_semantic_errors(self.caseObjectTree, self.treatment_str)
            #field_expression_validator.validate_field_expressions(self.caseObjectTree, self.treatment_str)
            #ui_ref_validator.validate_ui_ref(self.caseObjectTree,self.treatment_str)
            #url_validator.url_validator(self.caseObjectTree)

            # TODO [Validation]: Check valid path value here
            # 1. Check Sentry ID & Condition match with any existing
            #    Stage.Task.Field Object
            #
            #id_uniqueness_checker.check_id_uniqueness(self.caseObjectTree)
            # 2. Check Field with custom path is pointed to a valid source
            #    Need to prefix the path afterward (using
            #    prefix_path_value() function in interpreter/util_intprtr
            #path_validity_checker.check_path_validity(self.caseObjectTree, self.treatment_str)
            print("\nAttrList size =", len(case.setting.attrList))
            for attr in case.setting.attrList:
                attributeInterpreter.interpret_attribute_object(attr)
                print("Attr ID " + attr.name)
                print("#Directives ", attr.attrProp.directive.type)

            caseInJson = self.compile_for_connecare(
                workspaceDef.workspace, self.caseObjectTree)

            if runNetworkOp:
                response = requests.post(
                    HttpRequest.sacmUrl + \
                    "import/acadela/casedefinition?version={}&isExecute=false".format(self.caseDefinition.version),
                    headers=HttpRequest.simulateUserHeader,
                    json=json.loads(json.dumps(caseInJson)))

                if response.status_code == 500:
                    raise Exception("Internal Server Error in SACM")

                print("response", json.dumps(str(response._content)[1:-1], indent=2))

                # TODO [Validation]: Delete Created Case Version in
                # Sociocortex when an error is returned from SACM
