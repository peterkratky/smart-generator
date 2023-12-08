from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from marshmallow.validate import Equal

from .behaviour import Loop, LoopRandom, TemplateSequence
from .column import (ColumnDescriptorDate, ColumnDescriptorDatetime,
                     ColumnDescriptorFloat, ColumnDescriptorInteger,
                     ColumnDescriptorString, ColumnDescriptorTime)
from .descriptor import Descriptor
from .enums import DescriptorTypeNames


@dataclass
class Sequence(Descriptor):
    """
    Class Sequence is a dataclass that represents a sequence descriptor.
    It is a subclass of Descriptor.

    Attributes:
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
        behaviour (Union[Loop, LoopRandom, TemplateSequence]): Behaviour
            of the sequence.
        id (str): Id of the table. Default None.
        seed (int): Seed of the table. Default 1.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
            Template filters for the table. These are used when generating from
            templates. Default None.
        common_dependencies (Optional[list[str]]): List of common dependencies when
            generating from templates. This can be used to specify dependencies
            which are common to all columns in a sequence (e.g. the common country
            for multiple columns with cities). Default None.
    """

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

    behaviour: Union[Loop, LoopRandom, TemplateSequence]

    id: str = None
    seed: int = 1

    template_filters: Optional[dict[str, list[int]]] = None

    common_dependencies: Optional[list[str]] = None

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.SEQUENCE)},
        default=DescriptorTypeNames.SEQUENCE,
    )

    def get_descriptor_type(self):
        return f"SEQ.{self.behaviour.get_type()}"
