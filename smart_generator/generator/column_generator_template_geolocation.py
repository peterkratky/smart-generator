from ..descriptor.enums import (ColumnBehaviourTypeName, DescriptorTypeNames,
                                GeoCoordinateType, TemplateType)
from ..templates.enums import TemplateTableMode
from ..templates.templates_provider import TemplatesProvider
from .column_generator_template import ColumnGeneratorTemplate


class ColumnGeneratorTemplateGeolocation(ColumnGeneratorTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate geolocation values. This class is meant to be inherited by
    other classes.

    Attributes:
        precision (int): Number of decimal places of the numeric values.
        coordinate_type (GeoCoordinateType): Type of coordinate to generate.
    """

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        precision: int,
        templates_provider: TemplatesProvider,
        template_name: str,
        coordinate_type: GeoCoordinateType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.

        Args:
            precision (int): Number of decimal places of the numeric values.
            coordinate_type (GeoCoordinateType): Type of coordinate to generate.
        """
        super().__init__(
            id,
            name,
            seed_sequence,
            seed_column,
            visible,
            na_prob,
            templates_provider,
            template_name,
            template_filters,
            common_dependencies,
        )
        self.precision = precision
        self.coordinate_type = coordinate_type

    def _generate_geolocation_values(self, size: int):
        """
        Generates geolocation values from the template.

        Args:
            size (int): Number of the values to generate.
        """
        deps = self._get_effective_dependencies()
        values = None

        if self.coordinate_type == GeoCoordinateType.LONGITUDE_WGS84:
            if len(deps) == 0:
                labels, weights = self._load_weights_table_from_template(
                    mode=TemplateTableMode.LONGITUDE,
                    template_filters=self.template_filters,
                    preview=self.preview,
                )
                values = self.random_generator.choice(labels, p=weights, size=size)
            else:
                values = self._generate_from_template(
                    size, key=TemplateTableMode.LONGITUDE
                )

        if self.coordinate_type == GeoCoordinateType.LATITUDE_WGS84:
            if len(deps) == 0:
                labels, weights = self._load_weights_table_from_template(
                    mode=TemplateTableMode.LATITUDE,
                    template_filters=self.template_filters,
                    preview=self.preview,
                )
                values = self.random_generator.choice(labels, p=weights, size=size)
            else:
                values = self._generate_from_template(
                    size, key=TemplateTableMode.LATITUDE
                )

        return values.astype(float).round(self.precision)


class ColumnGeneratorTemplateGeolocationInt(ColumnGeneratorTemplateGeolocation):
    """
    A subclass of ColumnGeneratorTemplateGeolocation which represents a column generator
    of type int with geolocation values.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.TEMPLATE_GEOLOCATION}.{TemplateType.GEOLOCATION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        precision: int,
        templates_provider: TemplatesProvider,
        template_name: str,
        coordinate_type: GeoCoordinateType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplateGeolocation.__init__` of the parent class.
        """
        super().__init__(
            id,
            name,
            seed_sequence,
            seed_column,
            visible,
            na_prob,
            precision,
            templates_provider,
            template_name,
            coordinate_type,
            template_filters,
            common_dependencies,
        )

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class. Generates int values from the geo location template.
        """
        return self._generate_geolocation_values(size).astype(int)


class ColumnGeneratorTemplateGeolocationFloat(ColumnGeneratorTemplateGeolocation):
    """
    A subclass of ColumnGeneratorTemplateGeolocation which represents a column generator
    of type float with geolocation values.
    """

    generator_type = f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.TEMPLATE_GEOLOCATION}.{TemplateType.GEOLOCATION}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        precision: int,
        templates_provider: TemplatesProvider,
        template_name: str,
        coordinate_type: GeoCoordinateType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplateGeolocation.__init__` of the parent class.
        """
        super().__init__(
            id,
            name,
            seed_sequence,
            seed_column,
            visible,
            na_prob,
            precision,
            templates_provider,
            template_name,
            coordinate_type,
            template_filters,
            common_dependencies,
        )

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class. Generates float values from the geo location template.
        """
        return (
            self._generate_geolocation_values(size).astype(float).round(self.precision)
        )
