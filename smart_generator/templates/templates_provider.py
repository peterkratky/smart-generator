from datetime import datetime
from enum import Enum
from typing import Protocol

from cachetools import LRUCache, cached, keys

from ..helpers.merging_filters import filters_merge
from ..helpers.template_column_naming import (id_column_type_from_template,
                                              label_column_type_from_template)
from ..helpers.timeseries_coding import (convert_step_to_millis,
                                         encode_timestamp)
from .template_table import TemplateTable


def _filter_key(*args, template_filters={}, **kwargs):
    key = keys.hashkey(*args, **kwargs)
    if template_filters:
        key += tuple(sorted([(k, tuple(v)) for (k, v) in template_filters.items()]))
    return key


class TemplatesProvider:
    """
    A class used to represent a provider of templates. It holds information about all
    templates and provides methods to access them.

    Attributes:
        tables (dict): Dictionary of all templates.
        functions (dict): Dictionary of all functions used for generating expressions.
    """

    def __init__(self):
        self.tables = {}
        self.functions = {}

    def add_table(self, table: TemplateTable):
        """
        Adds a template table to the provider.

        Args:
            table (TemplateTable): The template table to add.
        """
        self.tables[table.name] = table

    def add_function(self, func):
        """
        Adds a function to the provider.

        Args:
            func: The function to add.
        """
        self.functions[func.__name__] = func

    @cached(LRUCache(maxsize=128), key=_filter_key)
    def get_table_labels_weights(
        self, template_name: str, template_filters: dict[str, list[int]] = None
    ):
        """
        Returns labels and weights for a template table based on filters. This method is
        cached. This method is abstract and must be implemented in a subclass.

        Args:
            template_name (str): Name of the template table.
            template_filters (dict[str, list[int]]): Filters to apply to the template.
        """
        ...

    def get_table_dependencies(
        self, template_name: str, filter_names: list[str] = None
    ):
        """
        Returns dependencies for a template table based on filters. This method is
        abstract and must be implemented in a subclass.

        Args:
            template_name (str): Name of the template table.
            filter_names (list[str]): Filters to apply to the template.
        """
        ...

    def get_strong_dependencies(
        self,
        template_name: str,
        filter_names: list[str] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Returns strong dependencies for a template table based on filters.

        Args:
            template_name (str): Name of the template table.
            filter_names (list[str]): Filters to apply to the template.
            common_dependencies (list[str]): Common dependencies to apply
                to the template.
        """
        dependencies = []
        if self.tables[template_name.lower()].id_column:
            dependencies.append(id_column_type_from_template(template_name))
        if self.tables[template_name.lower()].dependency_templates:
            for dependency in self.tables[template_name.lower()].dependency_templates:
                dependencies.append(id_column_type_from_template(dependency))
        if self.tables[template_name.lower()].weak_dependency_templates:
            for dependency in self.tables[
                template_name.lower()
            ].weak_dependency_templates:
                if filter_names and dependency in filter_names:
                    dependencies.append(id_column_type_from_template(dependency))
                if common_dependencies and dependency in common_dependencies:
                    dependencies.append(id_column_type_from_template(dependency))
        return dependencies

    def get_weak_dependencies(self, template_name: str):
        """
        Returns weak dependencies for a template table based on filters.

        Args:
            template_name (str): Name of the template table.
        """
        dependencies = []
        if self.tables[template_name.lower()].weak_dependency_templates:
            for dependency in self.tables[
                template_name.lower()
            ].weak_dependency_templates:
                dependencies.append(id_column_type_from_template(dependency))
        return dependencies

    def find_related_filters(self, template_filters: dict[str, list[int]]):
        """
        Returns related filters for a template table based on filters. For example, if
        the filter contains city ids, the method returns also respective country ids.
        This is an abstract method and must be implemented in a subclass.

        Args:
            template_filters (dict[str, list[int]]): Filters to apply to the template.
        """
        ...

    def find_related_common_dependencies(self, common_dependencies: list[str]):
        """
        Returns related common dependencies for a template table based on filters. For
        example, if the list contains city ids, the method returns also respective
        country ids.

        Args:
            common_dependencies (list[str]): Common dependencies to apply to the
                template.
        """
        result = []

        if common_dependencies:
            for template in common_dependencies:
                template_id_column = self.get_table(template).id_column
                result.append(template_id_column)
                if template in self.tables:
                    t = self.tables[template]

                    for d in t.dependency_templates:
                        result.append(d)
                        result = list(
                            set(result + self.find_related_common_dependencies([d]))
                        )

        return result

    def get_label_dependencies(self, template_name: str):
        """
        Returns dependencies of columns which are used to generate labels.

        Args:
            template_name (str): Name of the template table.
        """
        dependencies = []
        if (
            hasattr(self.tables[template_name.lower()], "label_dependency_templates")
            and self.tables[template_name.lower()].label_dependency_templates
        ):
            for dependency in self.tables[
                template_name.lower()
            ].label_dependency_templates:
                dependencies.append(label_column_type_from_template(dependency))
        return dependencies

    def get_table(self, template_name: str):
        """
        Returns a template table based on its name.

        Args:
            template_name (str): Name of the template table.
        """
        if template_name.lower() in self.tables:
            return self.tables[template_name.lower()]
        else:
            raise Exception(f"No template table defined for key {template_name}")

    def get_table_key(self, template_name: str):
        if template_name.lower() in self.tables:
            return self.tables[template_name.lower()].id_column
        else:
            raise Exception(f"No template table defined for key {template_name}")

    def encode_timestamp(self, template_name: str, timestamp: datetime):
        if template_name.lower() in self.tables:
            table = self.tables[template_name.lower()]
            return encode_timestamp(timestamp, table.frame, table.unit)
        else:
            raise Exception(f"No template table defined for key {template_name}")

    def get_timeseries_step(self, template_name: str):
        if template_name.lower() in self.tables:
            table = self.tables[template_name.lower()]
            return convert_step_to_millis(table.unit)
        else:
            raise Exception(f"No template table defined for key {template_name}")
