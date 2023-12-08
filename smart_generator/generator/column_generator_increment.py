from datetime import datetime, timezone

import numpy

from ..descriptor.enums import (ColumnBehaviourTypeName, DatePrecisionType,
                                DatetimePrecisionType, DescriptorTypeNames,
                                TimePrecisionType)
from ..helpers import datetime_precision
from .column_generator import ColumnGenerator


class ColumnGeneratorIncrementInt(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type int with
    incremental generation.

    Attributes:
        start (int): Minimum value of the column values.
        step (int): Step of the incremental generation.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.INCREMENT}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        start: int,
        step: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            start (int): Minimum value of the column values.
            step (int): Step of the incremental generation.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.start = start
        self.step = step

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate int values
        in incremental manner.
        """
        return numpy.arange(
            self.start, self.start + (size * self.step), self.step, dtype=int
        )


class ColumnGeneratorIncrementFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float with
    incremental generation.

    Attributes:
        start (float): Minimum value of the column values.
        step (float): Step of the incremental generation.
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.INCREMENT}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        start: float,
        step: float,
        precision: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            start (float): Minimum value of the column values.
            step (float): Step of the incremental generation.
            precision (int): Number of decimal places of the numeric values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.start = start
        self.step = step
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate float
        values in incremental manner.
        """
        return numpy.arange(
            self.start, self.start + (size * self.step), self.step, dtype=float
        ).round(self.precision)


class ColumnGeneratorIncrementDatetime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type datetime
    with incremental generation.

    Attributes:
        start (datetime): Minimum value of the column values.
        step (int): Step of the incremental generation.
        precision (DatetimePrecisionType): Precision of the datetime values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_DATETIME}.{ColumnBehaviourTypeName.INCREMENT}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        start: datetime,
        step: int,
        precision: DatetimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__` of the parent class.

        Args:
            start (datetime): Minimum value of the column values.
            step (int): Step of the incremental generation.
            precision (DatetimePrecisionType): Precision of the datetime values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.start = start
        self.step = step
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate datetime values in incremental manner.
        """
        start_timestamp = self.start.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = numpy.arange(
            start_timestamp,
            start_timestamp + (size * self.step * 1000),
            self.step * 1000,
            dtype=numpy.int64,
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.datetime_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps


class ColumnGeneratorIncrementDate(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type date with incremental generation.

    Attributes:
        start (datetime): Minimum value of the column values.
        step (int): Step of the incremental generation.
        precision (DatePrecisionType): Precision of the date values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_DATE}.{ColumnBehaviourTypeName.INCREMENT}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        start: datetime,
        step: int,
        precision: DatePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__` of the parent class.

        Args:
            start (datetime): Minimum value of the column values.
            step (int): Step of the incremental generation.
            precision (DatePrecisionType): Precision of the date values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.start = start
        self.step = step
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate date values in incremental manner.
        """
        start_timestamp = self.start.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = numpy.arange(
            start_timestamp,
            start_timestamp + (size * self.step * 1000),
            self.step * 1000,
            dtype=numpy.int64,
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.date_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to date
        timestamps = timestamps.astype("datetime64[D]")

        return timestamps


class ColumnGeneratorIncrementTime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type time with incremental generation.

    Attributes:
        start (datetime): Minimum value of the column values.
        step (int): Step of the incremental generation.
        precision (TimePrecisionType): Precision of the time values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_TIME}.{ColumnBehaviourTypeName.INCREMENT}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        start: datetime,
        step: int,
        precision: TimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__` of the parent class.

        Args:
            start (datetime): Minimum value of the column values.
            step (int): Step of the incremental generation.
            precision (TimePrecisionType): Precision of the time values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.start = start
        self.step = step
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate time values in incremental manner.
        """
        start_timestamp = self.start.replace(tzinfo=timezone.utc).timestamp() * 1000

        timestamps = numpy.arange(
            start_timestamp,
            start_timestamp + (size * self.step * 1000),
            self.step * 1000,
            dtype=numpy.int64,
        ).astype("datetime64[ms]")

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to time
        days = timestamps.astype("datetime64[D]")
        timestamps = (timestamps - days).astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps
