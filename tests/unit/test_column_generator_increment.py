from datetime import datetime

import numpy as np

from smart_generator.descriptor.enums import DatetimePrecisionType, DatePrecisionType
from smart_generator.generator.column_generator_increment import (
    ColumnGeneratorIncrementInt,
    ColumnGeneratorIncrementFloat,
    ColumnGeneratorIncrementDatetime,
    ColumnGeneratorIncrementDate,
    ColumnGeneratorIncrementTime,
)


class TestColumnGeneratorIncrementInt:
    def test_int_constructor(self, mocker):
        generator = ColumnGeneratorIncrementInt(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=0,
            step=1,
        )

        assert generator.start == 0
        assert generator.step == 1

        mocked_init = mocker.patch(
            "smart_generator.generator.column_generator_increment.ColumnGenerator.__init__",
            return_value=None,
        )
        mocked_init.called_once_with(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
        )

    def test_int_generate_column_values(self):
        generator = ColumnGeneratorIncrementInt(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=0,
            step=1,
        )

        values = generator._generate_column_values(3)

        assert np.array_equal(values, np.array([0, 1, 2]))

    def test_float_constructor(self, mocker):
        generator = ColumnGeneratorIncrementFloat(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=0.0,
            step=1.0,
            precision=2,
        )

        assert generator.start == 0.0
        assert generator.step == 1.0
        assert generator.precision == 2

        mocked_init = mocker.patch(
            "smart_generator.generator.column_generator_increment.ColumnGenerator.__init__",
            return_value=None,
        )
        mocked_init.called_once_with(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
        )

    def test_float_generate_column_values(self):
        generator = ColumnGeneratorIncrementFloat(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=0.0,
            step=1.0,
            precision=2,
        )

        values = generator._generate_column_values(3)

        assert np.array_equal(values, np.array([0.0, 1.0, 2.0]))

    def test_datetime_constructor(self, mocker):
        generator = ColumnGeneratorIncrementDatetime(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=3600,
            precision=DatetimePrecisionType.HOUR,
        )

        assert generator.start == datetime(2019, 1, 1, 0, 0, 0)
        assert generator.step == 3600
        assert generator.precision == DatetimePrecisionType.HOUR

        mocked_init = mocker.patch(
            "smart_generator.generator.column_generator_increment.ColumnGenerator.__init__",
            return_value=None,
        )
        mocked_init.called_once_with(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
        )

    def test_datetime_generate_column_values(self):
        generator = ColumnGeneratorIncrementDatetime(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=3600,
            precision=DatetimePrecisionType.HOUR,
        )

        values = generator._generate_column_values(3)

        assert np.array_equal(
            values,
            np.array(
                [
                    datetime(2019, 1, 1, 0, 0, 0),
                    datetime(2019, 1, 1, 1, 0, 0),
                    datetime(2019, 1, 1, 2, 0, 0),
                ]
            ),
        )

    def test_date_constructor(self, mocker):
        generator = ColumnGeneratorIncrementDate(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=3600 * 24,
            precision=DatePrecisionType.DAY,
        )

        assert generator.start == datetime(2019, 1, 1, 0, 0, 0)
        assert generator.step == 3600 * 24
        assert generator.precision == DatePrecisionType.DAY

        mocked_init = mocker.patch(
            "smart_generator.generator.column_generator_increment.ColumnGenerator.__init__",
            return_value=None,
        )
        mocked_init.called_once_with(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
        )

    def test_date_generate_column_values(self):
        generator = ColumnGeneratorIncrementDate(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=3600 * 24,
            precision=DatePrecisionType.DAY,
        )

        values = generator._generate_column_values(3)

        assert np.array_equal(
            values,
            np.array(["2019-01-01", "2019-01-02", "2019-01-03"], dtype="datetime64[D]"),
        )

    def test_time_constructor(self, mocker):
        generator = ColumnGeneratorIncrementTime(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=3600,
            precision=DatetimePrecisionType.HOUR,
        )

        assert generator.start == datetime(2019, 1, 1, 0, 0, 0)
        assert generator.step == 3600
        assert generator.precision == DatetimePrecisionType.HOUR

        mocked_init = mocker.patch(
            "smart_generator.generator.column_generator_increment.ColumnGenerator.__init__",
            return_value=None,
        )
        mocked_init.called_once_with(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
        )

    def test_time_generate_column_values(self):
        generator = ColumnGeneratorIncrementTime(
            id="id",
            name="name",
            seed_sequence=1,
            seed_column=1,
            visible=True,
            na_prob=0.0,
            start=datetime(2019, 1, 1, 0, 0, 0),
            step=60,
            precision=DatetimePrecisionType.MINUTE,
        )

        values = generator._generate_column_values(3)

        assert np.array_equal(
            values,
            np.array(
                ["1970-01-01T00:00", "1970-01-01T00:01", "1970-01-01T00:02"],
                dtype="datetime64[s]",
            ),
        )
