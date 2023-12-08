from ..descriptor.enums import (ColumnBehaviourTypeName, DescriptorTypeNames,
                                TemplateType)


def template_from_column_type(column_type):
    """
    Returns the template name from a column type.

    Args:
        column_type (str): The column type.

    Returns:
        str: The template name.
    """
    return column_type.split(".")[3].lower()


def template_filter_from_column_type(column_type):
    """
    Returns the template filter from a column type.

    Args:
        column_type (str): The column type.

    Returns:
        str: The template filter.
    """
    return f"{template_from_column_type(column_type)}".lower()


def id_column_type_from_template(template):
    """
    Returns column type from a template, specifically ID part.

    Args:
        template (str): The template name.

    Returns:
        str: The column type.
    """
    return f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.TEMPLATE_LABEL}.{TemplateType.ID}.{template.upper()}"


def label_column_type_from_template(template):
    """
    Returns column type from a template, specifically LABEL part.

    Args:
        template (str): The template name.

    Returns:
        str: The column type.
    """
    return f"{DescriptorTypeNames.COL_STRING}.{ColumnBehaviourTypeName.TEMPLATE_LABEL}.{TemplateType.LABEL}.{template.upper()}"
