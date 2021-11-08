import re
from sacm.interpreter.sentry import auto_parse_conditional_expression
from sacm.interpreter.sentry import interpret_precondition


def parse_field_expression(dynamic_field, fields):
    field_expression = dynamic_field.expression
    field_expression = field_expression
    pattern_keys = ["or", "and", "round", "number", "if", "else"]
    field_contains_pattern = any(pattern in field_expression for pattern in pattern_keys)
    print("field_contains_pattern", field_contains_pattern)
    if field_contains_pattern:
        parentheses = re.findall(r'\((.*?)\)', field_expression)
        fields_to_search = []
        for key in parentheses:
            field = re.findall(r'[a-zA-Z]+', key)
            print("founded field", field)
            fields_to_search = fields_to_search + field
        # parentheses = re.split('(and)|(or)', field_expression)
        fields_to_search = list(dict.fromkeys(fields_to_search))
        print("fields_to_search", fields_to_search)
        field_ids = [field.id for field in fields]
        print("field_ids", field_ids)
        for field in fields_to_search:
            if field not in pattern_keys and field not in field_ids:
                raise Exception(
                    "Invalid field {} found in expression of dynamic field {}!".format(field, dynamic_field.id))


def parse_precondition(precondition, case_object_tree):
    print("PARSING PRECONDITION", precondition)
    split_precondition_path = precondition.split(".")
    precondition_start = split_precondition_path[0]
    # CASE 1: precondition is located in SETTING
    if 'Setting' in precondition_start:
        if len(split_precondition_path) < 2:
            raise Exception("invalid precondition path {}!".format(precondition))
        field = re.split('\W+', split_precondition_path[1])[0]
        print("field", field)
        setting_list = case_object_tree["settings"][0].attribute
        setting_names = [setting.id for setting in setting_list]
        if field not in setting_names:
            raise Exception("invalid precondition path. {} not found in Settings!".format(precondition))

    # CASE 2: precondition is located in TASK
    else:
        if len(split_precondition_path) < 3:
            raise Exception("invalid precondition path {}!".format(precondition))
        precondition_stage = split_precondition_path[0]
        precondition_task = split_precondition_path[1]
        precondition_field = re.split('\W+', split_precondition_path[2])[0]

        # check if stage name is valid
        stages = case_object_tree["stages"]
        found_stage = None
        found_task = None
        found_field = None

        for stage in stages:
            if stage.id.split("_")[1] == precondition_stage:
                found_stage = stage
                break

        if found_stage is None:
            raise Exception("invalid precondition path. {} not found in stages!".format(precondition_stage))
        else:
            print("Stage is found", precondition_stage)
            task_list = stage.taskList
            for task in task_list:
                if task.id.split("_")[1] == precondition_task:
                    found_task = task
                    break
            if found_task is None:
                raise Exception("invalid precondition path. {} not found in tasks!".format(precondition_task))
            else:
                print("Task is found", precondition_task)
                task_field_list = found_task.fieldList + found_task.dynamicFieldList
                for field in task_field_list:
                    if field.id == precondition_field:
                        found_field = field
                        break
                if found_field is None:
                    raise Exception("invalid precondition path. {} not found in fields!".format(precondition_field))


def check_path_validity(case_object_tree):
    # 2. Check Field with custom path is pointed to a valid source
    #    Need to prefix the path afterward (using
    #    prefix_path_value() function in interpreter/util_intprtr
    print("CHECKING PATH VALIDITY")
    task_list = case_object_tree["tasks"]
    case_groups = case_object_tree["groups"]
    summary_list = case_object_tree["case"].summarySectionList
    case_stages = case_object_tree["stages"]
    setting_list = case_object_tree["settings"][0].attribute
    # TASK RELATED CHECKS
    print("1. TASK RELATED CHECKS:")
    # change the case here
    group_names = [group.name for group in case_groups]
    for task in task_list:
        print("CHECKING OWNER&DUE DATE VALIDITY", task.__dict__)
        owner_path = task.ownerPath
        owner_found = False
        due_date_found = False
        split_owner_path = owner_path.split(".")
        print("setting :", split_owner_path, owner_path)
        # 1.1 OWNER PATH CHECK
        print("1.1 OWNER PATH CHECK:")
        if (owner_path != 'None') and (owner_path is not None):
            # Check if first part is Setting and if so check if attr with that name exists and if owner
            # here technically I could have just traverse the whole settings
            # without dealing with patient and owner separately
            # then I would use the link for others and if
            for attr in setting_list:
                print("setting traverse:", attr.__dict__)
                if attr.id == split_owner_path[1]:
                    owner_found = True
                    print("attr found:", attr.id)
                    if split_owner_path[1] == 'CaseOwner':
                        print("CHECKING IF CASE OWNER IN GROUP:")
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception("CaseOwner not found in groups!")

                    elif split_owner_path[1] == 'CasePatient':
                        print("CHECKING IF CASE PATIENT IN GROUP:")
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception("CasePatient not found in groups!")
                    else:
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception("User {} not found in groups!".format(group_name))
                    break
            if not owner_found:
                raise Exception("Owner {} not found in settings!"
                                .format(split_owner_path[1]))

        print("1.2 DUE DATE PATH CHECK:")
        due_date_path = task.dueDatePath
        if due_date_path:
            split_due_date_path = due_date_path.split(".")
            for attr in setting_list:
                if attr.id == split_due_date_path[1]:
                    due_date_found = True
                    print("DUE DATE attr found:", attr.id, attr.type)
                    if attr.type.startswith("date."):
                        print("Due date attr value starts with 'date.' continue")
                    else:
                        # Syntax checker already detects this as a syntax error
                        raise Exception("Due date value {} is not in date format!"
                                        .format(attr.type))
                    break
            if not due_date_found:
                raise Exception("Due date {} not found in settings!"
                                .format(split_due_date_path[1]))

        # 1.3. CHECK TASK PRECONDITION
        print("1.3. CHECK TASK PRECONDITION:")
        task_precondition_list = task.preconditionList
        task_names = [task.id for task in task_list]
        if len(task_precondition_list) > 0:
            for precondition in task_precondition_list:
                # NOW LIST IS BEING CHECKED
                for step in precondition.stepList:
                    print("precondition:", step)
                    if step not in task_names:
                        raise Exception("Task {} in precondition not found!".format(step))
            if precondition.expression is not None:
                # if precondition has expression check path validity--DONE
                parse_precondition(precondition.expression, case_object_tree)

        # CUSTOM FIELD CHECK
        print("CUSTOM FIELD CHECK:")
        static_task_fields = task.fieldList
        dynamic_task_fields = task.dynamicFieldList
        task_fields = static_task_fields + dynamic_task_fields
        # check dynamic fields
        for field in dynamic_task_fields:
            print("Dynamic field attrs", field.id, field.path, field.explicitType)
            if field.explicitType == 'custom':
                parse_precondition(field.path, case_object_tree)
        # check static fields
        for field in static_task_fields:
            print("Static field attrs", field.id, field.path, field.type)
            if field.type == 'custom':
                parse_precondition(field.path, case_object_tree)
        # check if it's starting with setting and do as usual
        # if not then check stage then task field
        # 1.4. CHECK TASK FORM DYNAMIC FIELDS
        print("1.4. CHECK TASK FORM DYNAMIC FIELDS' EXPRESSIONS:")
        task_dynamic_field_list = task.dynamicFieldList
        if len(task_dynamic_field_list) > 0:
            for field in task_dynamic_field_list:
                if field.expression:
                    print("the expression:", field.expression)
                    parse_field_expression(field, task_fields)
                    # prefixed_condition = auto_parse_conditional_expression(field.expression, case_stages)
                    # print("prefixed_condition:", prefixed_condition)

    # 2. SUMMARY PANEL RELATED CHECKS
    print("2. SUMMARY PANEL  RELATED CHECKS :")
    # THE SIZE OF SPLIT ARRAY SHOULD BE >=3 AND LAST ONE IS FIELD
    # IF IT'S TRUE THEN CHECK O.W. THROW EXCEPTION
    # ALSO CHECK THE STAGE -- DONE
    for summary in summary_list:
        info_path = summary.summaryParamList[0].split(".")
        if len(info_path) < 3:
            raise Exception("Invalid info path {}!".format(summary.summaryParamList[0]))
        info_path_stage = info_path[0]
        info_path_task = info_path[1]
        info_path_field = info_path[2]
        print("INFO_PATH:", info_path_field, info_path_task)
        found_stage = None
        found_task = None
        found_field = None
        stage_names = [stage.id for stage in case_stages]
        print("stage_names", stage_names)
        for stage in case_stages:
            print("stage_id", stage.id)
            if stage.id == info_path_stage:
                found_stage = stage
                break
        if found_stage is None:
            raise Exception("invalid info path. {} not found in stages!".format(info_path_stage))
        else:
            task_list = found_stage.taskList
            print("Stage is found", info_path_stage, task_list)
            for task in task_list:
                if task.id == info_path_task:
                    found_task = task
                    break
            if found_task is None:
                raise Exception("Task {} in InfoPath not found!".format(info_path_task))
            else:
                print("Task is found", info_path_task)
                task_field_list = found_task.fieldList + found_task.dynamicFieldList
                for field in task_field_list:
                    if field.id == info_path_field:
                        found_field = field
                        break
                if found_field is None:
                    raise Exception("Form Field {} not found!".format(info_path_field))

    # 3. CHECK STAGE OWNER & PRECONDITION
    stage_names = [stage.id for stage in case_stages]
    for stage in case_stages:
        # 3.1. CHECK STAGE OWNER
        print("3.1. CHECK STAGE OWNER ")
        owner_path = stage.ownerPath
        split_owner_path = owner_path.split(".")
        if (owner_path != 'None') and (owner_path is not None):
            for attr in setting_list:
                if attr.id == split_owner_path[1]:
                    print("attr found:", attr.id)
                    group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                    print("group name:", group_name)
                    if group_name not in group_names:
                        raise Exception("Stage owner not found in groups!")
        # 3.2. CHECK STAGE PRECONDITION
        print("3.2. CHECK STAGE PRECONDITION")
        if len(stage.preconditionList) > 0:
            for precondition in stage.preconditionList:
                for step in precondition.stepList:
                    if step not in stage_names:
                        raise Exception("Stage {} in precondition not found!".format(precondition.stepList))
                # HERE ONLY CHECK IF THE PATH EXISTS AGAIN--DONE
                if precondition.expression is not None:
                    parse_precondition(precondition.expression, case_object_tree)
