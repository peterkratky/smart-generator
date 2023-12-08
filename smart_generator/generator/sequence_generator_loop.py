from ..descriptor.enums import SequenceBehaviourTypeName
from .sequence_generator import SequenceGenerator


class SequenceGeneratorLoop(SequenceGenerator):
    """
    Subclass of SequenceGenerator class for generating sequences with loop behaviour,
    where loop length is fixed.

    Attributes:
        iterations (int): Number of iterations of the loop.
    """

    generator_type = f"SEQ.{SequenceBehaviourTypeName.SEQ_LOOP}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_parent: int,
        seed: int,
        iterations: int,
        propagate_templates: bool = True,
    ):
        """
        Constructor which extends the constructor :meth:`SequenceGenerator.__init__`
        of the parent class.

        Args:
            iterations (int): Number of iterations of the loop.
        """
        super().__init__(id, name, seed_parent, seed, propagate_templates)
        self.iterations = iterations

    def _generate_sequence(self, row, row_metadata):
        """
        Implements the abstract method :meth:`SequenceGenerator._generate_sequence`
        of the parent class to generate the sequence size.
        """
        self.size = self.iterations
