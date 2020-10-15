# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from acadela.referencer.workspace import WorkspaceReferencer
from acadela.referencer.group import GroupReferencer
from acadela.referencer.user import UserReferencer
from acadela.interpreter.group import GroupInterpreter
from acadela.interpreter.user import UserInterpreter
from acadela.interpreter.workspace import WorkspaceInterpreter
from acadela.httprequest import HttpRequest
from acadela.interpreter import jsonutil
from acadela.interpreter import util
import json
import requests

this_folder = dirname(__file__)

class Interpreter():

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
        self.userList = []
        self.jsonEntityList = []
        self.jsonAttributeList = []

    # Interpret the case object
    def interpret(self):
        model = self.model
        workspace = model.defWorkspace

        # Pure Object Import
        if workspace == None:
            for defObj in model.defObj:
                if util.cname(defObj.object) == 'Entity':
                    obj = defObj.object;
                    print(obj.name)
                    for attr in obj.attr:
                       print('{} = {}'.format(util.cname(attr), attr.value))
        else:
            caseObjList = {}

            workspace = model.defWorkspace.workspace

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

            for group in case.userGroupList:
                if self.groupInterpreter.\
                        findStaticId(group, workspace.staticId) is not None:
                    self.groupList.append(group)
                else:
                    raise Exception("cannot find static ID for group {} with name {} in workspace {}"
                                    .format(group.id, group.name, workspace.staticId))

            for user in case.userList:
                if self.userInterpreter.\
                        findStaticId(user, self.groupList) is not None:
                    self.userList.append(user)
                else:
                    raise Exception(("cannot find static ID for user with reference ID {0}. " +
                                    "Please verify if the user reference ID is correct.")
                                    .format(user.id))

            print()

            print('casePrefix = ' + case.casePrefix.value)

            print('Workspace \n\tStaticID = {} \n\tID = {} \n'.format(
                workspace.staticId, workspace.id))

            for group in self.groupList:
                print("\tgroup: staticId = {}, name = {}".
                      format(group.staticId, group.name))

            print()

            for user in self.userList:
                print("\tuser: staticId = {}, id = {}".
                      format(user.staticId, user.id))

            print()

            print("Case Definition", case.caseDef.caseDefName)

            workspaceObjList = self.workspaceInterpreter\
                                   .workspacePropToJson(workspace, case)

            # Check if there is any Error being returned
            if workspaceObjList.get("Error") is None:
                caseObjList["Workspace"] = [workspaceObjList]
            else:
                raise Exception("Invalid workspace {} with error: {}"
                                .format(workspace.staticId, workspaceObjList["Error"]))

            caseObjList['Group'] = jsonutil.basicIdentityListToJson(self.groupList)

            caseObjList['User'] = jsonutil.basicIdentityListToJson(self.userList)

            caseDefJson = {"SACMDefinition": caseObjList}

            caseDefJsonFinal = {"jsonTemplate": caseDefJson}

            print(json.dumps(caseDefJsonFinal, indent=4))
            print()

            response = requests.post(
                HttpRequest.sacmUrl + "import/acadela/casedefinition?version=9&isExecute=false",
                headers=HttpRequest.simulateUserHeader,
                json=json.loads(json.dumps(caseDefJsonFinal)))

