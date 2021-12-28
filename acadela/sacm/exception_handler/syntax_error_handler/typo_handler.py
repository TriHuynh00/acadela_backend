from spellchecker import SpellChecker
import json
import re


def generate_dictionary(attribute_list):
    spell = SpellChecker(language=None, case_sensitive=True)
    spell.distance = 2
    attribute_dict = {}
    for attr in attribute_list:
        key = attr.replace("'", "")
        attribute_dict[key] = 10
    with open('dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(attribute_dict, f, ensure_ascii=False, indent=4)
    spell.word_frequency.load_dictionary('dictionary.json')
    return spell


def typo_handler(error, attribute_list, hash_attributes, error_line_str):
    spell = generate_dictionary(attribute_list)
    error_message = error.message
    error_line = error.line
    error_column = error.col
    print("Line with error:", error_line_str, error_line_str[error_column - 1:])
    misspelled = error_line_str[error_column - 1:len(error_line_str)]
    print(re.split('[\W|\d]+', misspelled))
    misspelled = re.split('[\W|\d]+', misspelled)[0]
    #misspelled = misspelled.split(' ', 1)[0].split('(',1)[0]
    print("Misspelled word:", misspelled)
    # misspelled = [t for t in error_message.split() if t.startswith('*')]
    # if misspelled == []:
    # return error_message
    # else:
    # misspelled = misspelled[0]
    # misspelled = misspelled.replace("*", "")
    # DO WE WANT THIS?
    # if any(ext in misspelled for ext in attribute_list):
    #    print("???", misspelled)
    res = [ele for ele in attribute_list if (ele.lower() in misspelled.lower())]
    print("Attributes included in misspelled:", res)

    # check for most likely correction
    candidate_attr = spell.correction(misspelled)
    print("SUGGESTION from spell checker:", candidate_attr)

    if candidate_attr == misspelled:
        # print("No keyword ", misspelled)
        if len(res) == 0:
            typo_text = "No keyword " + misspelled + '\n'
        elif misspelled in res or misspelled in hash_attributes:
            # check for hash
            if hash_attributes.index(misspelled):
                print("typo_hash", error_line_str[error_column - 2])
                if error_line_str[error_column - 2] != '#':
                    print("forgotten hash")
                    typo_text = "The keyword " + misspelled + " is a hash value. Did you forget to put #?\n"
                else:
                    typo_text = "No idea what happened?\n"
                # might need to check other possibilities
        else:
            for hash in hash_attributes:
                if misspelled.lower().startswith(hash):
                    typo_text = misspelled + " looks like a hash value. Did you forget to put #?\n"
                    print("found it")
                    break
                else:
                    typo_text = "No keyword " + misspelled + ". Did you meant: " + res[0] + '?\n'
    elif misspelled == '':
        typo_text = ""
    else:
        typo_text = "No keyword " + misspelled + ". Did you meant: " + candidate_attr + '?\n'

    return typo_text
