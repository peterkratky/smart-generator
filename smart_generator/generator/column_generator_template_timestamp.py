from datetime import datetime, timezone

import numpy

from ..descriptor.enums import (ColumnBehaviourTypeName, DatePrecisionType,
                                DatetimePrecisionType, DescriptorTypeNames,
                                TemplateType, TimePrecisionType)
from ..helpers import datetime_precision
from ..templates.templates_provider import TemplatesProvider
from .column_generator_template import ColumnGeneratorTemplate


class ColumnGeneratorTimestampTemplate(ColumnGeneratorTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate timestamp values. This class is meant to be inherited by other
    classes.

    Attributes:
        start (datetime): Start of the timestamp range.
        end (datetime): End of the timestamp range.
    """

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
        start: datetime,
        end: datetime,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.

        Args:
            start (datetime): Start of the timestamp range.
            end (datetime): End of the timestamp range.
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
        self.start = start
        self.end = end

    def _generate_timestamp_values(self, size: int):
        """
        Generates timestamp values from the template.

        Args:
            size (int): Number of the values to generate.
        """
        labels, weights = self._load_weights_table_from_template(
            template_filters=self.template_filters, preview=False
        )

        start_timestamp = self.start.replace(tzinfo=timezone.utc).timestamp() * 1000
        end_timestamp = self.end.replace(tzinfo=timezone.utc).timestamp() * 1000

        # get step (a unit between two datetimes) in millis from the template
        step = self.provider.get_timeseries_step(self.template_name)
        timestamps = (
            numpy.arange(start_timestamp, end_timestamp, step, dtype=numpy.int64)
            .astype("datetime64[ms]")
            .tolist()
        )

        # Timestamps in the templates for timeseries are encoded. This is done to more
        # easily compare timestamps, not absolute, but relative (e.g. a timestamp
        # regardelss the year).
        def encode_timestamp(timestamp):
            return self.provider.encode_timestamp(self.template_name, timestamp)[0]

        encoded_timestamps = numpy.array(list(map(encode_timestamp, timestamps)))

        timestamps_weights = numpy.take(weights, encoded_timestamps)
        timestamps_weights = timestamps_weights / numpy.sum(timestamps_weights)

        values = self.random_generator.choice(
            timestamps, p=timestamps_weights, size=size, shuffle=False
        )
        values.sort()
        return values


class ColumnGeneratorTimestampTemplateDatetime(ColumnGeneratorTimestampTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate datetime values.

    Attributes:
        precision (DatetimePrecisionType): Precision of the datetime values.
    """

    generator_type = f"{DescriptorTypeNames.COL_DATETIME}.{ColumnBehaviourTypeName.TEMPLATE_TIMESTAMP}.{TemplateType.TIMESTAMP}"

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
        start: datetime,
        end: datetime,
        precision: DatetimePrecisionType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.

        Args:
            precision (DatetimePrecisionType): Precision of the datetime values.
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
            start,
            end,
            template_filters,
            common_dependencies,
        )
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class.
        Generates datetime values from the template.
        """
        timestamps = self._generate_timestamp_values(size)

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.datetime_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps


class ColumnGeneratorTimestampTemplateDate(ColumnGeneratorTimestampTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate date values.

    Attributes:
        precision (DatePrecisionType): Precision of the date values.
    """

    generator_type = f"{DescriptorTypeNames.COL_DATE}.{ColumnBehaviourTypeName.TEMPLATE_TIMESTAMP}.{TemplateType.TIMESTAMP}"

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
        start: datetime,
        end: datetime,
        precision: DatePrecisionType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.

        Args:
            precision (DatePrecisionType): Precision of the date values.
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
            start,
            end,
            template_filters,
            common_dependencies,
        )
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class.
        Generates date values from the template.
        """
        timestamps = self._generate_timestamp_values(size)

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.date_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to date
        timestamps = timestamps.astype("datetime64[D]")

        return timestamps


class ColumnGeneratorTimestampTemplateTime(ColumnGeneratorTimestampTemplate):
    """
    A subclass of ColumnGeneratorTemplate which represents a column generator using
    templates to generate time values.

    Attributes:
        precision (TimePrecisionType): Precision of the time values.
    """

    generator_type = f"{DescriptorTypeNames.COL_TIME}.{ColumnBehaviourTypeName.TEMPLATE_TIMESTAMP}.{TemplateType.TIMESTAMP}"

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
        start: datetime,
        end: datetime,
        precision: TimePrecisionType,
        template_filters: dict[str, list[int]] = None,
        common_dependencies: list[str] = None,
    ):
        """
        Constructor which extends the constructor
        :meth:`ColumnGeneratorTemplate.__init__` of the parent class.

        Args:
            precision (TimePrecisionType): Precision of the time values.
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
            start,
            end,
            template_filters,
            common_dependencies,
        )
        self.precision = precision

    def _generate_column_values(self, size: int):
        """
        Implements the abstract method :meth:`ColumnGenerator._generate_column_values`
        of the parent class.
        Generates time values from the template.
        """
        timestamps = self._generate_timestamp_values(size)

        # Coarse to a specified precision
        timestamps = timestamps.astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        # Coarse datetime values to time
        days = timestamps.astype("datetime64[D]")
        timestamps = (timestamps - days).astype(
            f"datetime64[{datetime_precision.time_precision_to_numpy_label(self.precision)}]"
        )

        return timestamps
