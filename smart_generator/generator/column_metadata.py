class ColumnMetadata:
    """
    Class representing metadata about a column in a table.

    Attributes:
        id (str): ID of the column.
        name (str): Name of the column.
        seed (int): Seed of the column.
        generator_type (str): Type of the column generator.
        visible (bool): Visibility of the column.
        template_filters (dict[str, list[int]]): Template filters of the column.
    """

    def __init__(
        self,
        id: str,
        name: str,
        seed: int,
        generator_type: str,
        visible: bool,
        template_filters,
    ):
        """
        Constructor of ColumnMetadata class.

        Args:
            id (str): ID of the column.
            name (str): Name of the column.
            seed (int): Seed of the column.
            generator_type (str): Type of the column generator.
            visible (bool): Visibility of the column.
            template_filters (dict[str, list[int]]): Template filters of the column.
        """
        self.id = id
        self.name = name
        self.seed = seed
        self.generator_type = generator_type
        self.visible = visible
        self.template_filters = template_filters
