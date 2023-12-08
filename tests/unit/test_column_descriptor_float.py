import marshmallow_dataclass

from smart_generator.descriptor import behaviour
from smart_generator.descriptor.column import ColumnDescriptorFloat
from smart_generator.descriptor.enums import (
    ColumnVisibilityType,
    DescriptorTypeNames,
    GeoCoordinateType,
)


class TestColumnDescriptorFloat:
    def test_load_increment(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {"behaviour_type": "INCREMENT", "start": 1, "step": 1},
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.Increment)
        assert obj.behaviour.behaviour_type == "INCREMENT"
        assert obj.behaviour.start == 1
        assert obj.behaviour.step == 1
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_unique(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {"behaviour_type": "UNIQUE", "min": 1, "max": 10},
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.Unique)
        assert obj.behaviour.behaviour_type == "UNIQUE"
        assert obj.behaviour.min == 1
        assert obj.behaviour.max == 10
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_uniform_distribution(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "UNIFORM_DISTRIBUTION",
                "min": 1,
                "max": 10,
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.UniformDistribution)
        assert obj.behaviour.behaviour_type == "UNIFORM_DISTRIBUTION"
        assert obj.behaviour.min == 1
        assert obj.behaviour.max == 10
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_normal_distribution(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "NORMAL_DISTRIBUTION",
                "mean": 1,
                "std_dev": 10,
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.NormalDistribution)
        assert obj.behaviour.behaviour_type == "NORMAL_DISTRIBUTION"
        assert obj.behaviour.mean == 1
        assert obj.behaviour.std_dev == 10
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_exponential_distribution(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {"behaviour_type": "EXPONENTIAL_DISTRIBUTION", "scale": 1},
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.ExponentialDistribution)
        assert obj.behaviour.behaviour_type == "EXPONENTIAL_DISTRIBUTION"
        assert obj.behaviour.scale == 1
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_weights_table(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "WEIGHTS_TABLE",
                "weights_table": [{"key": 1, "value": 1}, {"key": 2, "value": 2}],
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.WeightsTable)
        assert obj.behaviour.behaviour_type == "WEIGHTS_TABLE"
        assert obj.behaviour.weights_table[0].key == 1
        assert obj.behaviour.weights_table[0].value == 1
        assert obj.behaviour.weights_table[1].key == 2
        assert obj.behaviour.weights_table[1].value == 2
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_template_label(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "TEMPLATE_LABEL",
                "template": "template1",
                "template_filters": {"filter1": [1, 2]},
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.TemplateLabel)
        assert obj.behaviour.behaviour_type == "TEMPLATE_LABEL"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["filter1"] == [1, 2]
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_template_timeseries(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "TEMPLATE_TIMESERIES",
                "template": "template1",
                "template_filters": {"filter1": [1, 2]},
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.precision == 2
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.TemplateTimeseries)
        assert obj.behaviour.behaviour_type == "TEMPLATE_TIMESERIES"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.template_filters["filter1"] == [1, 2]
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_load_template_geolocation(self):
        data = {
            "descriptor_type": "COL_FLOAT",
            "id": "id",
            "seed": 1,
            "name": "column1",
            "visibility_type": "VISIBLE",
            "precision": 2,
            "na_prob": 0,
            "behaviour": {
                "behaviour_type": "TEMPLATE_GEOLOCATION",
                "template": "template1",
                "coordinate_type": "LONGITUDE_WGS84",
                "template_filters": {"filter1": [1, 2]},
            },
        }
        schema = marshmallow_dataclass.class_schema(ColumnDescriptorFloat)()
        obj = schema.load(data)
        assert obj.id == "id"
        assert obj.seed == 1
        assert obj.visibility_type == ColumnVisibilityType.VISIBLE
        assert obj.na_prob == 0
        assert isinstance(obj.behaviour, behaviour.TemplateGeoLocation)
        assert obj.behaviour.behaviour_type == "TEMPLATE_GEOLOCATION"
        assert obj.behaviour.template == "template1"
        assert obj.behaviour.coordinate_type == GeoCoordinateType.LONGITUDE_WGS84
        assert obj.behaviour.template_filters["filter1"] == [1, 2]
        assert obj.descriptor_type == DescriptorTypeNames.COL_FLOAT

    def test_get_descriptor_type_increment(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.Increment(start=10, step=2),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.INCREMENT"

    def test_get_descriptor_type_unique(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.Unique(min=10, max=20),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.UNIQUE"

    def test_get_descriptor_type_uniform_distribution(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.UniformDistribution(min=10, max=20),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.UNIFORM_DISTRIBUTION"

    def test_get_descriptor_type_normal_distribution(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.NormalDistribution(mean=10, std_dev=20),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.NORMAL_DISTRIBUTION"

    def test_get_descriptor_type_exponential_distribution(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.ExponentialDistribution(scale=10),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.EXPONENTIAL_DISTRIBUTION"

    def test_get_descriptor_type_weights_table(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.WeightsTable(weights_table={"key": 1, "value": 0.1}),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.WEIGHTS_TABLE"

    def test_get_descriptor_type_template_label(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.TemplateLabel(
                template="template1", template_filters={"filter1": [1, 2]}
            ),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.TEMPLATE_LABEL.LABEL"

    def test_get_descriptor_type_template_timeseries(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.TemplateTimeseries(
                template="template1", template_filters={"filter1": [1, 2]}
            ),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.TEMPLATE_TIMESERIES.TIMESERIES"

    def test_get_descriptor_type_template_geolocation(self):
        obj = ColumnDescriptorFloat(
            id="1",
            seed=1,
            name="column1",
            visibility_type=ColumnVisibilityType.VISIBLE,
            precision=2,
            behaviour=behaviour.TemplateGeoLocation(
                template="template1",
                coordinate_type=GeoCoordinateType.LONGITUDE_WGS84,
                template_filters={"filter1": [1, 2]},
            ),
        )
        assert obj.get_descriptor_type() == "COL_FLOAT.TEMPLATE_GEOLOCATION.GEOLOCATION"
