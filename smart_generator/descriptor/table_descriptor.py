from dataclasses import dataclass, field
from typing import List, Optional, Union

from marshmallow.validate import Equal

from .column import (ColumnDescriptorDate, ColumnDescriptorDatetime,
                     ColumnDescriptorFloat, ColumnDescriptorInteger,
                     ColumnDescriptorString, ColumnDescriptorTime)
from .sequence import Sequence


@dataclass
class TableDescriptor:
    """
    Class TableDescriptor is a dataclass that represents a table descriptor.
    It is a subclass of Descriptor.

    Attributes:
        name (str): Name of the table.
        descriptors (List[Union[
            ColumnDescriptorInteger,
            ColumnDescriptorFloat,
            ColumnDescriptorDatetime,
            ColumnDescriptorDate,
            ColumnDescriptorTime,
            ColumnDescriptorString,
            Sequence
        ]]): List of child descriptors - column or sequence descriptors. There must be
            maximum one sequence descriptor.
        id (str): Id of the table. Default None.
        seed (int): Seed of the table. Default 0.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
            Template filters for the table. These are used when generating from
            templates. Default None.
        common_dependencies (Optional[list[str]]): List of common dependencies when
            generating from templates. This can be used to specify dependencies which
            are common to all columns in a sequence (e.g. the common country for
            multiple columns with cities). Default None.
    """

    name: str

    descriptors: List[
        Union[
            ColumnDescriptorInteger,
            ColumnDescriptorFloat,
            ColumnDescriptorDatetime,
            ColumnDescriptorDate,
            ColumnDescriptorTime,
            ColumnDescriptorString,
            Sequence,
        ]
    ]

    id: str = None
    seed: int = 0

    template_filters: Optional[Union[dict[str, list[int]], dict[str, list[str]]]] = None

    common_dependencies: Optional[list[str]] = None

    descriptor_type: str = field(metadata={"validate": Equal("TABLE")}, default="TABLE")

    def get_descriptor_type(self):
        return self.descriptor_type
