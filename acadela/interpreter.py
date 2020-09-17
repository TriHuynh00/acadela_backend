# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
import colored as colored

from pointmodel.point import Point


def cname(o):
    return o.__class__.__name__

class Interpreter():
    def __init__(self, model):
        self.model = model

    # Interpret the case object
    def interpret(self):
        model = self.model
        workspace = model.workspace

        print('Workspace \n\t StaticID = {} \n\t ID = {} \n'.format(
              workspace.staticId, workspace.id))

        case = model.workspaceProp.case

        if cname(case) == 'Case':
            print('Case', case.casename)

        # Interpret caseAttr
        # print('CaseAttr', case.caseAttr.prefix.pattern)

        for userGroup in case.userGroupList:
            print("\tgroup: staticId = {}, id = {}".
                  format(userGroup.staticId, userGroup.id))

        print()

        for user in case.userList:
            print("\tuser: staticId = {}, id = {}".
                  format(user.staticId, user.id))

        print()

        for entity in case.attrList.entity:
            # TODO: Crafting entityType based on casePrefix
            entityType = ""
            if len(entity.type) == 1:
                entityType = entity.type[0].type
            print("\tentity "
                  "\n\t\t name = {0}"
                  "\n\t\t description = {1}"
                  "\n\t\t multiplicity = {2}"
                  "\n\t\t type = {3} \n"
                  .format(entity.name,
                          entity.attr[0].description,
                          entity.attr[1].multiplicity,
                          entityType))


        # for caseAttr in case.caseAttrList.attr:
        #     # print('CaseAttr', cname(caseAttr))
        #     if cname(caseAttr) == 'CasePrefix':
        #         print('Case Prefix =', caseAttr.pattern)
        #     if cname(caseAttr) == 'Multiplicity':
        #         print('Multiplicity =', caseAttr.multiplicity)
        #     if cname(caseAttr) == 'UiReference':
        #         print('UiReference', caseAttr.uiRef)

