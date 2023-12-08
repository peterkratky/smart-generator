import pytest
import pandas as pd
import numpy as np

from smart_generator.generator.column_generator_template import ColumnGeneratorTemplate
from smart_generator.templates.template_table import TemplateTable

from smart_generator.templates.templates_provider import TemplatesProvider


class TestColumnGeneratorTemplate:
    @pytest.fixture()
    def mocked_provider(self, mocker):
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_strong_dependencies",
            return_value=["COL_STRING.TEMPLATE_LABEL.ID.CITY"],
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_weak_dependencies",
            return_value=[
                "COL_STRING.TEMPLATE_LABEL.ID.CITY",
                "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
            ],
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_label_dependencies",
            return_value=[],
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_table_key",
            return_value="city_id",
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_table",
            return_value=TemplateTable(
                "city", "city", id_column="city_id", dependency_templates=["country_id"]
            ),
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.TemplatesProvider.get_table_labels_weights",
            return_value=pd.DataFrame({"value": ["l1", "l2"], "weight": [0.1, 0.3]}),
        )

    def test_base_constructor(self, mocked_provider):
        # m = mocker.patch("templates.TemplatesProvider", return_value = None)
        # mocker.patch("generator.column_generator_template.ColumnGeneratorTemplate.__init__", return_value=None)
        # m.return_value = TemplatesProvider()
        # m.get_strong_dependencies.return_value = ["COLUMN_TEMPLATE.ID.CITY"]
        # m.get_weak_dependencies.return_value = ["COLUMN_TEMPLATE.ID.CITY", "COLUMN_TEMPLATE.ID.COUNTRY"]

        # mocker.patch("generator.column_generator_template.ColumnGeneratorTemplate.__init__.provider.get_strong_dependencies", return_value=["COLUMN_TEMPLATE.ID.CITY"])

        generator = ColumnGeneratorTemplate(
            id="id1",
            name="name1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )
        # m.assert_called_once()

        assert generator.template_name == "CITY"
        assert generator.strong_dependencies == ["COL_STRING.TEMPLATE_LABEL.ID.CITY"]
        assert generator.weak_dependencies == [
            "COL_STRING.TEMPLATE_LABEL.ID.CITY",
            "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
        ]
        assert generator.dependencies == list(
            set(
                [
                    "COL_STRING.TEMPLATE_LABEL.ID.CITY",
                    "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
                ]
            )
        )
        assert generator.template_key == "city_id"
        assert len(generator.template_filters.items()) == 1
        assert list(generator.template_filters.keys())[0] == "city_id"
        assert list(generator.template_filters.values())[0] == [1]
        assert generator.common_dependencies == ["country_id"]

    def test_get_effective_dependencies(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        mocker.patch.object(
            generator,
            "linked_internal_generators",
            ["COL_STRING.TEMPLATE_LABEL.ID.CITY"],
        )
        mocker.patch.object(
            generator, "dependencies", ["COL_STRING.TEMPLATE_LABEL.ID.CITY"]
        )

        assert generator._get_effective_dependencies() == [
            "COL_STRING.TEMPLATE_LABEL.ID.CITY"
        ]

    def test_load_weights_table_from_template(self, mocked_provider):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        labels, weights = generator._load_weights_table_from_template("label")

        assert np.array_equal(labels, np.array(["l1", "l2"]))
        assert np.sum(weights) == pytest.approx(1)

    def test_load_weights_table_from_template_empty_table(
        self, mocker, mocked_provider
    ):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        mocker.patch.object(
            generator.provider, "get_table_labels_weights", return_value=pd.DataFrame()
        )

        labels, weights = generator._load_weights_table_from_template("label")

        assert labels == [None]
        assert weights == [1]

    def test_generate_from_template(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        mocker.patch.object(
            generator,
            "_get_dependency_column_values",
            return_value=[[1, 0, 1, 0], [2, 2, 3, 3]],
        )
        mocker.patch.object(
            generator,
            "_get_effective_dependencies",
            return_value=[
                "COL_STRING.TEMPLATE_LABEL.ID.CITY",
                "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
            ],
        )

        values = generator._generate_from_template(4)
        assert np.array_equal(values, np.array(["l2", "l2", "l2", "l2"]))

    def test_generate_from_template_none_values(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        mocker.patch.object(
            generator,
            "_get_dependency_column_values",
            return_value=[[1, None, 1, None], [2, 2, 3, 3]],
        )
        mocker.patch.object(
            generator,
            "_get_effective_dependencies",
            return_value=[
                "COL_STRING.TEMPLATE_LABEL.ID.CITY",
                "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
            ],
        )

        values = generator._generate_from_template(4)
        assert np.array_equal(values, np.array(["l2", None, "l2", None]))

    def test_generate_from_template_empty_table(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplate(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
        )

        mocker.patch.object(
            generator,
            "_get_dependency_column_values",
            return_value=[[1, None, 1, None], [2, 2, 3, 3]],
        )
        mocker.patch.object(
            generator,
            "_get_effective_dependencies",
            return_value=[
                "COL_STRING.TEMPLATE_LABEL.ID.CITY",
                "COL_STRING.TEMPLATE_LABEL.ID.COUNTRY",
            ],
        )
        mocker.patch.object(
            generator.provider, "get_table_labels_weights", return_value=pd.DataFrame()
        )

        values = generator._generate_from_template(4)
        assert np.array_equal(values, np.array([None, None, None, None]))
