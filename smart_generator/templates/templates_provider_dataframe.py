import json
import logging
from typing import Protocol

import pandas
from cachetools import LRUCache, cached, keys

from ..helpers.merging_filters import filters_merge
from ..helpers.template_column_naming import id_column_type_from_template
from .enums import TemplateTableMode
from .templates_provider import TemplatesProvider


def _filter_key(*args, template_filters={}, **kwargs):
    key = keys.hashkey(*args, **kwargs)
    if template_filters:
        key += tuple(sorted([(k, tuple(v)) for (k, v) in template_filters.items()]))
    return key


class TemplatesProviderFromDataframe(TemplatesProvider):
    def __init__(self):
        super().__init__()
        self.dataframes = {}

    def add_dataframe(self, name: str, df: pandas.DataFrame):
        self.dataframes[name] = df

    @cached(LRUCache(maxsize=128), key=_filter_key)
    def get_table_labels_weights(
        self,
        template_name: str,
        mode: TemplateTableMode = TemplateTableMode.DEFAULT,
        template_filters: dict[str, list[int]] = None,
        preview: bool = True,
    ):
        table = self.tables[template_name.lower()]
        data_table = self.dataframes[template_name.lower()]

        for dependency in (
            table.dependency_templates + table.weak_dependency_templates + [table.name]
        ):
            if template_filters and dependency in template_filters:
                dependency_id_column = self.get_table(dependency).id_column
                data_table = data_table[
                    data_table[dependency_id_column].isin(template_filters[dependency])
                ]
            elif template_filters:
                logging.warning(
                    f"Dependency {dependency} not found in filters {json.dumps(template_filters)}"
                )

        aggregate = False

        if mode == TemplateTableMode.DEFAULT:
            mode = table.label_column
        elif mode == TemplateTableMode.ID:
            aggregate = True
            mode = table.id_column
        elif mode == TemplateTableMode.LONGITUDE:
            mode = table.longitude_column
        elif mode == TemplateTableMode.LATITUDE:
            mode = table.latitude_column

        weight = table.weight_column
        if not weight:
            weight = 1

        if not aggregate:
            data_table = data_table[[mode, weight]]
        else:
            data_table = data_table[[mode, weight]].groupby(mode).sum().reset_index()

        if preview:
            data_table = data_table.head(1000)

        # rename columns to value, weight
        data_table.columns = ["value", "weight"]

        return data_table

    def find_related_filters(self, template_filters: dict[str, list[int]]):
        result = {}
        if template_filters:
            for key, value in template_filters.items():
                result = filters_merge(result, self._find_parent_filters(key, value))
        return filters_merge(result, template_filters)

    def _find_parent_filters(self, filter_key: str, filter_values: list[str]):
        parent_filters = {}
        if filter_key.replace("_id", "") in self.tables:
            t = self.tables[filter_key.replace("_id", "")]

            for d in t.dependency_templates:
                table = self.dataframes[t.name]
                filter_column_id = self.get_table(filter_key).id_column
                table = table[table[filter_column_id].isin(filter_values)]
                d_column_id = self.get_table(d).id_column
                parent_filters[d] = table[d_column_id].tolist()
                parent_filters = filters_merge(
                    parent_filters,
                    self._find_parent_filters(d, table[d_column_id].tolist()),
                )

        return parent_filters

    def get_table_stats(
        self,
        template_name: str,
        key: TemplateTableMode = TemplateTableMode.DEFAULT,
        template_filters: dict[str, list[int]] = None,
        stat: str = "COUNT",
    ):
        table = self.tables[template_name.lower()]
        data_table = self.dataframes[template_name.lower()]

        for dependency in (
            table.dependency_templates + table.weak_dependency_templates + [table.name]
        ):
            if template_filters and dependency in template_filters:
                data_table = data_table[
                    data_table[dependency].isin(template_filters[dependency])
                ]
            elif template_filters:
                logging.warning(
                    f"Dependency {dependency} not found in filters {json.dumps(template_filters)}"
                )

        if key == TemplateTableMode.DEFAULT:
            key = table.label_column
        elif key == TemplateTableMode.ID:
            key = table.id_column
        elif key == TemplateTableMode.LONGITUDE:
            key = table.key_longitude
        elif key == TemplateTableMode.LATITUDE:
            key = table.key_latitude

        # return both key and respective count from table

        if stat == "COUNT":
            data_table = (
                data_table[[key]]
                .groupby([key], as_index=True)[key]
                .count()
                .reset_index(name="value")
            )
        else:
            raise ValueError(f"Stat {stat} not supported")

        data_table.columns = ["value", "stat"]

        return data_table
