import numpy


class ColumnGenerator:
    """
    Base class for all column generators.

    Attributes:
        id (str): Id of the column.
        name (str): Name of the column.
        seed (int): Seed for the generation process.
        random_generator (numpy.random.Generator): Random generator for the generation
            process.
        random_generator_na (numpy.random.Generator): Random generator for
            the generation process of NA values.
        visible (bool): Visibility of the column.
        na_prob (float): Probability of NA values.
        generated_values (numpy.ndarray): Values after the generation process.
        linked_internal_generators (dict): Dictionary of generators that are linked
            to this generator. Related to generation from templates. These are column
            generators (dependecies) which are used by this column generator
            within the same sequence (e.g. city uses city_id and country_id).
        template_filters (dict): Template filters for the column.
        temporal_filters (dict): Temporal filters for the column.
        dependent_generators_count (int): Number of dependent generators.
            Related to generation from templates.
        strong_dependencies (list): List of strong dependencies.
            Related to generation from templates.
        weak_dependencies (list): List of weak dependencies.
            Related to generation from templates.
        dependencies (list): List of all dependencies.
            Related to generation from templates.
        label_dependencies (list): List of label dependencies.
            Related to generation from templates.
        template_key (str): Template used for the generation.
            Related to generation from templates.
        const_value (str): Constant value in case of generation of constants.
    """

    dependencies = None

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
    ):
        """Constructor of the ColumnGenerator class.

        Args:
            id (str): Id of the column.
            name (str): Name of the column.
            seed_sequence (int): Seed for the generation process within a parent
                sequence.
            seed_column (int): Seed for the generation process of the column.
            visible (bool): Visibility of the column.
            na_prob (float): Probability of NA values.
        """
        self.id = id
        self.name = name
        self.seed = seed_sequence + seed_column
        self.random_generator = numpy.random.default_rng(seed=self.seed)
        self.random_generator_na = numpy.random.default_rng(seed=self.seed)
        self.visible = visible
        self.na_prob = na_prob
        self.generated_values = None
        self.const_value = None
        self.preview = False
        # The following attributes are related to generation from templates.
        # They are defined here as these attributes are checked in the factory
        # to create hierarchy of generators.
        self.linked_internal_generators = {}
        self.template_filters = None
        self.temporal_filters = None
        self.dependent_generators_count = 0
        self.strong_dependencies = None
        self.weak_dependencies = None
        self.dependencies = None
        self.label_dependencies = None
        self.template_key = None

    def _generate_column_values(self, size: int):
        """Abstract method for generating column values.

        Args:
            size (int): Number of generated values.
        """
        return None

    def _get_template_filters(self):
        """Getter of template filters."""
        return self.template_filters

    def generate_next_batch(self, size: int, preview: bool = False):
        """Generates next batch of values.

        Generates next batch of values and stores them in the generated_values
        attribute. If the column is a constant, the generated values are filled
        with the constant value. After the generation, the NA values are generated
        based on the na_prob attribute.

        Args:
            size (int): Number of generated values.
            preview (bool): If True, the generation is in preview mode.
        """
        self.preview = preview

        if self.const_value:
            self.generated_values = numpy.full(size, self.const_value)
        else:
            self.generated_values = self._generate_column_values(size)

        if self.na_prob and self.na_prob > 0:
            # na = numpy.full(size, numpy.nan)
            na = [None] * size
            na_mask = self.random_generator_na.choice(
                [True, False], size, p=[self.na_prob, 1 - self.na_prob]
            ).astype(int)
            self.generated_values = numpy.where(na_mask, na, self.generated_values)

    def get_generator_type(self):
        """Getter of the generator type."""
        return self.generator_type
