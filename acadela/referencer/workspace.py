from acadela.http_request import HttpRequest
import json

class WorkspaceReferencer:

    def __init__(self):
        pass

    def findWorkspaceStaticIdByRefId(self, refId):
        workspaceListJson = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "workspaces",
            HttpRequest.defaultHeader)

        if workspaceListJson != None:
            for workspace in workspaceListJson:
                # print(json.dumps(workspace, indent=4))
                if workspace['name'] == refId:
                    return workspace['id']
        else:
            return "invalidGetWorkspaceRequest"

        return "workspaceIdNotFound"

    def findPermissionGroupByStaticId(self, workspaceId):
        permissionIdList = []
        workspace = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "workspaces/" + workspaceId,
            HttpRequest.defaultHeader)

        if workspace != None:
            # print(json.dumps(workspace, indent=4))
            # print(json.dumps(workspace['permissions'], indent=4))
            if workspace['permissions'] is not None:
                for permission in workspace['permissions']:
                    permissionObj = workspace['permissions'][permission]
                    # print("Permission: ", permission)
                    if len(permissionObj) > 0:
                        if permissionObj[0]["id"] is not None:
                            permissionIdList.append(permissionObj[0]["id"])
                            # print(json.dumps(permissionObj[0]["id"]))
        else:
            return "invalidGetWorkspaceRequest"

        # print(permissionIdList)
        return permissionIdList

    # findPermissionGroupByStaticId("2c9480885d1737ef015d74deed260006")