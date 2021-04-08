from acadela.sacm import default_state

from acadela.sacm.case_object.attribute import Attribute
from acadela.sacm.case_object.derived_attribute import DerivedAttribute
from acadela.sacm.case_object.field import Field
from acadela.sacm.case_object.dynamic_field import DynamicField
from acadela.sacm.case_object.enumeration_option import EnumerationOption
from acadela.sacm.case_object.enumeration import Enumeration

import acadela.sacm.interpreter.directive as direc_intprtr

def interpret_field(field, fieldPath, taskType):
    directive = field.directive
    part = directive.part
    enumerationOptions = []
    question = None

    if field.question is not None:
        description = field.question.text
        for option in field.question.optionList:
            additionalDescription = \
                None if not hasattr(option, "additionalDescription") \
                    else option.additionalDescription

            externalId = \
                None if not hasattr(option, "externalId") \
                    else option.additionalDescription

            enumerationOptions.append(
                EnumerationOption(option.key, option.value,
                                  additionalDescription,
                                  externalId)
            )
        question = Enumeration(description, enumerationOptions)

    elif field.description is not None:
        description = field.description.value

    multiplicity = default_state.defaultAttrMap['multiplicity'] \
        if not hasattr(directive, "multiplicity") \
        else direc_intprtr\
                .interpret_directive(directive.multiplicity)

    type = default_state.defaultAttrMap['type'] \
        if not hasattr(directive, "type") \
        else direc_intprtr\
                    .interpret_directive(directive.type)

    mandatory = direc_intprtr.\
        interpret_directive(directive.mandatory)

    readOnly = direc_intprtr.\
        interpret_directive(directive.readOnly)

    position = default_state.defaultAttrMap['position']\
        if not hasattr(directive, 'position')\
        else direc_intprtr\
            .interpret_directive(directive.position)

    # Construct Attribute Object of TaskParam (field)
    fieldAsAttribute = Attribute(field.id, description,
                                 multiplicity = multiplicity,
                                 type = type)

    # Construct TaskParam Object
    if taskType == 'DualTask':
        partValidCode = check_part_for_dual_task(\
            part, field.id)

        if partValidCode == 1:
            part = direc_intprtr.interpret_directive(part)

    fieldAsTaskParam = Field(field.id, description,
         question, multiplicity, type,
         fieldPath, readOnly, mandatory, position, part)

    print("field as Attribute", vars(fieldAsAttribute))
    print("field as TaskParam", vars(fieldAsTaskParam))

    return {"fieldAsAttribute": fieldAsAttribute,
            "fieldAsTaskParam": fieldAsTaskParam}

def interpret_dynamic_field(field, fieldPath, taskType):
    directive = field.directive

    part = None if not hasattr(directive, "part")\
                else directive.part

    # Construct Attribute Object of TaskParam (field)
    fieldAsAttribute = DerivedAttribute(field.id, field.description,
        field.additionalDescription,
        field.expression,
        field.uiRef,
        field.externalId,
        directive.explicitType)

    if taskType == 'DualTask':
        check_part_for_dual_task(directive.part, field.id)

    position = None if directive.position is None\
               else directive.position



    dynamicField = DynamicField(field.id, field.description,
        directive.explicitType, field.additionalDescription,
        field.expression, field.uiRef, field.externalId,
        # Dynamic field properties
        fieldPath, directive.readOnly, directive.mandatory,
        position, part)

    return {"fieldAsAttribute": fieldAsAttribute,
            "fieldAsTaskParam": dynamicField}

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

    # print("\n\tField {}"
    #       "\n\t\tfieldTypes = {}"
    #       "\n\t\tDirectives "
    #       "\n\t\t\tmandatory = {}"
    #       "\n\t\t\treadOnly = {}"
    #       "\n\t\t\tposition = {}"
    #       "\n\t\t\tmultiplicity = {}"
    #       "\n\t\t\tpart = {}"
    #       "\n\t\t\ttype = {}"
    #       "\n\t\tdescription = {}"
    #       # "\n\t\townerPath = {}"
    #       # "\n\t\tdueDatePath = {}"
    #       # "\n\t\texternalId = {}"
    #       # "\n\t\tdynamicDescriptionPath = {}"
    #       .format(field.id,
    #               util.cname(field),
    #               directive.mandatory,
    #               directive.readOnly,
    #               "None" if directive.position is None else directive.position,
    #               "None" if not hasattr(directive, "multiplicity") else directive.multiplicity,
    #               "None" if directive.part is None else directive.part,
    #               directive.type,
    #               description))
    #               # (None if attrList.ownerPath is None else attrList.ownerPath.value),
    #               # dueDatePath,
    #               # ("None" if attrList.externalId is None else attrList.externalId.value),
    #               # ("None" if attrList.dynamicDescriptionPath is None else attrList.dynamicDescriptionPath.value)))
