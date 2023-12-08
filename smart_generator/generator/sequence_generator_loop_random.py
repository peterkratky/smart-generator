import numpy

from ..descriptor.enums import SequenceBehaviourTypeName
from .sequence_generator import SequenceGenerator


class SequenceGeneratorLoopRandom(SequenceGenerator):
    """
    Subclass of SequenceGenerator class for generating sequences with loop behaviour,
    where loop length is random.

    Attributes:
        iterations_min (int): Minimum number of iterations of the loop.
        iterations_max (int): Maximum number of iterations of the loop.
    """

    generator_type = f"SEQ.{SequenceBehaviourTypeName.SEQ_LOOP_RANDOM}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_parent: int,
        seed: int,
        iterations_min: int,
        iterations_max,
        propagate_templates: bool = True,
    ):
        """
        Constructor which extends the constructor :meth:`SequenceGenerator.__init__`
        of the parent class.

        Args:
            iterations_min (int): Minimum number of iterations of the loop.
            iterations_max (int): Maximum number of iterations of the loop.
        """
        super().__init__(id, name, seed_parent, seed, propagate_templates)
        self.iterations_min = iterations_min
        self.iterations_max = iterations_max

    def _generate_sequence(self, row, row_metadata):
        """
        Implements the abstract method :meth:`SequenceGenerator._generate_sequence`
        of the parent class to generate the sequence size.
        """
        self.size = numpy.random.randint(self.iterations_min, self.iterations_max)
