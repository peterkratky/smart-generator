import numpy

from ..descriptor.enums import (ColumnBehaviourTypeName, DescriptorTypeNames,
                                TemplateType)
from ..templates.templates_provider import TemplatesProvider
from .column_generator_template import ColumnGeneratorTemplate


class ColumnGeneratorTimeseriesTemplate(ColumnGeneratorTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using templates to generate timeseries values. This class is meant to be inherited by other classes.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.TEMPLATE_TIMESERIES}.{TemplateType.TIMESERIES}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        templates_provider: TemplatesProvider,
        template_name: str,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor :meth:`ColumnGeneratorTemplate.__init__` of the parent class.
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
        # Adds date, time and datetime as dependencies for the timeseries column generator.
        self.dependencies.extend(["COL_DATE", "COL_TIME", "COL_DATETIME"])

    def _generate_timeseries_values(self, size: int):
        """
        Generates timeseries values from the template.

        Args:
            size (int): Number of the values to generate.
        """
        labels, weights = self._load_weights_table_from_template(
            template_filters=self.template_filters, preview=False
        )

        weights = weights / numpy.average(weights)

        # Date, time or datetime are required for the generation of timeseries values. First one of these dependencies is used.
        datetime_dep = next(
            (d for d in self.dependencies if d in self.linked_internal_generators), None
        )
        if datetime_dep:
            timestamps = self.linked_internal_generators[
                datetime_dep
            ].generated_values.tolist()
        else:
            raise Exception(
                f"No datetime/date/time column available for templated timeseries {self.name}"
            )

        # Timestamps in the templates for timeseries are encoded. This is done to more easily compare timestamps, not absolute, but relative (e.g. a timestamp regardelss the year).
        def encode_timestamp(timestamp):
            return self.provider.encode_timestamp(self.template_name, timestamp)[0]

        encoded_timestamps = numpy.array(list(map(encode_timestamp, timestamps)))

        return numpy.take(weights, encoded_timestamps)


class ColumnGeneratorTimeseriesTemplateInt(ColumnGeneratorTimeseriesTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using templates to generate timeseries values of int type.
    """

    generator_type = f"{DescriptorTypeNames.COL_INTEGER}.{ColumnBehaviourTypeName.TEMPLATE_TIMESERIES}.{TemplateType.TIMESERIES}"

    def __init__(
        self,
        id: str,
        name: str,
        seed_sequence: int,
        seed_column: int,
        visible: bool,
        na_prob: float,
        templates_provider: TemplatesProvider,
        template_name: str,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.
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

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class.
        Generates timeseries values from the template. These values are integers.
        """
        return self._generate_timeseries_values(size).astype(int)


class ColumnGeneratorTimeseriesTemplateFloat(ColumnGeneratorTimeseriesTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate timeseries values of float type.
    """

    generator_type = f"{DescriptorTypeNames.COL_FLOAT}.{ColumnBehaviourTypeName.TEMPLATE_TIMESERIES}.{TemplateType.TIMESERIES}"

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
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.
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

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class.
        Generates timeseries values from the template. These values are floats.
        """
        return (
            self._generate_timeseries_values(size).astype(float).round(self.precision)
        )
