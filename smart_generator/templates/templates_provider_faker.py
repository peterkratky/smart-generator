import logging

import pandas
from cachetools import LRUCache, cached, keys
from faker import Faker

from .enums import TemplateTableMode
from .templates_provider import TemplatesProvider


def _filter_key(*args, template_filters={}, **kwargs):
    key = keys.hashkey(*args, **kwargs)
    if template_filters:
        key += tuple(sorted([(k, tuple(v)) for (k, v) in template_filters.items()]))
    return key


class TemplatesProviderFromFaker(TemplatesProvider):
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
        filter_locales = []
        if template_filters:
            for key, value in template_filters.items():
                if key.lower() == "locale":
                    filter_locales.extend(value)
        if len(filter_locales) > 0:
            filter_locales = [l for l in filter_locales if l in self.locales]
            if len(filter_locales) == 0:
                logging.warning(f"No valid locale filters supplied.")

        if template_name.lower() == "locale":
            if len(filter_locales) > 0:
                values = filter_locales
            else:
                values = self.locales
        else:
            if len(filter_locales) == 0:
                filter_locales = None
            try:
                faker = Faker(locale=filter_locales)
            except:
                faker = Faker()
            Faker.seed(1)
            method = getattr(faker, template_name.lower())
            sampling_size = 100
            if filter_locales is None:
                sampling_size = 1000
            values = [method() for _ in range(sampling_size)]

        table = pandas.DataFrame()
        table["value"] = values

        table = (
            table[["value"]]
            .groupby(["value"], as_index=True)["value"]
            .count()
            .reset_index(name="weight")
        )
        table = table.sort_values(by=["weight"], ascending=False)

        return table

    def find_related_filters(self, template_filters: dict[str, list[int]]):
        return template_filters
