import re
from sacm.interpreter.sentry import auto_parse_conditional_expression
from sacm.interpreter.sentry import interpret_precondition
from sacm.exception_handler.semantic_error_handler.utils import remove_attribute_prefix, find_line_number
import sacm.util as sacmUtil

def parse_field_expression(dynamic_field, task_fields, line_number):
    field_expression = dynamic_field.expression
    field_expression = str.strip(field_expression)
    pattern_keys = ["or", "and", "round", "number", "if", "else"]
    field_contains_pattern = any(pattern in field_expression for pattern in pattern_keys)
    print("Field expression in semancheck:", field_expression)
    # print("field_contains_pattern", field_contains_pattern)
    # If the dynamic field expression starts with the "if" keyword, then check for
    # the element paths inside it
    if field_expression.startswith("if"):
        if field_contains_pattern:
            parentheses = re.findall(r'\((.*?)\)', field_expression)
            fields_to_search = []
            for key in parentheses:
                field = re.findall(r'^(\'\")[a-zA-Z]+^(\'\")', key)
                print("founded field", field)
                fields_to_search = fields_to_search + field
            # parentheses = re.split('(and)|(or)', field_expression)
            fields_to_search = list(dict.fromkeys(fields_to_search))
            # print("fields_to_search", fields_to_search)
            field_ids = [field.id for field in task_fields]
            # print("field_ids", field_ids)
            for field in fields_to_search:
                if field not in pattern_keys and field not in field_ids:
                    raise Exception(
                        f"Semantic Error at line {line_number}! Invalid field {field} found in the expression of OutputField "
                        f"{dynamic_field.id}. Expected the ID of an InputField or OutputField declared in the same Form "
                        f"as OutputField {dynamic_field.id}.")


def parse_precondition(precondition_str, case_object_tree, line_number=(0, 0)):
    precondition_str = precondition_str.replace("(", "")\
                                        .replace(")", "")\
                                        .replace("\n", "")
    preconditions = re.split(r'( and )|( or )|(\+)' \
                             + '|[<>=]|[=]', precondition_str)

    for invalidElem in [None, "and", "or"]:
        preconditions = list(filter(lambda a: a != invalidElem, preconditions))

    for precondition in preconditions:
        if '.' not in precondition:
            continue
        precondition = precondition.replace(" ", "")
        split_precondition_path = precondition.split(".")
        print(precondition, split_precondition_path)
        precondition_start = split_precondition_path[0]
        # CASE 1: precondition is located in SETTING
        if 'Setting' in precondition_start:
            if len(split_precondition_path) < 2:
                raise Exception(f"Semantic Error at line {line_number}!\nInvalid precondition path '{precondition}'. "
                                f"The path does not point to an existing element. "
                                f"Make sure your path follows the below rule:"
                                f"\n\n Setting.&lt;AttributeName&gt;\n")
            field = re.split('\W+', split_precondition_path[1])[0]
            setting_list = case_object_tree["settings"][0].attribute
            setting_names = [setting.id for setting in setting_list]
            if field not in setting_names:
                raise Exception(
                    f"Semantic Error at line {line_number}! '{field}' not found in Settings. Invalid precondition path.")

        # CASE 2: precondition is located in TASK
        else:
            if len(split_precondition_path) != 3:
                raise Exception(f"Semantic Error at line {line_number}!\nInvalid precondition path '{precondition}'. "
                                f"The path does not point to an existing element. "
                                f"Make sure your path follows one of these rules:"
                                f"\n\n 1. &lt;StageName&gt;.&lt;TaskName&gt;.&lt;FieldName&gt;\n 2. Setting.&ltAttributeName&gt\n")
            precondition_stage = split_precondition_path[0]
            precondition_task = split_precondition_path[1]
            # precondition_field = re.split('\W+', split_precondition_path[2])[0]
            precondition_field = split_precondition_path[2]

            # check if stage name is valid
            stages = case_object_tree["stages"]
            found_stage = None
            found_task = None
            found_field = None

            for stage in stages:
                print(str.format("precond stage: {}| COT stage: {}",
                                 precondition_stage, stage.id.split("_")[1]))
                if stage.id.split("_")[1] == sacmUtil.unprefix(precondition_stage):
                    found_stage = stage
                    print("foundSTAGE", found_stage)
                    break

            if found_stage is None:
                raise Exception(
                    f"Semantic Error at line {line_number}! '{precondition_stage}' not found in Stages. "
                    f"Invalid precondition path.")
            else:
                task_list = stage.taskList
                for task in task_list:
                    print(f'taskID: {task.id.split("_")[1]} | precondTask: {sacmUtil.unprefix(precondition_task)}')
                    if task.id.split("_")[1] == sacmUtil.unprefix(precondition_task):
                        found_task = task
                        break
                if found_task is None:
                    raise Exception(
                        f"Semantic Error: Invalid reference path at line {line_number}! '{precondition_task}' Task does not exist."
                        f" Expect the ID of a defined Task in the Case.")
                else:
                    print("Task is found", precondition_task)
                    task_field_list = found_task.fieldList + found_task.dynamicFieldList
                    for field in task_field_list:
                        print(f"Field: {field.id} | PRecondField: {precondition_field}")
                        if field.id == precondition_field:
                            found_field = field
                            break
                    if found_field is None:
                        raise Exception(
                            f"Semantic Error at line {line_number}! {precondition_field} not found in Fields."
                            f" Invalid precondition path.")



def check_path_validity(case_object_tree, treatment_str):
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
        if (owner_path != 'None') and (owner_path is not None) and len(split_owner_path) > 1:
            # Check if first part is Setting and if so check if attr with that name exists and if owner
            # here technically I could have just traverse the whole settings
            # without dealing with patient and owner separately
            # then I would use the link for others and if
            for attr in setting_list:
                if attr.id == split_owner_path[1]:
                    owner_found = True
                    print("attr found:", attr.id)
                    if split_owner_path[1] == 'CaseOwner':
                        print("CHECKING IF CASE OWNER IN GROUP:")
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception(
                                f"Semantic Error at line {attr.lineNumber}! CaseOwner '{group_name}' "
                                f"not found in groups.")

                    elif split_owner_path[1] == 'CasePatient':
                        print("CHECKING IF CASE PATIENT IN GROUP:")
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception(
                                f"Semantic Error at line {attr.lineNumber}! CasePatient '{group_name}' "
                                f"not found in groups.")
                    else:
                        group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                        print("group name:", group_name)
                        if group_name not in group_names:
                            raise Exception(
                                f"Semantic Error at line {attr.lineNumber}! User '{group_name}' not found "
                                f"in users list under the Responsibilities section.")
                    break
            # ADD LINE NUMBER
            if not owner_found:
                line_number = find_line_number(treatment_str, task, split_owner_path[1])
                raise Exception(
                    f"Semantic Error at line {line_number}! Owner '{split_owner_path[1]}' not found in Settings.")

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
                        raise Exception(
                            f"Semantic Error at line {attr.lineNumber}! Due date value {attr.type}"
                            f" is not in date format.")
                    break
            if not due_date_found:
                line_number = find_line_number(treatment_str, task, split_due_date_path[1])
                raise Exception(
                    f"Semantic Error at line {line_number}! Due date {split_due_date_path[1]} not found in Settings.")

        # 1.3. CHECK TASK PRECONDITION
        print("1.3. CHECK TASK PRECONDITION:")
        task_precondition_list = task.preconditionList
        task_names = [task.id for task in task_list]
        stage_names = [stage.id for stage in case_stages]
        if len(task_precondition_list) > 0:
            for precondition in task_precondition_list:
                # NOW LIST IS BEING CHECKED
                for step in precondition.stepList:
                    if step not in task_names and step not in stage_names:
                        remove_field_prefix = remove_attribute_prefix(step)
                        line_number = find_line_number(treatment_str, precondition, remove_field_prefix)
                        raise Exception(
                            f"Semantic Error at line {line_number}! Task or Stage '{step}' in precondition not found.")
            if precondition.expression is not None:
                # if precondition has expression check path validity--DONE
                line_number = find_line_number(treatment_str, precondition, precondition.expression)
                parse_precondition(precondition.expression, case_object_tree, line_number)

        # CUSTOM FIELD CHECK
        print("CUSTOM FIELD CHECK:")
        static_task_fields = task.fieldList
        dynamic_task_fields = task.dynamicFieldList
        task_fields = static_task_fields + dynamic_task_fields
        # check dynamic fields
        for field in dynamic_task_fields:
            # print("Dynamic field attrs", field.id, field.path, field.explicitType, field.__dict__)
            if field.explicitType == 'custom':
                remove_field_prefix = remove_attribute_prefix(field.path)
                line_number = find_line_number(treatment_str, field, remove_field_prefix)
                parse_precondition(field.path, case_object_tree, line_number)
        # check static fields
        for field in static_task_fields:
            print("Static field attrs", field.id, field.path, field.type)
            if field.type == 'custom':
                remove_field_prefix = remove_attribute_prefix(field.path)
                line_number = find_line_number(treatment_str, field, remove_field_prefix)
                parse_precondition(field.path, case_object_tree, line_number)
        # check if it's starting with setting and do as usual
        # if not then check stage then task field
        # 1.4. CHECK TASK FORM DYNAMIC FIELDS
        print("1.4. CHECK TASK FORM DYNAMIC FIELDS' EXPRESSIONS:")
        task_dynamic_field_list = task.dynamicFieldList
        if len(task_dynamic_field_list) > 0:
            for field in task_dynamic_field_list:
                if field.expression:
                    line_number = find_line_number(treatment_str, field, "expression")
                    parse_field_expression(field, task_fields, line_number)

    # 2. SUMMARY PANEL RELATED CHECKS
    print("2. SUMMARY PANEL  RELATED CHECKS :")
    # THE SIZE OF SPLIT ARRAY SHOULD BE >=3 AND LAST ONE IS FIELD
    # IF IT'S TRUE THEN CHECK O.W. THROW EXCEPTION
    # ALSO CHECK THE STAGE -- DONE
    for summary in summary_list:
        info_path = summary.summaryParamList[0].split(".")
        # ADD LINES !!!
        if len(info_path) < 3:
            raise Exception(
                f"Semantic Error at line {summary.lineNumber}! Invalid info path {summary.summaryParamList[0]}."
                 f"The path does not point to an existing element. "
                                f"Make sure your path follows the following rule:"
                                f"\n 1. &lt;StageName&gt;.&lt;TaskName&gt;.&lt;FieldName&gt;\n ")
        info_path_stage = info_path[0]
        info_path_task = info_path[1]
        info_path_field = info_path[2]
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
        # ADD LINES !!!
        if found_stage is None:
            removed_prefix = remove_attribute_prefix(info_path_stage)
            line_number = find_line_number(treatment_str, summary, removed_prefix)
            raise Exception(
                f"Semantic Error at line {line_number}! {remove_attribute_prefix(info_path_stage)} not found in Stages. Invalid info path.")
        else:
            task_list = found_stage.taskList
            print("Stage is found", info_path_stage, task_list)
            for task in task_list:
                if task.id == info_path_task:
                    found_task = task
                    break
            # ADD LINES !!!
            if found_task is None:
                removed_prefix = remove_attribute_prefix(info_path_task)
                line_number = find_line_number(treatment_str, summary, removed_prefix)
                raise Exception(
                    f"Semantic Error at line {line_number}! '{removed_prefix}' "
                    f"not found in tasks of Stage {remove_attribute_prefix(info_path_stage)}. Invalid info path.")
            else:
                print("Task is found", info_path_task)
                task_field_list = found_task.fieldList + found_task.dynamicFieldList
                for field in task_field_list:
                    if field.id == info_path_field:
                        found_field = field
                        break
                # ADD LINES !!!
                if found_field is None:
                    removed_prefix = remove_attribute_prefix(info_path_field)
                    line_number = find_line_number(treatment_str, summary, removed_prefix)
                    raise Exception(
                        f"Semantic Error at line {line_number}! Field '{removed_prefix}' not found in Task "
                        f"{remove_attribute_prefix(info_path_task)}. Invalid info path.")

    # 3. CHECK STAGE OWNER & PRECONDITION
    stage_names = [stage.id for stage in case_stages]
    for stage in case_stages:
        # 3.1. CHECK STAGE OWNER
        print("3.1. CHECK STAGE OWNER ")
        owner_path = stage.ownerPath \
            if sacmUtil.is_attribute_not_null(stage, "ownerPath") \
            else None

        owner_found = False

        if (owner_path != 'None') and (owner_path is not None):
            split_owner_path = owner_path.split(".")
            for attr in setting_list:
                if attr.id == split_owner_path[1]:
                    owner_found = True
                    print("attr found:", attr.id)
                    group_name = attr.type.replace("Link.Users(", "").replace(")", "")
                    print("group name:", group_name)
                    if group_name not in group_names:
                        raise Exception(
                            f"Semantic Error at line {attr.lineNumber}! Stage Owner {group_name} not found in Groups!")
            if not owner_found:
                line_number = find_line_number(treatment_str, stage, split_owner_path[1])
                raise Exception(
                    f"Semantic Error at line {line_number}! Stage Owner '{split_owner_path[1]}' not found in Settings!")
        # 3.2. CHECK STAGE PRECONDITION
        print("3.2. CHECK STAGE PRECONDITION")
        if sacmUtil.is_attribute_not_null(stage, "preconditionList") and \
                len(stage.preconditionList) > 0:
            for precondition in stage.preconditionList:
                for step in precondition.stepList:
                    if step not in stage_names and step not in task_names:
                        remove_prefix = remove_attribute_prefix(step)
                        line_number = find_line_number(treatment_str, stage, remove_prefix)
                        raise Exception(
                            f"Semantic Error at line {line_number}! Stage or Task '{remove_prefix}' does not exist. "
                            f"Expect the ID of an existing Stage or Task.")
                # HERE ONLY CHECK IF THE PATH EXISTS AGAIN--DONE
                if precondition.expression is not None:
                    line_number = find_line_number(treatment_str, precondition, precondition.expression)
                    parse_precondition(precondition.expression, case_object_tree, line_number)
