from dataclasses import dataclass, field
from typing import Optional, Union

from marshmallow.validate import Equal

from .behaviour import (ExponentialDistribution, Increment, NormalDistribution,
                        TemplateGeoLocation, TemplateLabel, TemplateTimeseries,
                        TemplateTimestamp, UniformDistribution, Unique,
                        WeightsTable)
from .descriptor import Descriptor
from .enums import (ColumnVisibilityType, DatePrecisionType,
                    DatetimePrecisionType, DescriptorTypeNames,
                    TimePrecisionType)


@dataclass
class ColumnDescriptor(Descriptor):
    """
    Class ColumnDescriptor is a dataclass that represents a column descriptor.
    It is a subclass of Descriptor.
    """

    def get_descriptor_type(self):
        return f"{self.descriptor_type}.{self.behaviour.get_type()}"


@dataclass
class ColumnDescriptorInteger(ColumnDescriptor):
    """
    Class ColumnDescriptorInteger is a dataclass that represents a column descriptor
    of type integer. It is a subclass of ColumnDescriptor.

    Attributes:
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[Increment, Unique, UniformDistribution, NormalDistribution,
            ExponentialDistribution, WeightsTable, TemplateLabel, TemplateTimeseries]):
            Behaviour of the column describing the data generation process.
            Default None.
    """

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_INTEGER)},
        default=DescriptorTypeNames.COL_INTEGER,
    )

    na_prob: float = 0

    behaviour: Optional[
        Union[
            Increment,
            Unique,
            UniformDistribution,
            NormalDistribution,
            ExponentialDistribution,
            WeightsTable,
            TemplateLabel,
            TemplateTimeseries,
        ]
    ] = None


@dataclass
class ColumnDescriptorFloat(ColumnDescriptor):
    """
    Class ColumnDescriptorFloat is a dataclass that represents a column descriptor
    of type float. It is a subclass of ColumnDescriptor.

    Attributes:
        precision (int): Number of decimal places of the numberic values.
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[Increment, Unique, UniformDistribution, NormalDistribution,
            ExponentialDistribution, WeightsTable, TemplateLabel, TemplateTimeseries]):
            Behaviour of the column describing the data generation process.
            Default None.
    """

    precision: int

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_FLOAT)},
        default=DescriptorTypeNames.COL_FLOAT,
    )

    na_prob: float = 0

    behaviour: Optional[
        Union[
            Increment,
            Unique,
            UniformDistribution,
            NormalDistribution,
            ExponentialDistribution,
            WeightsTable,
            TemplateLabel,
            TemplateTimeseries,
            TemplateGeoLocation,
        ]
    ] = None


@dataclass
class ColumnDescriptorDatetime(ColumnDescriptor):
    """
    Class ColumnDescriptorDatetime is a dataclass that represents a column descriptor
    of type datetime. It is a subclass of ColumnDescriptor.

    Attributes:
        precision (DatetimePrecisionType): Precision of the datetime values.
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[Increment, UniformDistribution, WeightsTable, TemplateLabel,
            TemplateTimestamp]): Behaviour of the column describing the data generation
            process. Default None.
    """

    precision: DatetimePrecisionType

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_DATETIME)},
        default=DescriptorTypeNames.COL_DATETIME,
    )

    na_prob: float = 0

    behaviour: Optional[
        Union[
            Increment,
            UniformDistribution,
            WeightsTable,
            TemplateLabel,
            TemplateTimestamp,
        ]
    ] = None


@dataclass
class ColumnDescriptorDate(ColumnDescriptor):
    """
    Class ColumnDescriptorDate is a dataclass that represents a column descriptor
    of type date. It is a subclass of ColumnDescriptor.

    Attributes:
        precision (DatePrecisionType): Precision of the date values.
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[Increment, UniformDistribution, WeightsTable, TemplateLabel,
            TemplateTimestamp]): Behaviour of the column describing the data generation
            process. Default None.
    """

    precision: DatePrecisionType

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_DATE)},
        default=DescriptorTypeNames.COL_DATE,
    )

    na_prob: float = 0

    behaviour: Optional[
        Union[
            Increment,
            UniformDistribution,
            WeightsTable,
            TemplateLabel,
            TemplateTimestamp,
        ]
    ] = None


@dataclass
class ColumnDescriptorTime(ColumnDescriptor):
    """
    Class ColumnDescriptorTime is a dataclass that represents a column descriptor
    of type time. It is a subclass of ColumnDescriptor.

    Attributes:
        precision (TimePrecisionType): Precision of the time values.
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[Increment, UniformDistribution, WeightsTable, TemplateLabel,
            TemplateTimestamp]): Behaviour of the column describing the data generation
            process. Default None.
    """

    precision: TimePrecisionType

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_TIME)},
        default=DescriptorTypeNames.COL_TIME,
    )

    na_prob: float = 0

    behaviour: Optional[
        Union[
            Increment,
            UniformDistribution,
            WeightsTable,
            TemplateLabel,
            TemplateTimestamp,
        ]
    ] = None


@dataclass
class ColumnDescriptorString(ColumnDescriptor):
    """
    Class ColumnDescriptorString is a dataclass that represents a column descriptor
    of type string. It is a subclass of ColumnDescriptor.

    Attributes:
        id (str): Id of the column. Default None.
        seed (int): Seed of the column. Default 1.
        visibility_type (ColumnVisibilityType): Visibility type of the column.
            Default VISIBLE.
        na_prob (float): Probability of NA values. Default 0.
        behaviour (Union[WeightsTable, TemplateLabel]): Behaviour of the column
            describing the data generation process. Default None.
    """

    id: str = None
    seed: int = 1
    visibility_type: ColumnVisibilityType = ColumnVisibilityType.VISIBLE

    descriptor_type: str = field(
        metadata={"validate": Equal(DescriptorTypeNames.COL_STRING)},
        default=DescriptorTypeNames.COL_STRING,
    )

    na_prob: float = 0

    behaviour: Optional[Union[WeightsTable, TemplateLabel]] = None
