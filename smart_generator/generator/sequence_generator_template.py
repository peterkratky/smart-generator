from ..descriptor.enums import SequenceBehaviourTypeName
from ..templates.enums import TemplateTableMode
from ..templates.templates_provider import TemplatesProvider
from .sequence_generator import SequenceGenerator


class SequenceGeneratorTemplate(SequenceGenerator):
    """
    Subclass of SequenceGenerator class for generating sequences based on a template.

    Attributes:
        provider (TemplatesProvider): Provider of the templates.
        template_name (str): Name of the template.
        template_filters (dict[str, list[int]]): Filters for the template.
        common_dependencies (list[str]): Common dependency keys for the template.
        strong_dependencies (list[str]): List of strong dependencies.
        weak_dependencies (list[str]): List of weak dependencies.
        dependencies (list[str]): List of all dependencies.
    """

    generator_type = f"SEQ.{SequenceBehaviourTypeName.SEQ_TEMPLATE_SEQUENCE}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_parent: int,
        seed: int,
        templates_provider: TemplatesProvider,
        template_name: str,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
        propagate_templates: bool = True,
    ):
        """
        Constructor which extends the constructor :meth:`SequenceGenerator.__init__`
        of the parent class.

        Args:
            provider (TemplatesProvider): Provider of the templates.
            template_name (str): Name of the template.
            template_filters (dict[str, list[int]]): Filters for the template.
            common_dependencies (list[str]): Common dependency keys for the template.
        """
        super().__init__(id, name, seed_parent, seed, propagate_templates)
        self.provider = templates_provider
        self.template_name = template_name
        self.template_filters = template_filters
        self.common_dependencies = common_dependencies

        if self.provider:
            self.strong_dependencies = self.provider.get_strong_dependencies(
                self.template_name
            )
            self.weak_dependencies = self.provider.get_weak_dependencies(
                self.template_name
            )
            self.dependencies = list(
                set(self.strong_dependencies + self.weak_dependencies)
            )

    def _generate_sequence(self, row, row_metadata):
        """
        Implements the abstract method :meth:`SequenceGenerator._generate_sequence`
        of the parent class to generate the sequence size.
        The size of the sequence is determined based on the template.
        """
        self.size = None

        # TODO refactor
        stats_table = self.provider.get_table_stats(
            self.template_name, TemplateTableMode.ID
        )
        table_key = self.provider.get_table_key(self.template_name)
        # The sequence has a dependency column at the above level which contains ids
        # of sequences in the template. Therefore this needs to be propagated using
        # the row from the above level. Then, the size of the sequence is loaded from
        # the template based on the id of the sequence in the template.
        # For example, a route template contains sequences of gps points and a route id.
        # The route id is propagated to the sequence generator and the size
        # of the sequence is loaded from the route template as count of the points.
        # Imagine a sequence with id 42 and 1000 points, then the size of the sequence
        # is 1000.
        if row is not None:
            for column in row:
                column_name = row_metadata[column].name
                if table_key in column_name.lower():
                    self.size = stats_table[
                        stats_table["value"] == row[column].values[0]
                    ]["stat"].values[0]

        if not self.size:
            self.size = 100
