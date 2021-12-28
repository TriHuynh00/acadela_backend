from sacm.exception_handler.semantic_error_handler import id_uniqueness_checker
from sacm.exception_handler.semantic_error_handler import path_validity_checker
from sacm.exception_handler.semantic_error_handler.url_validation import url_validator
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import field_expression_validator
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import ui_ref_validator
class SemanticErrorHandler():
    def handle_semantic_errors (case_object_tree, treatment_str):
        # STRING PATTERN VALIDATIONS
        # 1. Validate the Dynamic Field expressions 
        field_expression_validator.validate_field_expressions(case_object_tree, treatment_str)
        # 2. Validate the UI References  
        ui_ref_validator.validate_ui_ref(case_object_tree, treatment_str)
        
        # TRUSTED URL VALIDATION 
        url_validator.url_validator(case_object_tree)
        # ID UNIQUENESS VALIDATION --> Check if all entities have unique ids
        id_uniqueness_checker.check_id_uniqueness(case_object_tree)
        
        # PATH VALIDATION-> Check Field with custom path is pointed to a valid source
        #                   Need to prefix the path afterward (using
        #                   prefix_path_value() function in interpreter/util_intprtr
        path_validity_checker.check_path_validity(case_object_tree, treatment_str)
