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
    error_column = error.col
    print("Line with error:", error_line_str, error_line_str[error_column - 1:])
    misspelled = error_line_str[error_column - 1:len(error_line_str)]
    misspelled = re.split('[\W|\d]+', misspelled)[0]
    print("Misspelled word:", misspelled)
    
    res = [ele for ele in attribute_list if (ele.lower() in misspelled.lower())]
    res_lower = [x.lower() for x in res]
    hash_lower = [x.lower() for x in hash_attributes]
    print("Attributes included in misspelled:", res)

    # check for most likely correction
    candidate_attr = spell.correction(misspelled)
    print("SUGGESTION from spell checker:", candidate_attr)
    if candidate_attr.lower() == misspelled.lower():
        if len(res) == 0:
            typo_text = f"Unrecognized keyword: {misspelled}\n"
        elif misspelled.lower() in hash_attributes:
            # check for hash
            if hash_lower.index(misspelled.lower()):
                print("typo_hash", error_line_str[error_column - 2])
                if error_line_str[error_column - 2] != '#':
                    print("forgotten hash")
                    typo_text = f"The keyword {misspelled} is a directive value. Did you mean #{misspelled}?\n"
                else:
                    typo_text = ""
                # might need to check other possibilities
        elif misspelled.lower() in res_lower:
            typo_text = f"Unexpected keyword: {misspelled} \n"
            
        else:
            for hash in hash_attributes:
                if misspelled.lower().startswith(hash):
                    typo_text = f"{misspelled} looks like a directive value. Did you mean #{misspelled}?\n"
                    break
                else:
                    typo_text = f"No keyword {misspelled}. Did you mean: {res[0]}?\n"
    elif misspelled == '':
        typo_text = ""
    else:
        typo_text = f"No keyword {misspelled}. Did you mean: {candidate_attr}?\n"
    return typo_text
