from ..descriptor.enums import ColumnBehaviourTypeName, DescriptorTypeNames
from .column_generator import ColumnGenerator


class ColumnGeneratorNormalDistributionInt(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type int with
    normal distribution.

    Attributes:
        mean (float): Mean of the normal distribution.
        std_dev (float): Standard deviation of the normal distribution.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.NORMAL_DISTRIBUTION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        mean: float,
        std_dev: float,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            mean (float): Mean of the normal distribution.
            std_dev (float): Standard deviation of the normal distribution.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.mean = mean
        self.std_dev = std_dev

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate int values
        from normal distribution.
        """
        return self.random_generator.normal(self.mean, self.std_dev, size).astype(int)


class ColumnGeneratorNormalDistributionFloat(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator of type float with
    normal distribution.

    Attributes:
        mean (float): Mean of the normal distribution.
        std_dev (float): Standard deviation of the normal distribution.
        precision (int): Number of decimal places of the numeric values.
    """

    generator_type = (
        f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.NORMAL_DISTRIBUTION}"
    )

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        mean: float,
        std_dev: float,
        precision: int,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            mean (float): Mean of the normal distribution.
            std_dev (float): Standard deviation of the normal distribution.
            precision (int): Number of decimal places of the numeric values.
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.mean = mean
        self.std_dev = std_dev
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Overrides :meth:`ColumnGenerator._generate_column_values` to generate float
        values from normal distribution.
        """
        return (
            self.random_generator.normal(self.mean, self.std_dev, size)
            .astype(float)
            .round(self.precision)
        )
