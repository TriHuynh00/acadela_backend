
def find_line_number(treatment_str, parent, field):
    init_line = parent.lineNumber[0]
    print("to find:", parent, field, init_line)
    treatment_str_lines = treatment_str.splitlines()
    line_index = None
    for index, item in enumerate(treatment_str_lines[init_line - 1:]):
        if field in item:
            line_index = index
            break
    if line_index is not None:
        line_index = line_index + init_line
    return line_index
