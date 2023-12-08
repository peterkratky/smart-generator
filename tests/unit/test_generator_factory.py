import pytest
import pandas as pd

from smart_generator.descriptor import behaviour
from smart_generator.descriptor.column import ColumnDescriptorInteger
from smart_generator.descriptor.enums import ColumnVisibilityType
from smart_generator.descriptor.table_descriptor import TableDescriptor
from smart_generator.generator.column_generator import ColumnGenerator
from smart_generator.generator.column_generator_template_label import (
    ColumnGeneratorTemplateId,
)
from smart_generator.generator.sequence_generator import SequenceGenerator
from smart_generator.generator_factory import (
    create_table_generator,
    create_generator,
    create_internal_generators_hierarchy,
    create_internal_generators,
    create_generators,
    get_generator_hierarchy,
)


class TestColumnGeneratorTemplate:
    @pytest.fixture()
    def mocked_provider(self, mocker):
        mocker.patch(
            "templates.templates_provider.TemplatesProvider.get_strong_dependencies",
            return_value=["COLUMN_TEMPLATE.ID.CITY"],
        )
        mocker.patch(
            "templates.templates_provider.TemplatesProvider.get_weak_dependencies",
            return_value=["COLUMN_TEMPLATE.ID.CITY", "COLUMN_TEMPLATE.ID.COUNTRY"],
        )
        mocker.patch(
            "templates.templates_provider.TemplatesProvider.get_table_key",
            return_value="city_id",
        )
        mocker.patch(
            "templates.templates_provider.TemplatesProvider.get_table",
            return_value=pd.DataFrame({"label": ["l1", "l2"], "weight": [0.1, 0.3]}),
        )

    def test_create_table_generator(self, mocker):
        m = mocker.patch(
            "smart_generator.generator_factory.get_generator_hierarchy",
            return_value=TableDescriptor(name="table", descriptors=None, seed=1),
        )

        generator = create_table_generator(TableDescriptor("t_name", None))

        m.assert_called_once()

        assert generator.name == "table"

    def test_create_generator_integer_incremental(self, mocker):
        descriptor = ColumnDescriptorInteger(
            id="id1",
            seed=1,
            name="name1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )

        generator = create_generator(descriptor, 1)

        assert generator.id == descriptor.id
        assert generator.name == descriptor.name
        assert generator.seed == 2  # descriptor seed + seed passed in the function
        assert generator.visible
        assert generator.na_prob == 0
        assert generator.start == 1
        assert generator.step == 2

    def test_create_internal_generators(self, mocker):
        dependencies = [
            "COL_INTEGER.TEMPLATE_LABEL.ID.CITY",
            "COL_INTEGER.TEMPLATE_LABEL.ID.COUNTRY",
        ]
        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        generators = create_internal_generators(dependencies, 1, 1)

        assert len(generators) == 2
        assert generators[0].name == "COUNTRY_ID_2"
        assert generators[0].seed == 2
        assert generators[1].name == "CITY_ID_2"
        assert generators[1].seed == 2

    def test_create_internal_generators_common_dependencies(self, mocker):
        dependencies = [
            "COL_INTEGER.TEMPLATE_LABEL.ID.CITY",
            "COL_INTEGER.TEMPLATE_LABEL.ID.COUNTRY",
        ]
        common_dependency_keys = ["country_id"]
        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        generators = create_internal_generators(
            dependencies, 1, 1, common_dependencies=common_dependency_keys
        )

        assert len(generators) == 2
        assert generators[0].name == "COUNTRY_ID_1"
        assert generators[0].seed == 1
        assert generators[1].name == "CITY_ID_2"
        assert generators[1].seed == 2

    def test_create_internal_generators_invalid_dependencies(self, mocker):
        dependencies = ["COLUMN_SOMETHING"]
        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        with pytest.raises(ValueError) as ex:
            create_internal_generators(dependencies, 1, 1)

    def test_create_internal_generators_hierarchy_1_level(self, mocker):
        generator = ColumnGeneratorTemplateId(
            "id1", "name1", 1, 1, True, 0, None, "city"
        )
        m = mocker.patch(
            "smart_generator.generator_factory.create_internal_generators",
            return_value=[generator],
        )

        generators = create_internal_generators_hierarchy([], 1, 1)

        m.assert_called_once()
        assert len(generators) == 1

    def test_create_internal_generators_hierarchy_2_levels(self, mocker):
        generator1 = ColumnGeneratorTemplateId(
            "id1", "name1", 1, 1, True, 0, None, "city"
        )
        generator1.dependencies = ["COLUMN_TEMPLATE.ID.COUNTRY"]
        generator2 = ColumnGeneratorTemplateId(
            "id2", "name2", 1, 1, True, 0, None, "country"
        )

        m = mocker.patch(
            "smart_generator.generator_factory.create_internal_generators",
            side_effect=[[generator1], [generator2]],
        )

        generators = create_internal_generators_hierarchy([], 1, 1)

        assert m.call_count == 2
        assert len(generators) == 2

    def test_create_generators_no_dependencies(self, mocker):
        descriptor1 = ColumnDescriptorInteger(
            id="id1",
            seed=1,
            name="name1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )
        descriptor2 = ColumnDescriptorInteger(
            id="id2",
            seed=2,
            name="name2",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )

        generator1 = ColumnGenerator("id1", "name1", 1, 1, True, 0)
        generator2 = ColumnGenerator("id2", "name2", 2, 2, True, 0)
        m = mocker.patch(
            "smart_generator.generator_factory.create_generator",
            side_effect=[generator1, generator2],
        )

        generators, internal_generators = create_generators([descriptor1, descriptor2])

        assert m.call_count == 2
        assert len(generators) == 2
        assert len(internal_generators) == 0

    def test_create_generators_dependencies(self, mocker):
        descriptor1 = ColumnDescriptorInteger(
            id="id1",
            seed=1,
            name="name1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )
        descriptor2 = ColumnDescriptorInteger(
            id="id2",
            seed=2,
            name="name2",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )

        generator1 = ColumnGenerator("id1", "name1", 1, 1, True, 0)
        generator2 = ColumnGenerator("id2", "name2", 2, 2, True, 0)
        generator1.strong_dependencies = ["COL_INTEGER.TEMPLATE_LABEL.ID.COUNTRY"]
        generator1.label_dependencies = []
        m = mocker.patch(
            "smart_generator.generator_factory.create_generator",
            side_effect=[generator1, generator2],
        )

        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        generators, internal_generators = create_generators([descriptor1, descriptor2])

        assert m.call_count == 2
        assert len(generators) == 2
        assert len(internal_generators) == 1

    def test_create_generators_filters(self, mocker):
        descriptor1 = ColumnDescriptorInteger(
            id="id1",
            seed=1,
            name="name1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )
        descriptor2 = ColumnDescriptorInteger(
            id="id2",
            seed=2,
            name="name2",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )

        generator1 = ColumnGenerator("id1", "name1", 1, 1, True, 0)
        generator2 = ColumnGenerator("id2", "name2", 2, 2, True, 0)
        generator1.strong_dependencies = ["COL_INTEGER.TEMPLATE_LABEL.ID.COUNTRY"]
        generator1.label_dependencies = []
        m = mocker.patch(
            "smart_generator.generator_factory.create_generator",
            side_effect=[generator1, generator2],
        )

        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        generators, internal_generators = create_generators(
            [descriptor1, descriptor2], template_filters={"country_id": 1}
        )

        assert m.call_count == 2
        assert m.mock_calls[0].args[2] == {"country_id": 1}
        assert m.mock_calls[1].args[2] == {"country_id": 1}
        assert len(generators) == 2
        assert len(internal_generators) == 1

    def test_get_generator_hierarchy(self, mocker):
        descriptor2 = ColumnDescriptorInteger(
            id="id2",
            seed=2,
            name="name2",
            visibility_type=ColumnVisibilityType.VISIBLE,
            na_prob=0,
            behaviour=behaviour.Increment(start=1, step=2),
        )
        descriptor1 = TableDescriptor(
            id="id1", seed=1, name="name_s", descriptors=[descriptor2]
        )

        generator1 = SequenceGenerator("id1", "name1", 1, 1)
        generator2 = ColumnGenerator("id2", "name2", 2, 2, True, 0)
        m1 = mocker.patch(
            "smart_generator.generator_factory.create_generator",
            return_value=generator1,
        )
        m2 = mocker.patch(
            "smart_generator.generator_factory.create_generators",
            return_value=([generator2], []),
        )

        mocker.patch(
            "smart_generator.generator_factory.get_templates_provider",
            return_value=None,
        )

        generator = get_generator_hierarchy(descriptor1)

        assert len(generator.child_column_generators) == 1
