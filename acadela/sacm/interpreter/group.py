from acadela.referencer.group import GroupReferencer

class GroupInterpreter:

    def __init__(self):
        self.groupFinder = GroupReferencer()

    def find_static_id(self, group, workspaceStaticId):
        group.staticId = self.groupFinder.findGroupStaticIdByName(group.groupName, workspaceStaticId)
        if group.staticId is not "groupIdNotFound":
            return group
        else:
            return None

    def group_list_to_json(self, groupList):
        jsonGroupList = []
        for group in groupList:
            jsonGroupList.append({
                "$": {
                    "staticId": str(group.staticId),
                    "id": str(group.name)
                }
            })
        return jsonGroupList