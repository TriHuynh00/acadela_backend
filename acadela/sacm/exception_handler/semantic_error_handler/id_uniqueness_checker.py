def find_duplicate2(objects, list, field, identifier):
    seen = set()
    for x in list:
        if x in seen:
            found = next((item for item in objects if getattr(item, identifier) == x), None).lineNumber
            print("wtf is this",found)
            raise Exception(("{} IDs should be unique. {} is a duplicate at line and column {} " +
                             "Please verify if the IDs are unique.")
                            .format(field, x, found))
            return True, x
        seen.add(x)
    return False, None

def find_duplicate(list, field):
    seen = set()
    for x in list:
        if x in seen:
            raise Exception(("{} IDs should be unique.{} is a duplicate. " +
                             "Please verify if the IDs are unique.")
                            .format(field, x))
            return True, x
        seen.add(x)
    return False, None


def raise_not_unique_exception(field, item):
    raise Exception(("{} IDs should be unique.{} is a duplicate. " +
                     "Please verify if the IDs are unique.")
                    .format(field, item))


def check_id_uniqueness(case_object_tree):
    # TODO [Validation]: Check valid path value here
    # 1. Check Sentry ID & Condition match with any existing
    #    Stage.Task.Field Object
    #
    case_groups = case_object_tree["groups"]
    case_users = case_object_tree["users"]
    case_stages = case_object_tree["stages"]
    case_settings = case_object_tree["settings"][0].attribute
    case_task_list = case_object_tree["tasks"]


    print("###1.CHECK ID UNIQUENESS###\n")
    # 1.GROUP ID/NAME UNIQUENESS
    group_names = [group.name for group in case_groups]
    # group_duplicate = any(group_names.count(element) > 1 for element in group_names)
    dup, item = find_duplicate2(case_groups, group_names, "Group", "name")
    print("GROUP Names:", group_names)
    print("GROUP ID NOT UNIQUE", dup, item, "\n######\n")

    # 2.USER ID/NAME UNIQUENESS
    user_names = [user.name for user in case_users]
    # group_duplicate = any(group_names.count(element) > 1 for element in group_names)
    dup, item = find_duplicate2(case_users, user_names, "User", "name")
    print("USER Names:", user_names)
    print("USER ID NOT UNIQUE", dup, item, "\n######\n")

    # 3.STAGE ID/NAME UNIQUENESS
    stage_names = [stage.id for stage in case_stages]
    # stage_duplicate = any(stage_names.count(element) > 1 for element in stage_names)
    # print("STAGE ID NOT UNIQUE", stage_duplicate)
    dup, item = find_duplicate2(case_stages, stage_names, "Stage", "id")
    print("STAGE Names:", stage_names)
    print("STAGE ID NOT UNIQUE", dup, item, "\n######\n")

    # 4.SETTING ATTRIBUTES ID/NAME UNIQUENESS
    attribute_names = [setting.id for setting in case_settings]
    # attribute_duplicate = any(attribute_names.count(element) > 1 for element in attribute_names)
    dup, item = find_duplicate2(case_settings, attribute_names, "Setting", "id")
    print("ATTRIBUTE Names:", attribute_names)
    print("ATTRIBUTE ID NOT UNIQUE", dup, item, "\n######\n")

    # CHECK IF ATTRIBUTE IDS AND STAGE IDS ARE DISJOINT
    set_difference = set(stage_names) - set(attribute_names)
    list_difference = list(set_difference)
    if len(list_difference) < len(stage_names):
        duplicate_key = set(stage_names) - set(list_difference)
        raise Exception("Duplicate ID: {} Attribute ID can not be same with a Stage ID ".format(duplicate_key))

    # 5.TASK ID/NAME UNIQUENESS
    task_names = [task.id for task in case_task_list]
    dup, item = find_duplicate2(case_task_list, task_names, "Task","id")
    print("TASK Names:", task_names)
    print("TASK ID NOT UNIQUE", dup, item)

    # 6.FIELD ID/NAME UNIQUENESS
    for task in case_task_list:
        field_names = [field.id for field in task.fieldList]
        dynamic_field_names = [field.id for field in task.dynamicFieldList]
        field_names = field_names + dynamic_field_names
        dup, item = find_duplicate2(task.fieldList + task.dynamicFieldList, field_names, "Field","id")
        print("FIELD Names:", field_names)
        print("FIELD ID NOT UNIQUE", dup, item, "\n######\n")
