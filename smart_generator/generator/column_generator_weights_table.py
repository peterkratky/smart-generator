from datetime import datetime

import numpy

from ..descriptor.enums import (ColumnBehaviourTypeName, DatePrecisionType,
                                DatetimePrecisionType, DescriptorTypeNames,
                                TimePrecisionType)
from ..helpers import datetime_precision
from .column_generator import ColumnGenerator


class ColumnGeneratorWeightsTableInt(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type int
    generating values from a weights table.

    Attributes:
        weights (dict[int, float]): Weights table of the column values in the form
            of dictionary (value, weight).
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[int, float],
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[int, float]): Weights table of the column values in the form
                of dictionary (value, weight).
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate int values
        from a weights table.
        """
        keys = list(self.weights.keys())
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        return self.random_generator.choice(keys, size, p=probabilities).astype(int)


class ColumnGeneratorWeightsTableFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float
    generating values from a weights table.

    Attributes:
        weights (dict[float, float]): Weights table of the column values in the form
            of dictionary (value, weight).
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[float, float],
        precision: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[float, float]): Weights table of the column values in the
                form of dictionary (value, weight).
            precision (int): Number of decimal places of the numeric values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate float
        values from a weights table.
        """
        keys = numpy.array(list(self.weights.keys())).round(self.precision)
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        return self.random_generator.choice(keys, size, p=probabilities)


class ColumnGeneratorWeightsTableString(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type string
    generating values from a weights table.

    Attributes:
        weights (dict[str, float]): Weights table of the column values in the form
            of dictionary (value, weight).
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_STRING}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[str, float],
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[str, float]): Weights table of the column values in the form
                of dictionary (value, weight).
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate string
        values from a weights table.
        """
        keys = list(self.weights.keys())
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        return self.random_generator.choice(keys, size, p=probabilities)


class ColumnGeneratorWeightsTableDatetime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type datetime
    generating values from a weights table.

    Attributes:
        weights (dict[datetime, float]): Weights table of the column values in the form
            of dictionary (value, weight).
        precision (DatetimePrecisionType): Precision of the datetime values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_DATETIME}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[datetime, float],
        precision: DatetimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[datetime, float]): Weights table of the column values in
                the form of dictionary (value, weight).
            precision (DatetimePrecisionType): Precision of the datetime values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate datetime
        values from a weights table.
        """
        keys = numpy.array(list(self.weights.keys())).astype(
            f"datetime64[{datetime_precision.datetime_precision_to_numpy_label(self.precision)}]"
        )
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        timestamps = self.random_generator.choice(keys, size, p=probabilities)

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.datetime_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps


class ColumnGeneratorWeightsTableDate(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type date
    generating values from a weights table.

    Attributes:
        weights (dict[datetime, float]): Weights table of the column values in the form
            of dictionary (value, weight).
        precision (DatePrecisionType): Precision of the date values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_DATE}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[datetime, float],
        precision: DatePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[datetime, float]): Weights table of the column values in
                the form of dictionary (value, weight).
            precision (DatePrecisionType): Precision of the date values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate date
        values from a weights table.
        """
        keys = numpy.array(list(self.weights.keys())).astype(
            f"datetime64[{datetime_precision.date_precision_to_numpy_label(self.precision)}]"
        )
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        timestamps = self.random_generator.choice(keys, size, p=probabilities)

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.date_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to date values
        timestamps = timestamps.astype("datetime64[D]")

        return timestamps


class ColumnGeneratorWeightsTableTime(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type time
    generating values from a weights table.

    Attributes:
        weights (dict[datetime, float]): Weights table of the column values in the form
            of dictionary (value, weight).
        precision (TimePrecisionType): Precision of the time values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_TIME}.{ColumnBehaviourTypeName.WEIGHTS_TABLE}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        weights: dict[datetime, float],
        precision: TimePrecisionType,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            weights (dict[datetime, float]): Weights table of the column values in
                the form of dictionary (value, weight).
            precision (TimePrecisionType): Precision of the time values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.weights = weights
        self.precision = precision

    def _generate_column_values(self, size: int):
        keys = numpy.array(list(self.weights.keys())).astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )
        weights = list(self.weights.values())
        probabilities = numpy.array(weights) / sum(weights)
        timestamps = self.random_generator.choice(keys, size, p=probabilities)

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
