# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from acadela.referencer.workspace import WorkspaceController
from acadela.referencer.group import GroupController
from acadela.referencer.user import UserController
from acadela.httprequest import HttpRequest
import json
import requests

this_folder = dirname(__file__)

def cname(o):
    return o.__class__.__name__

class Interpreter():

    def __init__(self, metamodel, model):
        self.metamodel = metamodel
        self.model = model
        self.refFinder = WorkspaceController
        self.groupFinder = GroupController()
        self.userFinder = UserController()
        self.groupList = []
        self.userList = []

    # Interpret the case object
    def interpret(self):
        model = self.model
        workspace = model.defWorkspace

        # Pure Object Import
        if workspace == None:
            for defObj in model.defObj:
                if cname(defObj.object) == 'Entity':
                    obj = defObj.object;
                    print(obj.name)
                    for attr in obj.attr:
                       print('{} = {}'.format(cname(attr), attr.value))
        else:
            caseObjList = {}

            workspace = model.defWorkspace.workspace

            workspace.staticId = self.refFinder.findWorkspaceStaticIdByName(workspace.id)

            case = model.defWorkspace.workspaceProp.case

            if cname(case) == 'Case':
                print('Case', case.casename)

            # Interpret caseAttr
            # print('CaseAttr', case.caseAttr.prefix.pattern)

            # gc = GroupController()
            for group in case.userGroupList:
                group.staticId = self.groupFinder.findGroupStaticIdByName(group.name, workspace.staticId)
                if group.staticId is not "groupIdNotFound":
                    self.groupList.append(group)

            for user in case.userList:
                user.staticId = self.userFinder.findUserStaticIdByRefIdAndGroupID(user.id, self.groupList)
                self.userList.append(user)

            print()

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

            workspaceObjList = {}
            workspaceObjList["$"] = \
                {
                    "staticId": workspace.staticId,
                    "id": workspace.id
                }



            jsonGroupList = []
            for group in self.groupList:
                jsonGroupList.append({
                    "$": {
                        "staticId": str(group.staticId),
                        "id": str(group.name)
                    }
                })

            caseObjList['Group'] = jsonGroupList

            jsonUserList = []
            for user in self.userList:
                jsonUserList.append({
                    "$": {
                        "staticId": str(user.staticId),
                        "id": str(user.id)
                    }
                })

            caseObjList['User'] = jsonUserList

            jsonEntityList = []
            for entity in case.attrList.entity:
                # TODO: Crafting entityType based on casePrefix
                entityType = ""
                if len(entity.type) == 1:
                    entityType = entity.type

                print('entity', entity.name)

                print('\tmultiplicity: {} \n\t description: {}'.format(entity.multiplicity.value, entity.description.value))

                jsonEntityList.append({
                    "$": {
                        "id": entity.name,
                        "description": entity.description.value
                    }
                })

            workspaceObjList["EntityDefinition"] = \
                jsonEntityList

            # workspaceObjList.append({
            #     'EntityDefinition': jsonEntityList
            # })

            caseObjList["Workspace"] = [workspaceObjList]

            caseDefJson = {"SACMDefinition": caseObjList}

            caseDefJsonFinal = {"jsonTemplate": caseDefJson}

            # print(json.dumps(caseDefJson['SACMDefinition']['Group'], indent=4))

            print(json.dumps(caseDefJsonFinal, indent=4))
            # print(str('{ "jsonTemplate"' + ":" + json.dumps(caseDefJson, indent=4)) + "}")
            print()
            response = HttpRequest.post(HttpRequest.sacmUrl,
                             "import/acadela/casedefinition?version=11&isExecute=false",
                             header=HttpRequest.simulateUserHeader,
                             body=caseDefJsonFinal)
            # response = requests.post(
            #     HttpRequest.sacmUrl + "import/acadela/casedefinition?version=10&isExecute=false",
            #     headers=HttpRequest.simulateUserHeader,
            #     json=json.loads(json.dumps(caseDefJsonFinal)))
            print(json.dumps(response, indent=4))

        # for caseAttr in case.caseAttrList.attr:
        #     # print('CaseAttr', cname(caseAttr))
        #     if cname(caseAttr) == 'CasePrefix':
        #         print('Case Prefix =', caseAttr.pattern)
        #     if cname(caseAttr) == 'Multiplicity':
        #         print('Multiplicity =', caseAttr.multiplicity)
        #     if cname(caseAttr) == 'UiReference':
        #         print('UiReference', caseAttr.uiRef)

