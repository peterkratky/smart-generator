from dataclasses import field
from datetime import datetime
from typing import Optional, Union

from marshmallow.validate import Equal
from marshmallow_dataclass import dataclass

from .enums import (ColumnBehaviourTypeName, GeoCoordinateType,
                    SequenceBehaviourTypeName)


@dataclass
class Behaviour:
    """
    Class Behaviour is a dataclass that represents a behaviour for the data generation
    process.
    """

    def get_type(self):
        return self.behaviour_type


@dataclass
class Increment(Behaviour):
    """
    Class Increment is a dataclass that represents column generation behaviour
    of incremental values.

    Attributes:
        start (Union[float, int, datetime]): Start value of the range.
        step (Union[float, int]): Step value of the range.
    """

    start: Union[float, int, datetime]
    step: Union[float, int]

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.INCREMENT)},
        default=ColumnBehaviourTypeName.INCREMENT,
    )


@dataclass
class Unique(Behaviour):
    """
    Class Unique is a dataclass that represents column generation behaviour of unique
    values.

    Attributes:
        min (int): Minimum value of the range.
        max (int): Maximum value of the range.
    """

    min: int
    max: int

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.UNIQUE)},
        default=ColumnBehaviourTypeName.UNIQUE,
    )


@dataclass
class UniformDistribution(Behaviour):
    """
    Class UniformDistribution is a dataclass that represents column generation behaviour
    of values from a uniform distribution.

    Attributes:
        min (Union[float, int, datetime]): Minimum value of the distribution.
        max (Union[float, int, datetime]): Maximum value of the distribution.
    """

    min: Union[float, int, datetime]
    max: Union[float, int, datetime]

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION)},
        default=ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION,
    )


@dataclass
class NormalDistribution(Behaviour):
    """
    Class NormalDistribution is a dataclass that represents column generation behaviour
    of values from a normal distribution.

    Attributes:
        mean (Union[float, int, datetime]): Mean value of the distribution.
        std_dev (Union[float, int]): Standard deviation of the distribution.
    """

    mean: Union[int, float, datetime]
    std_dev: Union[int, float]

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.NORMAL_DISTRIBUTION)},
        default=ColumnBehaviourTypeName.NORMAL_DISTRIBUTION,
    )


@dataclass
class ExponentialDistribution(Behaviour):
    """
    Class ExponentialDistribution is a dataclass that represents column generation
    behaviour of values from an exponential distribution.

    Attributes:
        scale (Union[float, int]): Scale value of the distribution.
    """

    scale: Union[int, float]

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.EXPONENTIAL_DISTRIBUTION)},
        default=ColumnBehaviourTypeName.EXPONENTIAL_DISTRIBUTION,
    )


@dataclass
class WeightsTable(Behaviour):
    """
    Class WeightsTable is a dataclass that represents column generation behaviour
    of values from a weights table.

    Attributes:
        weights_table (list[Entry]): List of entries of the weights table.
            An entry is represented as an object {"key": <key>, "value": <value>}
    """

    @dataclass
    class Entry:
        key: Union[float, int, datetime, str]
        value: float

    weights_table: list[Entry]

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.WEIGHTS_TABLE)},
        default=ColumnBehaviourTypeName.WEIGHTS_TABLE,
    )

    @property
    def weights(self):
        return {e.key: e.value for e in self.weights_table}


@dataclass
class TemplateLabel(Behaviour):
    """
    Class TemplateLabel is a dataclass that represents column generation behaviour
    of values from a template of labels.

    Attributes:
        template (str): Name of the template of labels.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
            Template filters applied to the template. Default None.
    """

    template: str

    template_filters: Optional[Union[dict[str, list[int]], dict[str, list[str]]]] = None

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.TEMPLATE_LABEL)},
        default=ColumnBehaviourTypeName.TEMPLATE_LABEL,
    )

    def get_type(self):
        return f"{self.behaviour_type}.LABEL"


@dataclass
class TemplateGeoLocation(Behaviour):
    """
    Class TemplateGeoLocation is a dataclass that represents column generation behaviour
    of values from a template of geolocations.

    Attributes:
        template (str): Name of the template of geolocations.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
            Template filters applied to the template. Default None.
    """

    template: str
    coordinate_type: GeoCoordinateType

    template_filters: Optional[Union[dict[str, list[int]], dict[str, list[str]]]] = None

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.TEMPLATE_GEOLOCATION)},
        default=ColumnBehaviourTypeName.TEMPLATE_GEOLOCATION,
    )

    def get_type(self):
        return f"{self.behaviour_type}.GEOLOCATION"


@dataclass
class TemplateTimestamp(Behaviour):
    """
    Class TemplateTimestamp is a dataclass that represents column generation behaviour
    of values from a template of timestamps.

    Attributes:
        template (str): Name of the template of timestamps.
        start (datetime): Start value of the range.
        end (datetime): End value of the range.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
        Template filters applied to the template. Default None.
    """

    template: str

    start: datetime
    end: datetime
    template_filters: Optional[Union[dict[str, list[int]], dict[str, list[str]]]] = None

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.TEMPLATE_TIMESTAMP)},
        default=ColumnBehaviourTypeName.TEMPLATE_TIMESTAMP,
    )

    def get_type(self):
        return f"{self.behaviour_type}.TIMESTAMP"


@dataclass
class TemplateTimeseries(Behaviour):
    """
    Class TemplateTimeseries is a dataclass that represents column generation behaviour
    of values from a template of timeseries.

    Attributes:
        template (str): Name of the template of timeseries.
        template_filters (Optional[Union[dict[str, list[int]], dict[str, list[str]]]]):
        Template filters applied to the template. Default None.
    """

    template: str

    template_filters: Optional[Union[dict[str, list[int]], dict[str, list[str]]]] = None

    behaviour_type: str = field(
        metadata={"validate": Equal(ColumnBehaviourTypeName.TEMPLATE_TIMESERIES)},
        default=ColumnBehaviourTypeName.TEMPLATE_TIMESERIES,
    )

    def get_type(self):
        return f"{self.behaviour_type}.TIMESERIES"


@dataclass
class Loop(Behaviour):
    """
    Class Loop is a dataclass that represents sequence generation behaviour of a loop.

    Attributes:
        iterations (int): Number of iterations of the loop.
    """

    iterations: int

    behaviour_type: str = field(
        metadata={"validate": Equal(SequenceBehaviourTypeName.SEQ_LOOP)},
        default=SequenceBehaviourTypeName.SEQ_LOOP,
    )


@dataclass
class LoopRandom(Behaviour):
    """
    Class LoopRandom is a dataclass that represents sequence generation behaviour
    of a random loop.

    Attributes:
        iterations_min (int): Minimum number of iterations of the loop.
        iterations_max (int): Maximum number of iterations of the loop.
    """

    iterations_min: int
    iterations_max: int

    behaviour_type: str = field(
        metadata={"validate": Equal(SequenceBehaviourTypeName.SEQ_LOOP_RANDOM)},
        default=SequenceBehaviourTypeName.SEQ_LOOP_RANDOM,
    )


@dataclass
class TemplateSequence(Behaviour):
    """
    Class TemplateSequence is a dataclass that represents sequence generation behaviour
    based on a sequence template.

    Attributes:
        template (str): Name of the sequence template.
    """

    template: str

    behaviour_type: str = field(
        metadata={"validate": Equal(SequenceBehaviourTypeName.SEQ_TEMPLATE_SEQUENCE)},
        default=SequenceBehaviourTypeName.SEQ_TEMPLATE_SEQUENCE,
    )
