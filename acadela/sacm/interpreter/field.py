from acadela.sacm.default_state import defaultAttrMap, CUSTOM_TYPE
from acadela.sacm import util

from acadela.sacm.case_object.attribute import Attribute
from acadela.sacm.case_object.derived_attribute import DerivedAttribute
from acadela.sacm.case_object.field import Field
from acadela.sacm.case_object.dynamic_field import DynamicField
from acadela.sacm.case_object.enumeration_option import EnumerationOption
from acadela.sacm.case_object.enumeration import Enumeration

import acadela.sacm.interpreter.directive as direc_intprtr

def interpret_field(field, fieldPath, taskType, formDirective):
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

    type = defaultAttrMap['type'] \
        if not hasattr(directive, "type") \
        else direc_intprtr\
                    .interpret_directive(directive.type)

    # If field type is custom, set the field path to custom path
    if type == CUSTOM_TYPE:
        fieldPath = field.path.value
        print("custom field path", fieldPath)

    readOnly = assign_form_directive_to_field('readOnly',
                                              directive,
                                              formDirective)

    mandatory = assign_form_directive_to_field('mandatory',
                                               directive,
                                               formDirective)

    position = interpret_position(directive)

    # For a field with custom path, do not create new attribute
    if type != CUSTOM_TYPE:
        fieldAsAttribute = Attribute(field.name, description,
                                     multiplicity=multiplicity,
                                     type=type)
        print("field as Attribute", vars(fieldAsAttribute))
    else:
        fieldAsAttribute = None

    # Construct TaskParam Object
    if taskType == 'DualTask':
        partValidCode = check_part_for_dual_task(\
            part, field.name)

        if partValidCode == 1:
            part = direc_intprtr.interpret_directive(part)

    fieldAsTaskParam = Field(field.name, description,
                             question,
                             multiplicity,
                             type,
                             fieldPath,
                             readOnly,
                             mandatory,
                             position, part)

    print("field as TaskParam", vars(fieldAsTaskParam))

    return {"fieldAsAttribute": fieldAsAttribute,
            "fieldAsTaskParam": fieldAsTaskParam}

def interpret_dynamic_field(field, fieldPath,
                            taskType, formDirective):

    directive = field.directive

    part = None if not hasattr(directive, "part")\
                else directive.part

    externalId = None \
        if field.externalId is None \
        else field.externalId.value

    extraDescription = None \
        if field.additionalDescription is None \
        else field.additionalDescription.value

    explicitAttrType = None \
        if not hasattr(directive, "explicitType") \
        else direc_intprtr \
        .interpret_directive(directive.explicitType)

    uiRefObj = util.getRefOfObject(field.uiRef)

    print("UIRef of ", field.name, "is", uiRefObj,
          'as type', util.cname(uiRefObj))

    uiRef = uiRefObj.value \
        if util.is_attribute_not_null(uiRefObj, "value") \
        else None

    # Construct Attribute Object of TaskParam (field)
    fieldAsAttribute = DerivedAttribute(field.name, field.description.value,
        extraDescription,
        field.expression.value,
        uiRef,
        externalId,
        explicitAttrType)

    if taskType == 'DualTask':
        check_part_for_dual_task(directive.part, field.name)

    position = interpret_position(directive)

    readOnly = assign_form_directive_to_field('readOnly',
                                              directive,
                                              formDirective)

    mandatory = assign_form_directive_to_field('mandatory',
                                              directive,
                                              formDirective)

    # if util.is_attribute_not_null(directive.readOnly):
    #     readOnly = direc_intprtr\
    #         .interpret_directive(directive.readOnly)
    # elif util.is_attribute_not_null(formDirective.readOnly):
    #     readOnly = direc_intprtr \
    #         .interpret_directive(formDirective.readOnly)

    # mandatory = defaultAttrMap['mandatory']
    #
    # if util.is_attribute_not_null(directive.mandatory):
    #     mandatory = direc_intprtr \
    #         .interpret_directive(directive.mandatory)
    # elif util.is_attribute_not_null(formDirective.mandatory):
    #     mandatory = direc_intprtr \
    #         .interpret_directive(formDirective.mandatory)

    dynamicField = DynamicField(field.name,
                                field.description.value,
                                directive.explicitType,
                                extraDescription,
                                field.expression.value,
                                field.uiRef,
                                externalId,
                                # Dynamic field properties
                                fieldPath,
                                readOnly,
                                mandatory,
                                position, part)

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
        else None

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
    if not any(operand in expression\
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

    dynamicField.expression = \
        'round({})'.format(' '.join(expressionElements))

    return dynamicField.expression

def sacm_compile(fieldList):
    taskParamList = []
    for field in fieldList:
        taskParam = {'$': {}}
        taskParamAttr = taskParam['$']

        util.compile_attributes(taskParamAttr, field,
                                ['path',
                                 'isReadOnly',
                                 'isMandatory',
                                 'position',
                                 'part'])

        taskParamList.append(taskParam)

    return taskParamList

def interpret_position(directiveObj):
    positionValue = defaultAttrMap['position'] \
        if not util.is_attribute_not_null(directiveObj, "position") \
        else direc_intprtr.interpret_directive(directiveObj.position)
    return str(positionValue).upper()
