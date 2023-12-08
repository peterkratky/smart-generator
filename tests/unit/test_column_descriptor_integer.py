import marshmallow_dataclass

from smart_generator.descriptor import behaviour
from smart_generator.descriptor.column import ColumnDescriptorInteger
from smart_generator.descriptor.enums import ColumnVisibilityType


class TestColumnDescriptorInteger:
    def test_load_increment(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "1",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {"behaviour_type": "INCREMENT", "start": 10, "step": 2},
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "1"
        assert obj.seed == 1
        assert obj.name == "column1"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "INCREMENT"
        assert obj.behaviour.start == 10
        assert obj.behaviour.step == 2

    def test_load_unique(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "2",
            "seed": 1,
            "name": "column2",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {"behaviour_type": "UNIQUE", "min": 1, "max": 1000000},
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "2"
        assert obj.seed == 1
        assert obj.name == "column2"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "UNIQUE"
        assert obj.behaviour.min == 1
        assert obj.behaviour.max == 1000000

    def test_load_uniform_distribution(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "3",
            "seed": 1,
            "name": "column3",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "UNIFORM_DISTRIBUTION",
                "min": 10,
                "max": 1000,
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "3"
        assert obj.seed == 1
        assert obj.name == "column3"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "UNIFORM_DISTRIBUTION"
        assert obj.behaviour.min == 10
        assert obj.behaviour.max == 1000

    def test_load_weights_table(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "4",
            "seed": 1,
            "name": "column4",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "WEIGHTS_TABLE",
                "weights_table": [
                    {"key": 1, "value": 0.1},
                    {"key": 2, "value": 0.2},
                    {"key": 3, "value": 0.3},
                ],
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "4"
        assert obj.seed == 1
        assert obj.name == "column4"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "WEIGHTS_TABLE"
        assert obj.behaviour.weights_table[0].key == 1
        assert obj.behaviour.weights_table[0].value == 0.1
        assert obj.behaviour.weights_table[1].key == 2
        assert obj.behaviour.weights_table[1].value == 0.2
        assert obj.behaviour.weights_table[2].key == 3
        assert obj.behaviour.weights_table[2].value == 0.3

    def test_load_normal_distribution(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "5",
            "seed": 1,
            "name": "column5",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "NORMAL_DISTRIBUTION",
                "mean": 10,
                "std_dev": 1,
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "5"
        assert obj.seed == 1
        assert obj.name == "column5"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "NORMAL_DISTRIBUTION"
        assert obj.behaviour.mean == 10
        assert obj.behaviour.std_dev == 1

    def test_load_exponential_distribution(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "6",
            "seed": 1,
            "name": "column6",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {"behaviour_type": "EXPONENTIAL_DISTRIBUTION", "scale": 7},
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "6"
        assert obj.seed == 1
        assert obj.name == "column6"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "EXPONENTIAL_DISTRIBUTION"
        assert obj.behaviour.scale == 7

    def test_load_template_label(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "7",
            "seed": 1,
            "name": "column7",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "TEMPLATE_LABEL",
                "template": "template1",
                "template_filters": {"key1": [1, 2, 3], "key2": [4, 5, 6]},
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "7"
        assert obj.seed == 1
        assert obj.name == "column7"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "TEMPLATE_LABEL"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["key1"] == [1, 2, 3]
        assert obj.behaviour.template_filters["key2"] == [4, 5, 6]

    def test_load_template_timeseries(self):
        data = {
            "descriptor_type": "COL_INTEGER",
            "id": "8",
            "seed": 1,
            "name": "column8",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "TEMPLATE_TIMESERIES",
                "template": "template1",
                "template_filters": {"key1": [1, 2, 3], "key2": [4, 5, 6]},
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorInteger)().load(data)

        assert obj.descriptor_type == "COL_INTEGER"
        assert obj.id == "8"
        assert obj.seed == 1
        assert obj.name == "column8"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "TEMPLATE_TIMESERIES"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["key1"] == [1, 2, 3]
        assert obj.behaviour.template_filters["key2"] == [4, 5, 6]

    def test_get_descriptor_type_increment(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.Increment(start=10, step=2),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.INCREMENT"

    def test_get_descriptor_type_unique(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.Unique(min=1, max=1000000),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.UNIQUE"

    def test_get_descriptor_type_uniform_distribution(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.UniformDistribution(min=10, max=1000),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.UNIFORM_DISTRIBUTION"

    def test_get_descriptor_type_weights_table(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.WeightsTable(weights_table={"key": 1, "value": 0.1}),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.WEIGHTS_TABLE"

    def test_get_descriptor_type_normal_distribution(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.NormalDistribution(mean=10, std_dev=1),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.NORMAL_DISTRIBUTION"

    def test_get_descriptor_type_exponential_distribution(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.ExponentialDistribution(scale=7),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.EXPONENTIAL_DISTRIBUTION"

    def test_get_descriptor_type_template_label(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.TemplateLabel(
                template="template1", template_filters={"key": 1}
            ),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.TEMPLATE_LABEL.LABEL"

    def test_get_descriptor_type_template_timeseries(self):
        obj = ColumnDescriptorInteger(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.TemplateTimeseries(
                template="template1", template_filters={"key": 1}
            ),
        )
        assert obj.get_descriptor_type() == "COL_INTEGER.TEMPLATE_TIMESERIES.TIMESERIES"
