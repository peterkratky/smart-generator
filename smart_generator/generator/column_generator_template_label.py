import random
import re

import exrex

from ..descriptor.enums import (ColumnBehaviourTypeName, DescriptorTypeNames,
                                TemplateType)
from ..helpers.template_column_naming import template_from_column_type
from ..templates.enums import TemplateTableMode
from ..templates.templates_provider import TemplatesProvider
from .column_generator_template import ColumnGeneratorTemplate


class ColumnGeneratorTemplateId(ColumnGeneratorTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate ids of labels.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.TEMPLATE_LABEL}.{TemplateType.ID}"

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
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.
        """
        super().__init__(
            id,
            name,
            seed_sequence,
            seed_column,
            visible,
            na_prob,
            templates_provider,
            template_name,
            template_filters,
            common_dependencies,
        )
        if (
            self.strong_dependencies
            and f"{self.generator_type}.{template_name}" in self.strong_dependencies
        ):
            self.strong_dependencies.remove(f"{self.generator_type}.{template_name}")
        if (
            self.dependencies
            and f"{self.generator_type}.{template_name}" in self.dependencies
        ):
            self.dependencies.remove(f"{self.generator_type}.{template_name}")

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class. Generates ids of labels from the template. These ids are
        used to generate labels in other columns.
        """
        deps = self.strong_dependencies
        if len(deps) == 0:
            ids, weights = self._load_weights_table_from_template(
                mode=TemplateTableMode.ID,
                template_filters=self.template_filters,
                preview=self.preview,
            )
            return self.random_generator.choice(ids, p=weights, size=size)
        else:
            return self._generate_from_template(size, key=TemplateTableMode.ID)


class ColumnGeneratorTemplateLabelString(ColumnGeneratorTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate string labels.
    """

    generator_type = f"{DescriptorTypeNames.COL_STRING}.{ColumnBehaviourTypeName.TEMPLATE_LABEL}.{TemplateType.LABEL}"

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
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.
        """
        super().__init__(
            id,
            name,
            seed_sequence,
            seed_column,
            visible,
            na_prob,
            templates_provider,
            template_name,
            template_filters,
            common_dependencies,
        )
        self.template_label = "label"

    def _eval_expressions(self, values: list[str]):
        """
        Evaluates expressions in the values.

        Args:
            values (list[str]): List of values to evaluate.
        """
        for i in range(len(values)):
            vars = {**self.provider.functions}
            if self.label_dependencies:
                for d in self.label_dependencies:
                    vars[
                        template_from_column_type(d)
                    ] = self.linked_internal_generators[d].generated_values[i]
            to_eval = re.findall(r"\{\{[^\{\}]*\}\}", values[i])
            for e in to_eval:
                evaluated = eval(e.replace("{{", "").replace("}}", ""), vars)
                values[i] = values[i].replace(e, evaluated)

        random.seed(self.seed)
        return [exrex.getone(v) for v in values]

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class. Generates string labels from the template. If the values
        contains expressions, they are evaluated. Labels are strings.
        """
        values = None
        deps = self._get_effective_dependencies()
        if len(deps) == 0:
            labels, weights = self._load_weights_table_from_template(
                template_filters=self.template_filters, preview=self.preview
            )
            values = self.random_generator.choice(labels, p=weights, size=size)
        else:
            values = self._generate_from_template(size)

        if self.provider.get_table(self.template_name).using_expressions:
            values = self._eval_expressions(values)

        return values
