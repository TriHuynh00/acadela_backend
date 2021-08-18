from http_request import HttpRequest
from referencer.group import GroupReferencer
import json

class UserReferencer:

    def __init__(self):
        self.groupController = GroupReferencer()

    def findAllUsers(self):
        allUserJson = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "users/",
            HttpRequest.defaultHeader)
        return allUserJson

    def findUserById(self, userId):
        groupJson = HttpRequest.get(
            HttpRequest.sociocortexUrl,
            "users/" + userId,
            HttpRequest.defaultHeader)
        return groupJson

    def findUserStaticIdByRefIdAndGroupID(self, refId, groupList):

        # Get the members in each group object and compare their refId with the target user's refId
        # that we want to get the staticId
        # print("GroupList", groupList)
        for group in groupList:
            groupJson = self.groupController.findGroupById(group.staticId)

            # Loop through member list to obtain member ID
            if groupJson is not "groupIdNotFound":
                # print(json.dumps(groupJson, indent=4))
                for member in groupJson['members']:

                    memberJsonObj = self.findUserById(member['id'])
                    if memberJsonObj is not None \
                        and member['resourceType'] == 'users':
                        # print(json.dumps(member['id'], indent=4))
                        # compare member's refId with the target userRefId
                        for attribute in memberJsonObj['attributes']:
                            if attribute['name'] == "refId":
                                if refId == attribute['values'][0]:
                                    return memberJsonObj['id']

        return "userStaticIdNotFound"

# uc = UserController()
# groupIdList = ["a412ac64923a11e7bd0c0242ac120002"]
# uid = uc.findUserStaticIdByRefIdAndGroupID("kurnosenkovi", groupIdList)
# print(uid)