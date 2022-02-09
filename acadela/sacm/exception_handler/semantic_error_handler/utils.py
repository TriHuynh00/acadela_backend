
def remove_attribute_prefix(str):
    remove_prefix = str.split('_')
    if len(remove_prefix) > 1:
        remove_prefix = remove_prefix[1]
    else:
        remove_prefix = remove_prefix[0]
    return remove_prefix

def find_line_number(treatment_str, parent, field):
    init_line = parent.lineNumber[0]
    print("to find:", parent, field, init_line)
    treatment_str_lines = treatment_str.splitlines()
    init_line_str = treatment_str_lines[init_line - 1]
    print(init_line_str)
    line_index = None
    for index, item in enumerate(treatment_str_lines[init_line - 1:]):
        if field in item:
            line_index = index
            break
    if line_index is not None:
        line_index = line_index + init_line
        print(line_index)
    return line_index
