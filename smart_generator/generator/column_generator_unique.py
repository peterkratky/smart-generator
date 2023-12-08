import numpy

from ..descriptor.enums import ColumnBehaviourTypeName, DescriptorTypeNames
from .column_generator import ColumnGenerator


class ColumnGeneratorUniqueInt(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type int with
    unique values.

    Attributes:
        min (int): Minimum value of the column values.
        max (int): Maximum value of the column values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.UNIQUE}"
    )

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
        in unique manner.
        """
        values = numpy.arange(self.min, self.max, dtype=int)
        return self.random_generator.choice(values, size, replace=False)


class ColumnGeneratorUniqueFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float with
    unique values.

    Attributes:
        min (float): Minimum value of the column values.
        max (float): Maximum value of the column values.
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.UNIQUE}"

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
        values in unique manner.
        """
        values = numpy.arange(self.min, self.max, dtype=float)
        return self.random_generator.choice(values, size, replace=False).round(
            self.precision
        )
