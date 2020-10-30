from acadela.referencer.group import GroupReferencer

class GroupInterpreter:

    def __init__(self):
        self.groupFinder = GroupReferencer()

    def findStaticId(self, group, workspaceStaticId):
        group.staticId = self.groupFinder.findGroupStaticIdByName(group.name, workspaceStaticId)
        if group.staticId is not "groupIdNotFound":
            return group
        else:
            return None

    def groupListToJson(self, groupList):
        jsonGroupList = []
        for group in groupList:
            jsonGroupList.append({
                "$": {
                    "staticId": str(group.staticId),
                    "id": str(group.id)
                }
            })
        return jsonGroupList