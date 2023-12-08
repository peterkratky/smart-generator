import pytest
import numpy as np

from smart_generator.generator.column_generator_template_label import (
    ColumnGeneratorTemplateId,
    ColumnGeneratorTemplateLabelString,
)
from smart_generator.templates.template_table import TemplateTable

from smart_generator.templates.templates_provider import TemplatesProvider


class TestColumnGeneratorTemplateLabel:
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
                "city",
                "city",
                id_column="city_id",
                dependency_templates=["country_id"],
                using_expressions=False,
            ),
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.ColumnGeneratorTemplate._load_weights_table_from_template",
            return_value=(["l1", "l2"], [0.3, 0.7]),
        )
        mocker.patch(
            "smart_generator.generator.column_generator_template.ColumnGeneratorTemplate._generate_from_template",
            return_value=np.array(["l2", None, "l2", None]),
        )

    def test_id_constructor(self, mocked_provider):
        generator = ColumnGeneratorTemplateId(
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

        assert generator.generator_type == "COL_INTEGER.TEMPLATE_LABEL.ID"
        assert generator.get_generator_type() == "COL_INTEGER.TEMPLATE_LABEL.ID.CITY"
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

    def test_id_generate_column_values(self, mocked_provider):
        generator = ColumnGeneratorTemplateId(
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

        values = generator._generate_column_values(4)
        assert np.array_equal(values, np.array(["l2", None, "l2", None]))

    def test_id_generate_column_values_no_dependecies(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplateId(
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

        mocker.patch.object(generator, "strong_dependencies", [])

        values = generator._generate_column_values(4)
        assert np.array_equal(values, np.array(["l1", "l1", "l2", "l1"]))

    def test_label_constructor(self, mocked_provider):
        generator = ColumnGeneratorTemplateLabelString(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )

        assert generator.generator_type == "COL_STRING.TEMPLATE_LABEL.LABEL"
        assert generator.get_generator_type() == "COL_STRING.TEMPLATE_LABEL.LABEL.CITY"
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

    def test_label_generate_column_values(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplateLabelString(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )

        mocker.patch.object(
            generator,
            "linked_internal_generators",
            ["COL_STRING.TEMPLATE_LABEL.ID.CITY"],
        )

        values = generator._generate_column_values(4)
        assert np.array_equal(values, np.array(["l2", None, "l2", None]))

    def test_lavel_generate_column_values_eval_expressions(
        self, mocker, mocked_provider
    ):
        generator = ColumnGeneratorTemplateLabelString(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )

        mocker.patch.object(
            generator.provider,
            "get_table",
            return_value=TemplateTable(
                "city",
                "city",
                id_column="city_id",
                dependency_templates=["country_id"],
                using_expressions=True,
            ),
        )
        mocked_method = mocker.patch.object(
            generator, "_eval_expressions", return_value=["l2", None, "l2", None]
        )

        generator._generate_column_values(4)

        mocked_method.assert_called_once()

    def test_label_generate_column_values_no_dependecies(self, mocker, mocked_provider):
        generator = ColumnGeneratorTemplateLabelString(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )

        mocker.patch.object(generator, "strong_dependencies", [])

        values = generator._generate_column_values(4)
        assert np.array_equal(values, np.array(["l1", "l1", "l2", "l1"]))

    def test_label_eval_expressions(self, mocked_provider):
        generator = ColumnGeneratorTemplateLabelString(
            id="id1",
            name="label1",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0,
            template_name="CITY",
            templates_provider=TemplatesProvider(),
            template_filters={"city_id": [1]},
            common_dependencies=["country_id"],
        )

        values = generator._eval_expressions(["[1-5]", "\d{3}"])
        assert np.array_equal(values, np.array(["1", "152"]))
