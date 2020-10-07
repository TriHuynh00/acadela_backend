# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.
from os.path import dirname
from acadela.sc_controller.workspace import WorkspaceController
from acadela.sc_controller.group import GroupController

this_folder = dirname(__file__)

def cname(o):
    return o.__class__.__name__

class Interpreter():
    def __init__(self, metamodel, model):
        self.metamodel = metamodel
        self.model = model
        self.refFinder = WorkspaceController
        self.groupFinder = GroupController

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
            workspace = model.defWorkspace.workspace

            workspace.staticId = self.refFinder.findWorkspaceStaticIdByName(workspace.id)



            case = model.defWorkspace.workspaceProp.case

            if cname(case) == 'Case':
                print('Case', case.casename)

            # Interpret caseAttr
            # print('CaseAttr', case.caseAttr.prefix.pattern)

            gc = GroupController()
            for userGroup in case.userGroupList:
                userGroup.staticId = gc.findGroupStaticIdByName(userGroup.id, workspace.staticId)

            print()

            print('Workspace \n\tStaticID = {} \n\tID = {} \n'.format(
                workspace.staticId, workspace.id))

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
                    entityType = entity.type

                print('entity', entity.name)
                for attr in entity.attr:
                    print('\t{} = {}'.format(cname(attr), attr.value))
                print()


            print("Case Definition", case.caseDef.caseDefName)


        # for caseAttr in case.caseAttrList.attr:
        #     # print('CaseAttr', cname(caseAttr))
        #     if cname(caseAttr) == 'CasePrefix':
        #         print('Case Prefix =', caseAttr.pattern)
        #     if cname(caseAttr) == 'Multiplicity':
        #         print('Multiplicity =', caseAttr.multiplicity)
        #     if cname(caseAttr) == 'UiReference':
        #         print('UiReference', caseAttr.uiRef)

