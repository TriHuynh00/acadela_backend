from sacm.default_state import defaultAttrMap, CUSTOM_TYPE, DOCUMENT_LINK_TYPE
from sacm import util
from sacm.interpreter import util_intprtr

from sacm.case_object.attribute import Attribute
from sacm.case_object.derived_attribute import DerivedAttribute
from sacm.case_object.input_field import InputField
from sacm.case_object.output_field import OutputField
from sacm.case_object.enumeration_option import EnumerationOption
from sacm.case_object.enumeration import Enumeration
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import ui_ref_validator
from sacm.exception_handler.syntax_error_handler.string_pattern_validator import field_expression_validator


import sacm.interpreter.directive as direc_intprtr

def interpret_field(field, fieldPath, taskType, formDirective, model, treatment_str):
    directive = field.directive
    part = directive.part
    enumerationOptions = []
    question = None

    if field.question is not None:
        print("Field question len", len(field.question.optionList))
        description = field.question.text
        for option in field.question.optionList:
            additionalDescription = option.additionalDescription.value \
                if util.is_attribute_not_null(option, "additionalDescription") \
                else None

            externalId = option.externalId.value\
                if util.is_attribute_not_null(option, "externalId") \
                else None

            enumerationOptions.append(
                EnumerationOption(option.key,
                                  option.value,
                                  additionalDescription,
                                  externalId)
            )
        question = Enumeration(description, enumerationOptions)
        description = question

    elif field.description is not None:
        description = field.description.value

    multiplicity = defaultAttrMap['multiplicity'] \
        if not hasattr(directive, "multiplicity") \
        else direc_intprtr\
                .interpret_directive(directive.multiplicity)

    readOnly = assign_form_directive_to_field('readOnly',
                                              directive,
                                              formDirective)

    mandatory = assign_form_directive_to_field('mandatory',
                                               directive,
                                               formDirective)

    position = interpret_position(directive)

    uiRef = interpret_uiRef(field)

    externalId = field.externalId.value \
        if util.is_attribute_not_null(field, "externalId") \
        else None

    additionalDescription = field.additionalDescription.value \
        if util.is_attribute_not_null(field, "additionalDescription") \
        else None

    defaultValue = interpret_field_attr_value(field.defaultValue)

    print("Ref Object of default value", field.name, "is", defaultValue,
          'of type', util.cname(defaultValue))

    defaultValues = interpret_field_attr_value(field.defaultValues)

    # defaultValue = None \
    #     if field.defaultValue is None \
    #     else field.defaultValue.value
    #
    # defaultValues = None \
    #     if field.defaultValues is None \
    #     else field.defaultValues.value

    type = defaultAttrMap['type'] \
        if not util.is_attribute_not_null(directive, "type") \
        else direc_intprtr \
            .interpret_directive(directive.type)

    # If field type is custom, set the field path to custom path
    if type == CUSTOM_TYPE:
        fieldPath = util_intprtr.prefix_path_value(field.path.value, False)
        print("custom field path", fieldPath)
    else:
        # Parse document link
        if str(type).lower().startswith(DOCUMENT_LINK_TYPE):
            # Get the link URL but remove the )
            url = type.split('(')[1][:-1]

            # A link document is readOnly, notMandatory, of type string
            # uiRef = 'privatelink' and defaultValue = url
            readOnly = 'true'
            mandatory = 'false'
            type = 'string'
            uiRef = 'privatelink'
            defaultValue = str(url)

        elif str(type) == 'multiplechoice':
            type = 'enumeration'
            multiplicity = 'atLeastOne'


    # For a field with custom path, do not create new attribute
    if type != CUSTOM_TYPE:
        fieldAsAttribute = Attribute(field.name, description,
                                     multiplicity=multiplicity,
                                     type=type,
                                     uiReference=uiRef,
                                     externalId=externalId,
                                     additionalDescription=additionalDescription,
                                     defaultValues=defaultValues,
                                     defaultValue=defaultValue)
        print("field as Attribute", vars(fieldAsAttribute))
    else:
        fieldAsAttribute = None

    # Construct TaskParam Object
    if taskType == 'DualTask':
        partValidCode = check_part_for_dual_task(\
            part, field.name)

        if partValidCode == 1:
            part = direc_intprtr.interpret_directive(part)
    lineNumber = model._tx_parser.pos_to_linecol(field._tx_position)

    inputField = InputField(field.name, description,
                             question,
                             multiplicity,
                             type,
                             fieldPath,
                             readOnly,
                             mandatory,
                             position,
                             uiRef,
                             externalId,
                             part,
                             defaultValue,
                             defaultValues,
                             lineNumber)

    if util.is_attribute_not_null(inputField, "uiReference"):
        ui_ref_validator.validate_field_ui_ref(inputField, treatment_str)

    print("field as TaskParam", vars(inputField))

    return {"fieldAsAttribute": fieldAsAttribute,
            "fieldAsTaskParam": inputField}

def interpret_dynamic_field(field, fieldPath,
                            taskType, formDirective, model, treatment_str):

    directive = field.directive

    part = None if not hasattr(directive, "part")\
                else directive.part

    externalId = field.externalId.value \
        if util.is_attribute_not_null(field, "externalId") \
        else None

    extraDescription = field.additionalDescription.value \
        if util.is_attribute_not_null(field, "additionalDescription") \
        else None

    explicitAttrType = defaultAttrMap["type"] \
        if not util.is_attribute_not_null(directive, "explicitType") \
        else direc_intprtr \
        .interpret_directive(directive.explicitType)

    # uiRefObj = util.getRefOfObject(field.uiRef)
    #
    # print("UIRef of ", field.name, "is", uiRefObj,
    #       'as type', util.cname(uiRefObj))
    #
    # uiRef = uiRefObj.value \
    #     if util.is_attribute_not_null(uiRefObj, "value") \
    #     else None
    uiRef = interpret_uiRef(field)

    expression =str(field.expression.value) \
        if util.is_attribute_not_null(field.expression,"value")  \
        else None
    if expression is not None:
        expression = ' '.join(expression.split())

    print ("expression is", expression)

    # If field type is custom, set the field path to custom path
    if explicitAttrType == CUSTOM_TYPE:
        fieldPath = util_intprtr.prefix_path_value(field.path.value, False)
        print("custom field path of dynamic field", fieldPath)

    if taskType == 'DualTask':
        check_part_for_dual_task(directive.part, field.name)

    position = interpret_position(directive)

    readOnly = assign_form_directive_to_field('readOnly',
                                              directive,
                                              formDirective)

    mandatory = assign_form_directive_to_field('mandatory',
                                              directive,
                                              formDirective)

    # defaultValue = None \
    #     if field.defaultValue is None \
    #     else field.defaultValue.value

    defaultValue = interpret_field_attr_value(field.defaultValue)

    print("Ref Object of default value", field.name, "is", defaultValue,
          'of type', util.cname(defaultValue))

    defaultValues = interpret_field_attr_value(field.defaultValues)

    # defaultValues = None \
    #     if field.defaultValues is None \
    #     else field.defaultValues.value

    # Construct Attribute Object of TaskParam (field)
    fieldAsAttribute = DerivedAttribute(field.name,
                                        field.description.value,
                                        extraDescription,
                                        expression,
                                        uiRef,
                                        externalId,
                                        explicitAttrType)

    lineNumber = model._tx_parser.pos_to_linecol(field._tx_position)

    dynamicField = OutputField(field.name,
                                field.description.value,
                                explicitAttrType,
                                extraDescription,
                                expression,
                                uiRef,
                                externalId,
                                # Dynamic field properties
                                fieldPath,
                                position,
                                part,
                                readOnly,
                                mandatory,
                                defaultValue,
                                defaultValues,
                                lineNumber)

    if util.is_attribute_not_null(dynamicField, "uiReference"):
        ui_ref_validator.validate_field_ui_ref(dynamicField, treatment_str)

        # STRING PATTERN VALIDATIONS
        # 1. Validate the Dynamic Field expressions
    if util.is_attribute_not_null(dynamicField, "expression"):
        field_expression_validator.validate_field_expression(dynamicField, treatment_str)

    return {"fieldAsAttribute": fieldAsAttribute,
            "fieldAsTaskParam": dynamicField}

def assign_form_directive_to_field(directiveName,
                                   fieldDirective,
                                   formDirective):

    directiveVal = defaultAttrMap[directiveName]

    formDirectiveVal = getattr(formDirective, directiveName) \
        if util.is_attribute_not_null(formDirective, directiveName) \
        else None

    fieldDirectiveVal = getattr(fieldDirective, directiveName) \
        if util.is_attribute_not_null(fieldDirective, directiveName) \
        else defaultAttrMap[directiveName]

    if fieldDirectiveVal is not None:
        directiveVal = direc_intprtr \
            .interpret_directive(fieldDirectiveVal)
    elif formDirectiveVal is not None:
        directiveVal = direc_intprtr \
            .interpret_directive(formDirectiveVal)
    else:
        if hasattr(defaultAttrMap, directiveName):
            directiveVal = defaultAttrMap[directiveName]

    return directiveVal

# Check if the part value is human (#humanDuty) or auto (#systemDuty)
# Return -1 if part is neither #humanDuty or #systemDuty
#        0  if part is None
#        1  if part is valid
def check_part_for_dual_task(part, fieldId):

    if part is None:
        raise Exception('undefined part in field ' + fieldId)
        return 0

    elif part != '#humanDuty' and part != '#systemDuty':
        raise Exception('invalid part value {} in field {}. '
                        'Part value is \"#humanDuty\" or \"#systemDuty\"'
                        .format(part, fieldId))
        return -1

    return 1

# number should be rounded with round()
# string should be converted to number with number(string, 0)
def auto_convert_expression(dynamicField, fieldList):
    mathOperators = ['+', '-', '*', '/']

    expression = str(dynamicField.expression)

    # If there is no math operators in the uiReference,
    # it is something else and no need to convert them to number
    if dynamicField.explicitType in ["text", "string", "longtext", "json"] \
        or not any(operand in expression\
               for operand in mathOperators):
        return expression

    # If math operators is in uiReference, process it
    for operand in mathOperators:
        expression = expression.replace(operand, ' ' + operand + ' ') \

    expression = expression.replace('\n', ' ')

    expressionElements = expression.split(' ')

    # Loop from the end of string to remove redundant chars
    # along the way without affecting the array index order
    for i in range(len(expressionElements) - 1, -1, -1):
        element = expressionElements[i].strip()

        if element == '' or element == ' ':
            expressionElements.remove(element)

        for field in fieldList:
            fieldType = str(field.type)

            if element == field.id\
                and (fieldType == 'text'
                    or fieldType == 'enumeration'
                    or fieldType == 'longtext'
                    or fieldType == 'notype'):

                expressionElements[i] = 'number({}, 2)'.format(element)

    # dynamicField.expression = \
    #     'round({})'.format(' '.join(expressionElements))

    return dynamicField.expression

def sacm_compile(fieldList):
    taskParamList = []
    for field in fieldList:

        # Do not render hidden uiRef
        print("uiRef of field", field.id, 'is', field.uiReference)
        if field.uiReference == 'hidden':
            continue

        taskParam = {'$': {}}
        taskParamAttr = taskParam['$']

        util.compile_attributes(taskParamAttr, field,
                                ['path',
                                 'isReadOnly',
                                 'isMandatory',
                                 'position',
                                 'part',
                                 'lineNumber'])

        taskParamAttr['acadelaId'] = field.id
        fieldType = util.cname(field)
        if fieldType == "InputField":
            taskParamAttr['fieldType'] = "inputfield"
        elif fieldType == "OutputField":
                taskParamAttr['fieldType'] = "outputfield"

        taskParamList.append(taskParam)

    return taskParamList

def interpret_position(directiveObj):
    positionValue = defaultAttrMap['position'] \
        if not util.is_attribute_not_null(directiveObj, "position") \
        else direc_intprtr.interpret_directive(directiveObj.position)
    return str(positionValue).upper()

def interpret_uiRef(field):
    uiRefObj = util.getRefOfObject(field.uiRef)

    print("UIRef of ", field.name, "is", uiRefObj,
          'as type', util.cname(uiRefObj))

    uiRef = uiRefObj.value \
        if util.is_attribute_not_null(uiRefObj, "value") \
        else None

    return uiRef

def interpret_field_attr_value(fieldAttr):
    refObj = util.getRefOfObject(fieldAttr)

    refValue = refObj.value \
        if util.is_attribute_not_null(refObj, "value") \
        else None

    return refValue