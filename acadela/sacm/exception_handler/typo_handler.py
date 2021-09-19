from spellchecker import SpellChecker
import json
import re


def generate_dictionary(attribute_list):
    spell = SpellChecker(language=None)
    spell.distance = 2
    attribute_dict = {}
    for attr in attribute_list:
        key = attr.replace("'", "")
        attribute_dict[key] = 10
    # print(attribute_dict)
    with open('dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(attribute_dict, f, ensure_ascii=False, indent=4)
    spell.word_frequency.load_dictionary('dictionary.json')
    return spell


def typo_handler(error, attribute_list, error_line_str):
    spell = generate_dictionary(attribute_list)
    error_message = error.message
    error_line = error.line
    error_column = error.col
    print("????", error_line_str, error_line_str[error_column-1:])
    misspelled = error_line_str[error_column-1:len(error_line_str)]
    misspelled = misspelled.split(' ', 1)[0]
    print("misspelled",misspelled)
    #misspelled = [t for t in error_message.split() if t.startswith('*')]
    #if misspelled == []:
        # return error_message
    #else:
        #misspelled = misspelled[0]
    #misspelled = misspelled.replace("*", "")
    # DO WE WANT THIS?
    if any(ext in misspelled for ext in attribute_list):
        print("???", misspelled)
    res = [ele for ele in attribute_list if (ele in misspelled)]
    print("res", res)
    # print("missing space between ", res, " and ", misspelled.replace(res, ""))
    # end extra

    # check for most likely correction
    candidate_attr = spell.correction(misspelled)
    print("SUGGESTION", candidate_attr)
    if candidate_attr == misspelled:
        # print("No keyword ", misspelled)
        if len(res) == 0:
            typo_text = "No keyword " + misspelled + '\n'
        elif res[0] == misspelled:
            typo_text = "This is the place to handle it maybe?\n"
        else:
            typo_text = "No keyword " + misspelled + ". Did you meant: " + res[0] + '?\n'
    else:
        typo_text = "No keyword " + misspelled + ". Did you meant: " + candidate_attr + '?\n'

    # error_text = error_message.replace(")\s", "").replace("'(", "'")
    # error_message = typo_text + '\n' + error_message
    return typo_text
