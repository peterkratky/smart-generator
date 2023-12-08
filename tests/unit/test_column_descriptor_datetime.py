from datetime import datetime

import marshmallow_dataclass

from smart_generator.descriptor import behaviour
from smart_generator.descriptor.column import ColumnDescriptorDatetime
from smart_generator.descriptor.enums import ColumnVisibilityType, DatetimePrecisionType


class TestColumnDescriptorDatetime:
    def test_load_increment(self):
        data = {
            "descriptor_type": "COL_DATETIME",
            "id": "1",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "precision": "MINUTE",
            "behaviour": {
                "behaviour_type": "INCREMENT",
                "start": "2020-01-01T01:10:33",
                "step": 60,
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorDatetime)().load(data)

        assert obj.descriptor_type == "COL_DATETIME"
        assert obj.id == "1"
        assert obj.seed == 1
        assert obj.name == "column1"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.precision == DatetimePrecisionType.MINUTE
        assert obj.behaviour.behaviour_type == "INCREMENT"
        assert obj.behaviour.start == datetime(2020, 1, 1, 1, 10, 33)
        assert obj.behaviour.step == 60

    def test_load_uniform_distribution(self):
        data = {
            "descriptor_type": "COL_DATETIME",
            "id": "2",
            "seed": 1,
            "name": "column2",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "precision": "MINUTE",
            "behaviour": {
                "behaviour_type": "UNIFORM_DISTRIBUTION",
                "min": "2020-01-01T01:10:33",
                "max": "2020-01-01T01:20:33",
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorDatetime)().load(data)

        assert obj.descriptor_type == "COL_DATETIME"
        assert obj.id == "2"
        assert obj.seed == 1
        assert obj.name == "column2"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.precision == DatetimePrecisionType.MINUTE
        assert obj.behaviour.behaviour_type == "UNIFORM_DISTRIBUTION"
        assert obj.behaviour.min == datetime(2020, 1, 1, 1, 10, 33)
        assert obj.behaviour.max == datetime(2020, 1, 1, 1, 20, 33)

    def test_load_weights_table(self):
        data = {
            "descriptor_type": "COL_DATETIME",
            "id": "3",
            "seed": 1,
            "name": "column3",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "precision": "MINUTE",
            "behaviour": {
                "behaviour_type": "WEIGHTS_TABLE",
                "weights_table": [
                    {"key": "2020-01-01T01:10:33", "value": 0.5},
                    {"key": "2020-01-01T01:20:33", "value": 0.5},
                ],
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorDatetime)().load(data)

        assert obj.descriptor_type == "COL_DATETIME"
        assert obj.id == "3"
        assert obj.seed == 1
        assert obj.name == "column3"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.precision == DatetimePrecisionType.MINUTE
        assert obj.behaviour.behaviour_type == "WEIGHTS_TABLE"
        assert obj.behaviour.weights_table[0].key == datetime(2020, 1, 1, 1, 10, 33)
        assert obj.behaviour.weights_table[0].value == 0.5
        assert obj.behaviour.weights_table[1].key == datetime(2020, 1, 1, 1, 20, 33)
        assert obj.behaviour.weights_table[1].value == 0.5

    def test_load_template_label(self):
        data = {
            "descriptor_type": "COL_DATETIME",
            "id": "4",
            "seed": 1,
            "name": "column4",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "precision": "MINUTE",
            "behaviour": {
                "behaviour_type": "TEMPLATE_LABEL",
                "template": "template1",
                "template_filters": {"filter1": [1, 2, 3]},
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorDatetime)().load(data)

        assert obj.descriptor_type == "COL_DATETIME"
        assert obj.id == "4"
        assert obj.seed == 1
        assert obj.name == "column4"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.precision == DatetimePrecisionType.MINUTE
        assert obj.behaviour.behaviour_type == "TEMPLATE_LABEL"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["filter1"] == [1, 2, 3]

    def test_load_template_timestamp(self):
        data = {
            "descriptor_type": "COL_DATETIME",
            "id": "5",
            "seed": 1,
            "name": "column5",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "precision": "MINUTE",
            "behaviour": {
                "behaviour_type": "TEMPLATE_TIMESTAMP",
                "template": "template1",
                "start": "2020-01-01T01:10:33",
                "end": "2020-01-01T01:20:33",
                "template_filters": {"filter1": [1, 2, 3]},
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorDatetime)().load(data)

        assert obj.descriptor_type == "COL_DATETIME"
        assert obj.id == "5"
        assert obj.seed == 1
        assert obj.name == "column5"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.precision == DatetimePrecisionType.MINUTE
        assert obj.behaviour.behaviour_type == "TEMPLATE_TIMESTAMP"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.start == datetime(2020, 1, 1, 1, 10, 33)
        assert obj.behaviour.end == datetime(2020, 1, 1, 1, 20, 33)
        assert obj.behaviour.template_filters["filter1"] == [1, 2, 3]

    def test_get_descriptor_type_increment(self):
        obj = ColumnDescriptorDatetime(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=DatetimePrecisionType.MINUTE,
            behaviour=behaviour.Increment(
                start=datetime(2020, 1, 1, 1, 10, 33), step=60
            ),
        )
        assert obj.get_descriptor_type() == "COL_DATETIME.INCREMENT"

    def test_get_descriptor_type_uniform_distribution(self):
        obj = ColumnDescriptorDatetime(
            id="2",
            seed=1,
            name="column2",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=DatetimePrecisionType.MINUTE,
            behaviour=behaviour.UniformDistribution(
                min=datetime(2020, 1, 1, 1, 10, 33), max=datetime(2020, 1, 1, 1, 20, 33)
            ),
        )
        assert obj.get_descriptor_type() == "COL_DATETIME.UNIFORM_DISTRIBUTION"

    def test_get_descriptor_type_weights_table(self):
        obj = ColumnDescriptorDatetime(
            id="3",
            seed=1,
            name="column3",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=DatetimePrecisionType.MINUTE,
            behaviour=behaviour.WeightsTable(
                weights_table=[
                    {"key": datetime(2020, 1, 1, 1, 10, 33), "value": 0.5},
                    {"key": datetime(2020, 1, 1, 1, 10, 33), "value": 0.5},
                ]
            ),
        )
        assert obj.get_descriptor_type() == "COL_DATETIME.WEIGHTS_TABLE"

    def test_get_descriptor_type_template_label(self):
        obj = ColumnDescriptorDatetime(
            id="4",
            seed=1,
            name="column4",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=DatetimePrecisionType.MINUTE,
            behaviour=behaviour.TemplateLabel(
                template="template1", template_filters={"filter1": [1, 2, 3]}
            ),
        )
        assert obj.get_descriptor_type() == "COL_DATETIME.TEMPLATE_LABEL.LABEL"

    def test_get_descriptor_type_template_timestamp(self):
        obj = ColumnDescriptorDatetime(
            id="5",
            seed=1,
            name="column5",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=DatetimePrecisionType.MINUTE,
            behaviour=behaviour.TemplateTimestamp(
                template="template1",
                start=datetime(2020, 1, 1, 1, 10, 33),
                end=datetime(2020, 1, 1, 1, 20, 33),
                template_filters={"filter1": [1, 2, 3]},
            ),
        )
        assert obj.get_descriptor_type() == "COL_DATETIME.TEMPLATE_TIMESTAMP.TIMESTAMP"
