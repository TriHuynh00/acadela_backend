# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from acadela.referencer.workspace import WorkspaceReferencer
from acadela.referencer.group import GroupReferencer
from acadela.referencer.user import UserReferencer

from acadela.sacm.interpreter.group import GroupInterpreter
from acadela.sacm.interpreter.user import UserInterpreter
from acadela.sacm.interpreter.workspace import WorkspaceInterpreter
import acadela.sacm.interpreter.task as taskInterpreter
import acadela.sacm.interpreter.attribute as attributeInterpreter
import acadela.sacm.interpreter.entity_generator as entityGenerator
from acadela.sacm.interpreter.stage import interpret_stage
from acadela.sacm import util, json_util

from acadela.http_request import HttpRequest

import json
import requests
import sys

this_folder = dirname(__file__)
sys.path.append('E:\\TUM\\Thesis\\ACaDeLaEditor\\acadela_backend\\')

runNetworkOp = False

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
        self.groupList = []
        self.caseDefinition = None
        self.userList = []
        self.entityList = []
        self.stageList = []
        self.taskList = []
        self.attributeList = []
        self.jsonEntityList = []
        self.jsonAttributeList = []
        self.caseObjectTree = [
            {"workspace": ""},
            {"groups": self.groupList},
            {"users":  self.userList},
            {"entities": self.entityList},
            {"stages": self.stageList},
            {"tasks": self.taskList},
            {"case": self.caseDefinition},
            {"attributes": self.attributeList}
        ]

    def compile_for_connecare(self, workspace, case):
        caseObjList = {}
        workspaceObjList = self.workspaceInterpreter \
            .workspacePropToJson(workspace, case, self.entityList)

        # Check if there is any Error being returned
        if workspaceObjList.get("Error") is None:
            caseObjList["Workspace"] = [workspaceObjList]
        else:
            raise Exception("Invalid workspace {} with error: {}"
                            .format(workspace.staticId, workspaceObjList["Error"]))

        caseObjList['Group'] = json_util.basicIdentityListToJson(self.groupList)

        caseObjList['User'] = json_util.basicIdentityListToJson(self.userList)

        caseDefJson = {"SACMDefinition": caseObjList}

        caseDefJsonFinal = {"jsonTemplate": caseDefJson}

        print(json.dumps(caseDefJsonFinal, indent=4))
        print()
        return caseDefJsonFinal

    # Interpret the case object
    def interpret(self):
        model = self.model
        workspace = model.defWorkspace

        # Pure Object Import
        if workspace == None:
            for defObj in model.defObj:
                if util.cname(defObj.object) == 'Entity':
                    obj = defObj.object
                    print(obj.name)
                    for attr in obj.attr:
                       print('{} = {}'.format(util.cname(attr), attr.value))
        else:
            acaversion = model.versionTag

            print("ACA v =", acaversion)

            workspace = model.defWorkspace.workspace

            if runNetworkOp:
                workspace.staticId = self.refFinder.findWorkspaceStaticIdByRefId(workspace.id)

            case = model.defWorkspace.workspaceProp.case

            # returnedMsg = self.workspaceInterpreter.findStaticId(workspace.id)


            # if "Error" in returnedMsg:
            #     raise Exception("StaticID not found for workspace {}, Reason: {}"
            #                     .format(workspace.id, returnedMsg))
            # else:
            #     workspace.staticId = returnedMsg

            if util.cname(case) == 'Case':
                print('Case', case.casename)

            for group in case.responsibilities.groupList:
                print("Group", group.id)

                if runNetworkOp:
                    if self.groupInterpreter.\
                            find_static_id(group, workspace.staticId) is not None:
                        self.groupList.append(group)
                    else:
                        raise Exception("cannot find static ID for group {} with name {} in workspace {}"
                                        .format(group.id, group.name, workspace.staticId))

            for user in case.responsibilities.userList:
                print("User", user.id)
                if runNetworkOp:
                    if self.userInterpreter.\
                            findStaticId(user, self.groupList) is not None:
                        self.userList.append(user)
                    else:
                        raise Exception(("cannot find static ID for user with reference ID {0}. " +
                                        "Please verify if the user reference ID is correct.")
                                        .format(user.id))

            print()

            print('casePrefix = ' + case.casePrefix.value)
            util.set_case_prefix(case.casePrefix.value)
            print('Workspace \n\tStaticID = {} \n\tID = {} \n'.format(
                workspace.staticId, workspace.id))

            #for group in self.groupList:
            #    print("\tgroup: staticId = {}, name = {}".
            #          format(group.staticId, group.name))

            print()

            for user in self.userList:
                print("\tuser: staticId = {}, id = {}".
                      format(user.staticId, user.id))

            print()
            ########################################
            # INTERPRET CLINICAL PATHWAYS ELEMENTS #
            ########################################

            for stage in case.stageList:

                taskAsAttributeList = []
                taskList = []

                for task in stage.taskList:

                    interpretedTask = \
                        taskInterpreter\
                            .interpret_task(task, stage.id)

                    taskAsAttributeList\
                        .append(interpretedTask['taskAsAttribute'])

                    taskList \
                        .append(interpretedTask['task'])

                    self.entityList\
                        .append(interpretedTask['taskAsEntity'])

                # TODO add task as stage attribute
                interpret_stage(stage, taskAsAttributeList, taskList)

            ############################################
            # END INTERPRET CLINICAL PATHWAYS ELEMENTS #
            ############################################
            caseEntitiesAndProps = entityGenerator.\
                generate_case_data_entities_and_props(settingObj=case.setting,
                                                      stages=case.stageList)
            self.entityList.extend(caseEntitiesAndProps['Entities'])

            print("Case Owner: "
                  "\n\tid: {}"
                  "\n\ttype: {}".format(
                    caseEntitiesAndProps["CaseOwner"].id,
                    caseEntitiesAndProps["CaseOwner"].type))

            print("\nAttrList size =", len(case.setting.attrList))
            for attr in case.setting.attrList:
                attributeInterpreter.interpret_attribute_object(attr)
                print("Attr ID " + attr.name)
                print("#Directives ", attr.attrProp.directive.type)

            print("\n Hook Info")
            for hook in case.hook:
                print("On {} invoke {}".format(hook.event, hook.url))

            for stage in case.stageList:
                print("\n Stage Info")
                directive = stage.directive
                print("\tDirectives: "
                      "\n\t\t mandatory = {}"
                      "\n\t\t repeatable = {}"
                      "\n\t\t activation = {}"
                      "\n\t\t multiplicity = {}".
                      format(directive.mandatory,
                             directive.repeatable,
                             directive.activation,
                             directive.multiplicity,))
                print("\tDescription: " + stage.description.value)
                print("\tOwnerPath: " + stage.ownerpath.value)
                print("\tDynamic Description Path: " + stage.dynamicDescriptionPath.value)
                print("\tExternal ID: " + stage.externalId.value)

                # Task interpret
                # for task in stage.taskList:
                #     directive = task.directive
                #     attrList = task.attrList
                #     dueDatePath = None
                #
                #     if util.cname(task) != 'AutomatedTask':
                #         if attrList.dueDatePath is not None:
                #             dueDatePath = attrList.dueDatePath.value
                #
                #     print("\n\tTask {}"
                #           "\n\t\tDirectives "
                #           "\n\t\t\tmandatory = {}"
                #           "\n\t\t\trepeatable = {}"
                #           "\n\t\t\tactivation = {}"
                #           "\n\t\t\tmultiplicity = {}"
                #           "\n\t\tdescription = {}"
                #           "\n\t\townerPath = {}"
                #           "\n\t\tdueDatePath = {}"
                #           "\n\t\texternalId = {}"
                #           "\n\t\tdynamicDescriptionPath = {}"
                #           .format(task.id,
                #                   directive.mandatory,
                #                   directive.repeatable,
                #                   directive.activation,
                #                   directive.multiplicity,
                #                   attrList.description.value,
                #                   ("None" if attrList.ownerPath is None else attrList.ownerPath.value ),
                #                   dueDatePath,
                #                   ("None" if attrList.externalId is None else attrList.externalId.value),
                #                   ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))
            # print("Case Definition", case.caseDef.caseDefName)

            caseInJson = self.compile_for_connecare(workspace, case)

            if runNetworkOp:
                response = requests.post(
                HttpRequest.sacmUrl + "import/acadela/casedefinition?version=1&isExecute=false",
                headers=HttpRequest.simulateUserHeader,
                json=json.loads(json.dumps(caseInJson)))
