from smart_generator.descriptor.column import ColumnDescriptor
from smart_generator.descriptor.enums import ColumnVisibilityType


def prepare_args_from_descriptor(descriptor: ColumnDescriptor):
    """
    Prepares the arguments for the generator from the descriptor.

    Args:
        descriptor (ColumnDescriptor): The descriptor of the column.

    Returns:
        dict: The arguments for the generator constructor.
    """
    args = {}

    # get the rest of the fields from the descriptor
    fields = descriptor.__dict__
    args = args | fields
    args.pop("descriptor_type", None)

    # rename seed to seed_column
    if "COL" in descriptor.get_descriptor_type():
        if "seed" in args:
            args["seed_column"] = args["seed"]
            args.pop("seed", None)

    if hasattr(descriptor, "visibility_type"):
        args["visible"] = (
            True
            if descriptor.visibility_type == ColumnVisibilityType.VISIBLE
            else False
        )
        args.pop("visibility_type", None)

    if hasattr(descriptor, "behaviour"):
        args = args | descriptor.behaviour.__dict__
        args.pop("behaviour_type", None)
        args.pop("behaviour", None)

    if "weights_table" in args:
        args["weights"] = {e.key: e.value for e in args["weights_table"]}
        args.pop("weights_table", None)

    if "descriptors" in args:
        args.pop("descriptors", None)

    if "template_filters" in args:
        args.pop("template_filters", None)

    if "common_dependencies" in args:
        args.pop("common_dependencies", None)

    if "template" in args:
        args["template_name"] = args["template"]
        args.pop("template", None)

    return args
