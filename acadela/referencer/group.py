from acadela.httprequest import HttpRequest
from acadela.referencer.workspace import WorkspaceReferencer
import json

class GroupReferencer:

    def __init__(self):
        groupPrincipalTypes = ['members', '']
        self.workspaceFinder = WorkspaceReferencer()

    def findGroupById(self, groupId):
        groupJson = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "groups/" + groupId,
            HttpRequest.defaultHeader)
        return groupJson

    def findGroupStaticIdByName(self, groupName, workspaceId):
        permissionIdList = self.workspaceFinder.findPermissionGroupByStaticId(workspaceId)
        # print ("permissionIdList", permissionIdList)
        for permissionId in permissionIdList:

            permissionGroupObj = self.findGroupById(permissionId)
            # print(json.dumps(permissionGroupObj['members'], indent = 4))
            # print("GName ", groupName, " permissionId", permissionId, " PGroupObj ", json.dumps(permissionGroupObj, indent=4))

            # For a single group object, get the name of the group
            if permissionGroupObj['name'] == groupName\
                and permissionGroupObj['resourceType'] == 'groups':
                return permissionGroupObj['id']
            # Otherwise, check the members list,
            else:
                for groupObj in permissionGroupObj['members']:
                    # If this is a user member, skip
                    if groupObj['resourceType'] == 'groups' \
                        and groupObj['name'] == groupName:
                        # print(groupName + " found" + ' in ', permissionGroupObj['members'])
                        return groupObj['id']

        return "groupIdNotFound"

# gc = GroupController()
# gid = gc.findGroupStaticIdByName("Umcg Anesthesiologist", "2c9480885d1737ef015d74deed260006")
# print(gid)