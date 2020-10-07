from acadela.http_request import HttpRequest
from acadela.sc_controller.workspace import WorkspaceController
import json

class GroupController:

    def __init__(self):
        pass

    def findGroupById(self, groupId):
        groupJson = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "groups/" + groupId,
            HttpRequest.defaultHeader)
        return groupJson

    def findGroupStaticIdByName(self, groupName, workspaceId):
        permissionIdList = WorkspaceController.findPermissionGroupByStaticId(workspaceId)

        for permissionId in permissionIdList:
            permissionGroupObj = self.findGroupById(permissionId)
            print(json.dumps(permissionGroupObj['members'], indent = 4))
            for groupObj in permissionGroupObj['members']:
                if groupObj['name'] == groupName:
                    print(groupName + " found" + ' in ',permissionGroupObj['members'])
                    return groupObj['id']


            #
            # GroupListJson = HttpRequest.get(
            #     HttpRequest.sociocortexUrl,
            #     "groups/",
            #     HttpRequest.defaultHeader)

            # if workspaceListJson != None:
            #     for workspace in workspaceListJson:
            #         print(json.dumps(workspace, indent=4))
            #         if workspace['name'] == name:
            #             return workspace['id']
            # else:
            #     return "invalidGetWorkspaceRequest"

        return "groupIdNotFound"

# gc = GroupController()
# gid = gc.findGroupStaticIdByName("Umcg Anesthesiologist", "2c9480885d1737ef015d74deed260006")
# print(gid)