import json
import logging

import numpy

from ..helpers.columns_combinations import (rows_from_columns,
                                            unique_combinations_from_columns)
from ..helpers.merging_filters import filters_conjunction
from ..helpers.template_column_naming import template_filter_from_column_type
from ..templates.enums import TemplateTableMode
from ..templates.templates_provider import TemplatesProvider
from .column_generator import ColumnGenerator


class ColumnGeneratorTemplate(ColumnGenerator):
    """
    A subclass of ColumnGenerator which represents a column generator using templates
    to generate values. This is an abstract class meant to be used as a base class for
    all column generators using templates.

    Attributes:
        provider (TemplatesProvider): Provider of the templates.
        template_name (str): Name of the template.
        template_filters (dict[str, list[int]]): Filters to apply to the template.
        common_dependencies (list[str]): List of common dependencies when generating
            from templates. This can be used to specify dependencies which are common
            to all columns in a sequence (e.g. the common country for multiple columns
            with cities).
        randomize (bool): Whether to randomize the generated values or not.
            Default True, but template settings can override this. If false, the order
            of values from the template will be kept as is. This can be useful when
            generating a sequence from the templates (e.g. gps route).
    """

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        templates_provider: TemplatesProvider,
        template_name: str,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGenerator.__init__`
        of the parent class.

        Args:
            templates_provider (TemplatesProvider): Provider of the templates.
            template_name (str): Name of the template.
            template_filters (dict[str, list[int]]): Filters to apply to the template.
            common_dependencies (list[str]): List of common dependencies when generating
                from templates. This can be used to specify keys which are common to all
                columns in a sequence (e.g. the common country for multiple columns
                with cities).
        """
        super().__init__(id, name, seed_sequence, seed_column, visible, na_prob)
        self.provider = templates_provider
        self.template_name = template_name
        self.template_filters = template_filters
        self.common_dependencies = common_dependencies
        self.randomize = True

        if self.provider:
            self.strong_dependencies = self.provider.get_strong_dependencies(
                self.template_name,
                [*self.template_filters] if self.template_filters else None,
                [*self.common_dependencies] if self.common_dependencies else None,
            )
            self.weak_dependencies = self.provider.get_weak_dependencies(
                self.template_name
            )
            self.dependencies = list(
                set(self.strong_dependencies + self.weak_dependencies)
            )
            self.template_key = self.provider.get_table_key(self.template_name)
            self.randomize = self.provider.get_table(self.template_name).randomize
            self.label_dependencies = self.provider.get_label_dependencies(
                self.template_name
            )

    def _get_effective_dependencies(self):
        """
        Returns effective dependencies and translates them to generator objects. These
        are dependecy generators which are linked to the current generator.

        Returns:
            list[str]: List of effective dependencies.
        """
        return [d for d in self.dependencies if d in self.linked_internal_generators]

    def _get_dependency_column_values(self):
        """
        Returns generated values of the dependency columns. This is list of lists and
        the order of the values is the same as the order of the dependencies.

        Returns:
            list[list]: List of lists of generated values of the dependency columns.
        """
        return [
            self.linked_internal_generators[d].generated_values
            for d in self._get_effective_dependencies()
        ]

    def _load_weights_table_from_template(
        self,
        mode: TemplateTableMode = TemplateTableMode.DEFAULT,
        template_filters: dict[str, list[int]] = None,
        preview: bool = False,
    ):
        """
        Loads the weights table from the template. These are two lists of the same size.
        The first list contains the labels and the second list contains the weights.

        In case there is no weights table for the given filters, the method returns two
        lists: [None], [1].

        Args:
            mode (TemplateTableMode): Mode of the table determining which columns will
                be loaded. Defaults to TemplateTableKey.DEFAULT.
            template_filters (dict[str, list[int]]): Filters to apply to the template.
            preview (bool): Whether to load the preview or not.

        Returns:
            tuple[list, list]: Tuple of lists of the same size. The first list contains
                the labels and the second list contains the weights.
        """
        table = self.provider.get_table_labels_weights(
            template_name=self.template_name,
            mode=mode,
            template_filters=template_filters,
            preview=preview,
        )
        if table.size > 0:
            labels = table["value"]
            weights = table["weight"].to_numpy(dtype="float64")
            weights = weights / numpy.sum(weights)
        else:
            logging.warning(
                f"No {self.template_name} found for filters: {json.dumps(template_filters)}"
            )
            labels = [None]
            weights = [1]

        return labels, weights

    def _generate_from_template(
        self, size: int, key: TemplateTableMode = TemplateTableMode.DEFAULT
    ):
        """
        Generates values from the template.

        This method ensures that the generated values are consistent with
        the dependencies. For example, if the template is a list of cities and
        the dependencies are countries, the generated values will be cities from
        the given countries.

        This method is used when there is at least one dependency (e.g. country has
        dependency on country id).

        Args:
            size (int): Number of generated values.
            key (TemplateTableMode): Key type of the table to load.
            Default TemplateTableKey.DEFAULT.

        Returns:
            list: List of generated values.
        """
        dependency_cols = self._get_dependency_column_values()
        combinations = unique_combinations_from_columns(dependency_cols)
        dependency_rows = rows_from_columns(dependency_cols)

        values = [None] * size
        for i in range(len(combinations)):
            filters = {}

            combination = combinations[i]
            if None not in combination:
                for j in range(len(dependency_cols)):
                    d = self._get_effective_dependencies()[j]
                    filters[template_filter_from_column_type(d)] = (
                        [int(combination[j])]
                        if isinstance(combination[j], (numpy.int32, numpy.int64))
                        else [combination[j]]
                    )
                filters = filters_conjunction(filters, self.template_filters)
                labels, weights = self._load_weights_table_from_template(
                    mode=key, template_filters=filters, preview=self.preview
                )
            else:
                labels = [None]
                weights = [1]

            if self.randomize:
                gen_vals = self.random_generator.choice(
                    labels, p=weights, size=size, shuffle=True
                )
            else:
                gen_vals = numpy.resize(labels, size)
            mask = numpy.all(dependency_rows == combination, axis=1)
            values = numpy.where(mask, gen_vals, values)

        return values

    def get_generator_type(self):
        return f"{self.generator_type}.{self.template_name.upper()}"
