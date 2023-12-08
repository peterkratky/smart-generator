from ..descriptor.enums import ColumnBehaviourTypeName, DescriptorTypeNames
from .column_generator import ColumnGenerator


class ColumnGeneratorExponentialDistributionInt(ColumnGenerator):
    """A subclass of ColumnGenerator which represents a column generator of type int
    with exponential distribution.

    Attributes:
        scale (float): Scale of the exponential distribution.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.EXPONENTIAL_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        scale: float,
    ):
        """Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            scale (float): Scale of the exponential distribution.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.scale = scale

    def _generate_column_values(self, size: int):
        """Overrides :meth:`ColumnGenerator._generate_column_values` to generate int
        values from exponential distribution."""
        return self.random_generator.exponential(self.scale, size).astype(int)


class ColumnGeneratorExponentialDistributionFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float
    with exponential distribution.

    Attributes:
        scale (float): Scale of the exponential distribution.
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.EXPONENTIAL_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        scale: float,
        precision: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            scale (float): Scale of the exponential distribution.
            precision (int): Number of decimal places of the numeric values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.scale = scale
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate float
        values from exponential distribution.
        """
        return (
            self.random_generator.exponential(self.scale, size)
            .astype(float)
            .round(self.precision)
        )
