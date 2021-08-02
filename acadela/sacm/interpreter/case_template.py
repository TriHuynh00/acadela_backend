# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from acadela.referencer.workspace import WorkspaceReferencer
from acadela.referencer.group import GroupReferencer
from acadela.referencer.user import UserReferencer

from acadela.sacm import util, json_util

from acadela.sacm.interpreter.group import GroupInterpreter
from acadela.sacm.interpreter.user import UserInterpreter
from acadela.sacm.interpreter.workspace import WorkspaceInterpreter
import acadela.sacm.interpreter.task as taskInterpreter
import acadela.sacm.interpreter.attribute as attributeInterpreter
import acadela.sacm.interpreter.case_definition as caseDefinition
from acadela.sacm.interpreter.stage import interpret_stage

from acadela.sacm.case_object.entity import Entity

from acadela.http_request import HttpRequest

import json
import requests
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

class CaseInterpreter():

    def __init__(self, metamodel, model):
        self.metamodel = metamodel
        self.model = model
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

        print(json.dumps(caseDefJsonFinal, indent=4))
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
        #else:
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

            for group in case.responsibilities.groupList:
                print("Group", group.name)

                if runNetworkOp:
                    if self.groupInterpreter.\
                            find_static_id(group, workspaceDef.workspace.staticId) is not None:
                        self.groupList.append(group)
                    else:
                        raise Exception("cannot find static ID for group {} with name {} in workspace {}"
                                        .format(group.name, group.groupName, workspaceDef.workspace.staticId))

            for user in case.responsibilities.userList:
                print("User", user.name)
                if runNetworkOp:
                    if self.userInterpreter.\
                            findStaticId(user, self.groupList) is not None:
                        self.userList.append(user)
                    else:
                        raise Exception(("cannot find static ID for user with reference ID {0}. " +
                                        "Please verify if the user reference ID is correct.")
                                        .format(user.name))

            print()


            print('Workspace \n\tStaticID = {} \n\tID = {} \n'.format(
                workspaceDef.workspace.staticId, workspaceDef.workspace.name))

            #for group in self.groupList:
            #    print("\tgroup: staticId = {}, name = {}".
            #          format(group.staticId, group.name))

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

                stage = util.getRefOfObject(caseStage)

                taskAsAttributeList = []

                stageTasks = []

                for task in stage.taskList:

                    task = util.getRefOfObject(task)

                    iTask = taskInterpreter\
                            .interpret_task(task, stage.name)

                    taskAsAttributeList\
                        .append(iTask['taskAsAttribute'])

                    stageTasks.append(iTask['task'])

                    self.taskList.append(iTask['task'])

                    self.entityList\
                        .append(iTask['taskAsEntity'])

                interpretedStage = \
                    interpret_stage(stage,
                                   stageTasks,
                                   taskAsAttributeList)

                self.entityList\
                    .append(interpretedStage['stageAsEntity'])

                self.stageList\
                    .append(interpretedStage['stage'])

                stageAsAttributeList\
                    .append(interpretedStage['stageAsAttribute'])

            ############################################
            # END INTERPRET CLINICAL PATHWAYS ELEMENTS #
            ############################################

            interpretedSetting = caseDefinition\
                .interpret_setting_entity(case.setting)

            settingEntity = interpretedSetting['settingAsEntity']
            self.entityList.append(settingEntity)

            interpretedCase = caseDefinition.interpret_case_definition(
                case, interpretedSetting, stageAsAttributeList, self.stageList)

            self.entityList \
                .append(interpretedCase['caseDataEntity'])

            self.caseDefinition = interpretedCase['caseDefinition']

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
                "attributes": self.attributeList
            }

            # TODO [Validation]: Check valid path value here
            # 1. Check Sentry ID & Condition match with any existing
            #    Stage.Task.Field Object
            #
            # 2. Check Field with custom path is pointed to a valid source
            #    Need to prefix the path afterward (using
            #    prefix_path_value() function in interpreter/util_intprtr

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

                print("response", json.dumps(str(response._content)[1:-1], indent=2))

                # TODO [Validation]: Delete Created Case Version in
                # Sociocortex when an error is returned from SACM
