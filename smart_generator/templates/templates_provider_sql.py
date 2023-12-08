import json
import logging
from typing import Protocol

import numpy
import pandas
import sqlalchemy
from cachetools import LRUCache, cached, keys
from sqlalchemy import text as sql_text

from ..helpers.merging_filters import filters_merge
from ..helpers.template_column_naming import (id_column_type_from_template,
                                              label_column_type_from_template)
from .enums import TemplateTableMode
from .templates_provider import TemplatesProvider


def _filter_key(*args, template_filters={}, **kwargs):
    key = keys.hashkey(*args, **kwargs)
    if template_filters:
        key += tuple(sorted([(k, tuple(v)) for (k, v) in template_filters.items()]))
    return key


class TemplatesProviderFromSql(TemplatesProvider):
    def __init__(self, connection_string: str):
        super().__init__()
        self.engine = sqlalchemy.create_engine(connection_string)

    @cached(LRUCache(maxsize=1000000), key=_filter_key)
    def get_table_labels_weights(
        self,
        template_name: str,
        mode: TemplateTableMode = TemplateTableMode.DEFAULT,
        template_filters: dict[str, list[int]] = None,
        preview: bool = True,
    ):
        table = self.tables[template_name.lower()]
        conds = []
        for dependency in (
            table.dependency_templates + table.weak_dependency_templates + [table.name]
        ):
            dependency_column_id = self.get_table(dependency).id_column
            if template_filters and dependency in template_filters:
                conds.append(
                    f"{dependency_column_id} IN ({','.join(map(str, template_filters[dependency]))})"
                )
            elif template_filters:
                logging.warning(
                    f"Dependency {dependency} not found in filters {json.dumps(template_filters)}"
                )

        aggregate = False

        # top = "" if not preview else "TOP 1000"
        top = "" if not preview else "LIMIT 1000"

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
            # sql = f"SELECT {top} {key} as value, {weight} as weight FROM {table.table}"
            sql = f"SELECT {mode} as value, {weight} as weight FROM {table.source_name}"
            if len(conds) > 0:
                sql = sql + f" WHERE {' AND '.join(conds)}"
            sql = sql + f" {top}"
        else:
            # sql = f"SELECT {top} {key} as value, SUM({weight}) as weight FROM {table.table}"
            sql = f"SELECT {mode} as value, SUM({weight}) as weight FROM {table.source_name}"
            if len(conds) > 0:
                sql = sql + f" WHERE {' AND '.join(conds)}"
            sql = sql + f" GROUP BY {mode}"
            sql = sql + f" {top}"

        print(sql)

        with self.engine.connect() as connection:
            table = pandas.read_sql_query(
                sql=sql_text(sql), con=connection
            )  # , dtype={"weight": numpy.float32})
        # if table[template_key_name].dtype == numpy.float64:
        #    table[template_key_name] = table[template_key_name].astype(numpy.float32)
        return table

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
                filter_column_id = self.get_table(filter_key).id_column
                sql = f"SELECT {d} FROM {t.name} WHERE {filter_column_id} IN ({','.join(map(str, filter_values))})"
                with self.engine.connect() as connection:
                    table = pandas.read_sql_query(sql=sql_text(sql), con=connection)
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
        conds = []
        for dependency in (
            table.dependency_templates + table.weak_dependency_templates + [table.name]
        ):
            if template_filters and dependency in template_filters:
                conds.append(
                    f"{dependency} IN ({','.join(map(str, template_filters[dependency]))})"
                )
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

        sql = f"SELECT {key} as value, {stat}({key}) as stat FROM {table.source_name} GROUP BY {key}"
        if len(conds) > 0:
            sql = sql + f" WHERE {' AND '.join(conds)}"

        with self.engine.connect() as connection:
            table = pandas.read_sql_query(sql=sql_text(sql), con=connection)
        return table
