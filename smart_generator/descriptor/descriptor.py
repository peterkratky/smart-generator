from dataclasses import dataclass


@dataclass
class Descriptor:
    """
    Class Descriptor is a base class for all descriptors. It is a dataclass.

    Attributes:
        name (str): Name of the descriptor.
    """

    name: str

    def get_descriptor_type(self):
        return self.descriptor_type
