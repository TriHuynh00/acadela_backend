import csv
from os.path import dirname
import sys


def url_validator(case_object_tree):
    print("url validator")
    task_list = case_object_tree["tasks"]
    case_object = case_object_tree["case"]
    print("case_dict", case_object.__dict__)
    case_hooks = case_object.caseHookEvents
    this_folder = dirname(__file__)
    workspace_name = case_object_tree["workspace"].workspace.name
    print(case_object_tree["workspace"].workspace.name)
    with open(this_folder + "/trusted_urls.csv", 'r') as f:
        rows = csv.reader(f)
        missing_hook = None
        method_missing = False
        for task in task_list:
            if len(task.hookList) > 0:
                print(task.hookList)
                print(task.__dict__)
                print("Checking Tasks:")
                for hook in task.hookList:
                    found_url = False
                    print("hook: ", hook.__dict__)
                    f.seek(0)  # <-- set the iterator to beginning of the input file
                    for row_csv in rows:
                        # if current rows 2nd value is equal to input, print that row
                        if hook.url == row_csv[1] and workspace_name == row_csv[0]:
                            if hook.method is not None:
                                if hook.method in row_csv[2]:
                                    print("found", row_csv)
                                    found_url = True
                                    break
                                else:
                                    method_missing = True
                                    missing_hook = hook
                                    break
                            else:
                                found_url = True
                                break
                            # break
                    if not found_url:
                        print("??? not found", found_url)
                        missing_hook = hook
                        break
                if missing_hook:
                    if method_missing:
                        raise Exception("The URL {} doesn't accept the HTTP method {} at line {}. Please check the "
                                        "trusted sources list for the permitted methods\n ".format(missing_hook.url,
                                                                                                   missing_hook.method,
                                                                                                   missing_hook.line_number))
                    else:
                        raise Exception(
                            "The URL {}  at line {} is not in the list of trusted sources for workspace {}. "
                            "Please check the trusted sources list for the permitted URLs \n".format(
                                missing_hook.url, workspace_name, missing_hook.line_number))
        if len(case_hooks) > 0:
            method_missing = False
            for hook in case_hooks:
                found = False
                f.seek(0)  # <-- set the iterator to beginning of the input file
                for row in rows:
                    # if current rows 2nd value is equal to input, print that row
                    if hook.url == row[1] and workspace_name == row[0]:
                        print("IT'S HERE", hook.url)
                        if hook.method is not None:
                            if hook.method in row[2]:
                                print("found", row)
                                found = True
                                break
                            else:
                                method_missing = True
                                missing_hook = hook
                                break
                        else:
                            found = True
                            break
                        # break
                if not found:
                    missing_hook = hook
                    break
            if missing_hook:
                if method_missing:
                    raise Exception("The URL {} doesn't accept the HTTP method {} at line {}. Please check the "
                                    "trusted sources list for the permitted methods\n ".format(missing_hook.url,
                                                                                               missing_hook.method,
                                                                                               missing_hook.line_number))
                else:
                    raise Exception("The URL {}  at line {} is not in the list of trusted sources for workspace {}. "
                                    "Please check the trusted sources list for the permitted URLs \n".format(
                        missing_hook.url, workspace_name, missing_hook.line_number))
