import marshmallow_dataclass

from smart_generator.descriptor import behaviour
from smart_generator.descriptor.column import ColumnDescriptorString
from smart_generator.descriptor.enums import ColumnVisibilityType


class TestColumnDescriptorString:
    def test_load_weights_table(self):
        data = {
            "descriptor_type": "COL_STRING",
            "id": "1",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "WEIGHTS_TABLE",
                "weights_table": [
                    {"key": "a", "value": 0.1},
                    {"key": "b", "value": 0.2},
                    {"key": "c", "value": 0.3},
                ],
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorString)().load(data)

        assert obj.descriptor_type == "COL_STRING"
        assert obj.id == "1"
        assert obj.seed == 1
        assert obj.name == "column1"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "WEIGHTS_TABLE"
        assert obj.behaviour.weights_table[0].key == "a"
        assert obj.behaviour.weights_table[0].value == 0.1
        assert obj.behaviour.weights_table[1].key == "b"
        assert obj.behaviour.weights_table[1].value == 0.2
        assert obj.behaviour.weights_table[2].key == "c"
        assert obj.behaviour.weights_table[2].value == 0.3

    def test_load_template_label(self):
        data = {
            "descriptor_type": "COL_STRING",
            "id": "2",
            "seed": 1,
            "name": "column2",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "TEMPLATE_LABEL",
                "template": "template1",
                "template_filters": {"key1": [1, 2, 3], "key2": [4, 5, 6]},
            },
        }

        obj = marshmallow_dataclass.class_schema(ColumnDescriptorString)().load(data)

        assert obj.descriptor_type == "COL_STRING"
        assert obj.id == "2"
        assert obj.seed == 1
        assert obj.name == "column2"
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0.5
        assert obj.behaviour.behaviour_type == "TEMPLATE_LABEL"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["key1"] == [1, 2, 3]
        assert obj.behaviour.template_filters["key2"] == [4, 5, 6]

    def test_get_descriptor_type_weights_table(self):
        obj = ColumnDescriptorString(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.WeightsTable(
                weights_table=[{"key": "a", "value": 0.1}]
            ),
        )
        assert obj.get_descriptor_type() == "COL_STRING.WEIGHTS_TABLE"

    def test_get_descriptor_type_template_label(self):
        obj = ColumnDescriptorString(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            behaviour=behaviour.TemplateLabel(
                template="template1", template_filters={"key": 1}
            ),
        )
        assert obj.get_descriptor_type() == "COL_STRING.TEMPLATE_LABEL.LABEL"
