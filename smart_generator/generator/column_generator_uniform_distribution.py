from datetime import datetime, timezone

from ..descriptor.enums import (ColumnBehaviourTypeName, DatePrecisionType,
                                DatetimePrecisionType, DescriptorTypeNames,
                                TimePrecisionType)
from ..helpers import datetime_precision
from .column_generator import ColumnGenerator


class ColumnGeneratorUniformDistributionInt(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type int with
    uniform distribution.

    Attributes:
        min (int): Minimum value of the column values.
        max (int): Maximum value of the column values.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        min: int,
        max: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            min (int): Minimum value of the column values.
            max (int): Maximum value of the column values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.min = min
        self.max = max

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate int values
        from uniform distribution.
        """
        return self.random_generator.integers(self.min, self.max, size)


class ColumnGeneratorUniformDistributionFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float with
    uniform distribution.

    Attributes:
        min (float): Minimum value of the column values.
        max (float): Maximum value of the column values.
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        min: float,
        max: float,
        precision: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            min (float): Minimum value of the column values.
            max (float): Maximum value of the column values.
            precision (int): Number of decimal places of the numeric values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.min = min
        self.max = max
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate float
        values from uniform distribution.
        """
        return (
            self.random_generator.uniform(self.min, self.max, size)
            .astype(float)
            .round(self.precision)
        )


class ColumnGeneratorUniformDistributionDatetime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type datetime
    with uniform distribution.

    Attributes:
        min (datetime): Minimum value of the column values.
        max (datetime): Maximum value of the column values.
        precision (DatetimePrecisionType): Precision of the datetime values.
    """

    generator_type = f"{DescriptorTypeNames.COL_DATETIME}.{ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        min: datetime,
        max: datetime,
        precision: DatetimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            min (datetime): Minimum value of the column values.
            max (datetime): Maximum value of the column values.
            precision (DatetimePrecisionType): Precision of the datetime values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.min = min
        self.max = max
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate datetime
        values from uniform distribution.
        """
        min_timestamp = self.min.replace(tzinfo=timezone.utc).timestamp() * 1000
        max_timestamp = self.max.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = self.random_generator.uniform(
            min_timestamp, max_timestamp, size
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.datetime_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps


class ColumnGeneratorUniformDistributionDate(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type date with
    uniform distribution.

    Attributes:
        min (datetime): Minimum value of the column values.
        max (datetime): Maximum value of the column values.
        precision (DatePrecisionType): Precision of the date values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_DATE}.{ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        min: datetime,
        max: datetime,
        precision: DatePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            min (datetime): Minimum value of the column values.
            max (datetime): Maximum value of the column values.
            precision (DatePrecisionType): Precision of the date values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.min = min
        self.max = max
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate date
        values from uniform distribution.
        """
        min_timestamp = self.min.replace(tzinfo=timezone.utc).timestamp() * 1000
        max_timestamp = self.max.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = self.random_generator.uniform(
            min_timestamp, max_timestamp, size
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.date_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to date values
        timestamps = timestamps.astype("datetime64[D]")

        return timestamps


class ColumnGeneratorUniformDistributionTime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type time with
    uniform distribution.

    Attributes:
        min (datetime): Minimum value of the column values.
        max (datetime): Maximum value of the column values.
        precision (TimePrecisionType): Precision of the time values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_TIME}.{ColumnBehaviourTypeName.UNIFORM_DISTRIBUTION}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        min: datetime,
        max: datetime,
        precision: TimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            min (datetime): Minimum value of the column values.
            max (datetime): Maximum value of the column values.
            precision (TimePrecisionType): Precision of the time values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.min = min
        self.max = max
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate time
        values from uniform distribution.
        """
        min_timestamp = self.min.replace(tzinfo=timezone.utc).timestamp() * 1000
        max_timestamp = self.max.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = self.random_generator.uniform(
            min_timestamp, max_timestamp, size
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to time values
        days = timestamps.astype("datetime64[D]")
        timestamps = (timestamps - days).astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps
