import csv
from os.path import dirname
import sys


def url_validator(case_object_tree):
    print("url validator")
    task_list = case_object_tree["tasks"]
    case_object = case_object_tree["case"]
    case_hooks = case_object.caseHookEvents
    this_folder = dirname(__file__)
    workspace_name = case_object_tree["workspace"].workspace.name

    with open(this_folder + "/trusted_urls.csv", 'r') as f:
        rows = csv.reader(f)
        missing_hook = None
        method_missing = False
        allowed_methods = []
        for task in task_list:
            if len(task.hookList) > 0:
                for hook in task.hookList:
                    found_url = False
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
                                    allowed_methods = row_csv[2]
                                    break
                            else:
                                found_url = True
                                break
                            # break
                    if not found_url:
                        missing_hook = hook
                        break
                if missing_hook:
                    line_number_text = f"at line {str(missing_hook.lineNumber[0])}"
                    if method_missing:
                        raise Exception(
                            f"The URL {missing_hook.url} {line_number_text} does not "
                            f"accept the HTTP method {missing_hook.method}. Allowed methods for this URL: {allowed_methods}. ")
                    else:
                        raise Exception(
                            f"The URL {missing_hook.url} {line_number_text} is not in the list "
                            f"of trusted sources for workspace {workspace_name}. "
                            f"Please check the trusted sources list for the permitted URLs \n")
        if len(case_hooks) > 0:
            method_missing = False
            for hook in case_hooks:
                found = False
                f.seek(0)  # <-- set the iterator to beginning of the input file
                for row in rows:
                    # if current rows 2nd value is equal to input, print that row
                    if hook.url == row[1] and workspace_name == row[0]:
                        if hook.method is not None:
                            if hook.method in row[2]:
                                found = True
                                break
                            else:
                                method_missing = True
                                missing_hook = hook
                                allowed_methods = row[2]
                                break
                        else:
                            found = True
                            break
                        # break
                if not found:
                    missing_hook = hook
                    break
            if missing_hook:
                line_number_text = f"at line {str(missing_hook.lineNumber[0])} " #and column {str(missing_hook.lineNumber[1])}"
                if method_missing:
                    raise Exception(f"The URL {missing_hook.url} {line_number_text} does not accept the HTTP method "
                                    f"{missing_hook.method}.  Allowed methods: {allowed_methods}."
                                    f"Please further check the trusted sources list for the permitted methods.\n ")
                else:
                    raise Exception(
                        f"The URL {missing_hook.url} {line_number_text} "
                        f"is not in the list of trusted sources for the workspace "
                        f"{workspace_name}. Please check the trusted sources list for the permitted URLs \n")
