import numpy
import pandas

from .table_generator import TableGenerator


class SequenceGenerator(TableGenerator):
    """
    Subclass of TableGenerator class for generating sequences. This class is meant to be
    used as a base class for all sequence generators.

    Attributes:
        sequence_values (numpy.ndarray): Values of the sequence.
        total_size (int): Total size of the sequence.
    """

    def __init__(
        self,
        id: str,
        name: str,
        seed_parent: int,
        seed: int,
        propagate_templates: bool = True,
    ):
        """
        Constructor which extends the constructor :meth:`SequenceGenerator.__init__`
        of the parent class.

        Args:
            id (str): Id of the generator.
            seed_parent (int): Seed of the parent generator.
        """
        super().__init__(id, name, seed, propagate_templates)
        self.sequence_values = None
        self.total_size = 0

    def _generate_sequence(self, row, row_metadata):
        """
        Abstract method for generating the sequence values.

        Args:
            row (pandas.Series): Row values from the above level.
            row_metadata (dict[str, ColumnMetadata]): Metadata of the row values
                (columns).
        """
        return None

    # TODO - clean up unused method
    def generate_sequence(self):
        """
        Generates the sequence values.
        """
        self._generate_sequence()
        self.size = len(self.sequence_values)
        if self.child_sequence_generator:
            self.child_sequence_generator.generate_sequence()
            self.total_size = self.child_sequence_generator.total_size * len(
                self.sequence_values
            )
        else:
            self.total_size = len(self.sequence_values)

    def generate_next_batch(
        self, max_size, row=None, row_metadata=None, preview: bool = False
    ):
        """
        Generates the next batch of sequence values. This method overrides the parent
        method. Ensures that the supplied row values are propagated to the generators
        of the sequence (e.g. country supplied from the above level is set to
        the relevant generators as a constant).

        Args:
            max_size (int): Maximum size of the batch.
            row (pandas.Series): Row values to propagate to the generators
                of the sequence.
            row_metadata (dict[str, ColumnMetadata]): Metadata of the row values
                (columns).
            preview (bool): Whether to generate preview or not.
        """
        self._generate_sequence(row, row_metadata)

        if self.propagate_templates:
            if row is not None and row_metadata is not None:
                for column in row:
                    if "TEMPLATE" in row_metadata[column].generator_type:
                        generator = self.get_generator_by_type(
                            row_metadata[column].generator_type,
                            row_metadata[column].seed + self.seed,
                        )
                        if generator:
                            generator.const_value = row[column].values[0]

        self._generate_next_batch(max_size, self.size, preview)
