def basicIdentityListToJson(objList):
    jsonObjList = []
    # TODO: Check if the staticId and id exist
    for obj in objList:
        jsonObjList.append({
            "$": {
                "staticId": str(obj.staticId),
                "id": str(obj.name)
            }
        })
    return jsonObjList
