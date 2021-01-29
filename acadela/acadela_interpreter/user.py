from acadela.referencer.user import UserReferencer

class UserInterpreter():

    def __init__(self):
        self.userFinder = UserReferencer()

    def findStaticId(self, user, groupList):
        user.staticId = self.userFinder.findUserStaticIdByRefIdAndGroupID(user.id, groupList)
        if user.staticId is not "userStaticIdNotFound":
            return user
        else:
            return None
