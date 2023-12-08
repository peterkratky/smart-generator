import marshmallow_dataclass
import numpy as np
from numpy import int64

from smart_generator.descriptor.table_descriptor import TableDescriptor
from smart_generator import create_table_generator, create_generator


class TestGeneratorsBasic:
    def test_basic_generators_int(self):
        data_int = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "visibility_type": "VISIBLE",
                    "na_prob": 0.5,
                    "behaviour": {
                        "behaviour_type": "INCREMENT",
                        "start": 10,
                        "step": 2,
                    },
                },
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "2",
                    "seed": 2,
                    "name": "column2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {"behaviour_type": "UNIQUE", "min": 1, "max": 2000000},
                },
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "3",
                    "seed": 1,
                    "name": "column3",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "NORMAL_DISTRIBUTION",
                        "mean": 0,
                        "std_dev": 1,
                    },
                },
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "4",
                    "seed": 1,
                    "name": "column4",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "EXPONENTIAL_DISTRIBUTION",
                        "scale": 10,
                    },
                },
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "5",
                    "seed": 2,
                    "name": "column5",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": 10,
                        "max": 100,
                    },
                },
                {
                    "descriptor_type": "COL_INTEGER",
                    "id": "6",
                    "seed": 1,
                    "name": "column6",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": 1, "value": 0.05},
                            {"key": 2, "value": 0.05},
                            {"key": 3, "value": 0.9},
                        ],
                    },
                },
            ],
        }

        table_generator = create_generator(data_int)
        table_generator.generate_next_batch(10, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 10
        assert batch.shape[1] == 6

        assert np.array_equal(
            batch["column1"].values,
            np.array([10, 12, None, 16, None, None, 22, None, 26, None], dtype=object),
        )
        assert np.array_equal(
            batch["column2"].values,
            np.array(
                [
                    1200201,
                    596981,
                    827625,
                    218611,
                    1675143,
                    1628448,
                    523222,
                    183832,
                    902539,
                    669766,
                ]
            ),
        )
        assert np.array_equal(
            batch["column3"].values, np.array([0, 0, 0, -1, 0, 0, 0, 0, 0, 0])
        )
        assert np.array_equal(
            batch["column4"].values, np.array([10, 3, 53, 3, 1, 17, 4, 5, 0, 7])
        )
        assert np.array_equal(
            batch["column5"].values,
            np.array([85, 33, 19, 36, 47, 83, 50, 18, 40, 64], dtype=int64),
        )
        assert np.array_equal(
            batch["column6"].values, np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 1])
        )

    def test_basic_generators_float(self):
        data_float = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "precision": 2,
                    "na_prob": 0.5,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "INCREMENT",
                        "start": 10,
                        "step": 2,
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "2",
                    "seed": 2,
                    "name": "column2",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {"behaviour_type": "UNIQUE", "min": 1, "max": 2000000},
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "3",
                    "seed": 1,
                    "name": "column3",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "NORMAL_DISTRIBUTION",
                        "mean": 0,
                        "std_dev": 1,
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "4",
                    "seed": 1,
                    "name": "column4",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "EXPONENTIAL_DISTRIBUTION",
                        "scale": 10,
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "5",
                    "seed": 2,
                    "name": "column5",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": 10,
                        "max": 100,
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "6",
                    "seed": 1,
                    "name": "column6",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": 1.1, "value": 0.05},
                            {"key": 2.2, "value": 0.05},
                            {"key": 3.3, "value": 0.9},
                        ],
                    },
                },
            ],
        }

        table_generator = create_generator(data_float)
        table_generator.generate_next_batch(10, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 10
        assert batch.shape[1] == 6

        assert np.array_equal(
            batch["column1"].values,
            np.array(
                [10.0, 12.0, None, 16.0, None, None, 22.0, None, 26.0, None],
                dtype=object,
            ),
        )
        assert np.array_equal(
            batch["column2"].values,
            np.array(
                [
                    1200201.0,
                    596981.0,
                    827625.0,
                    218611.0,
                    1675143.0,
                    1628448.0,
                    523222.0,
                    183832.0,
                    902539.0,
                    669766.0,
                ]
            ),
        )
        assert np.array_equal(
            batch["column3"].values,
            np.array([0.35, 0.82, 0.33, -1.3, 0.91, 0.45, -0.54, 0.58, 0.36, 0.29]),
        )
        assert np.array_equal(
            batch["column4"].values,
            np.array([10.73, 3.08, 53.75, 3.66, 1.15, 18.0, 4.99, 5.51, 0.3, 7.64]),
        )
        assert np.array_equal(
            batch["column5"].values,
            np.array(
                [33.55, 36.86, 83.28, 18.27, 64.01, 75.57, 26.91, 14.96, 34.75, 69.17]
            ),
        )
        assert np.array_equal(
            batch["column6"].values,
            np.array([3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 1.1]),
        )

    def test_basic_generators_string(self):
        data_string = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": "a", "value": 0.2},
                            {"key": "b", "value": 0.3},
                            {"key": "c", "value": 0.5},
                        ],
                    },
                }
            ],
        }

        table_generator = create_generator(data_string)
        table_generator.generate_next_batch(10, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 10
        assert batch.shape[1] == 1

        assert np.array_equal(
            batch["column1"].values,
            np.array(["c", "c", "a", "c", "b", "b", "c", "b", "c", "a"]),
        )

    def test_basic_generators_datetime(self):
        data_datetime = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_DATETIME",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": "2020-01-01T01:10:33", "value": 0.3},
                            {"key": "2020-01-01T02:20:33", "value": 0.3},
                            {"key": "2020-01-01T03:30:33", "value": 0.4},
                        ],
                    },
                },
                {
                    "descriptor_type": "COL_DATETIME",
                    "id": "2",
                    "seed": 1,
                    "name": "column2",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": "2020-01-01T00:00:00",
                        "max": "2021-01-02T00:00:00",
                    },
                },
                {
                    "descriptor_type": "COL_DATETIME",
                    "id": "3",
                    "seed": 1,
                    "name": "column3",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "INCREMENT",
                        "start": "2020-01-01T00:00:00",
                        "step": 60,
                    },
                },
            ],
        }

        table_generator = create_generator(data_datetime)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 5
        assert batch.shape[1] == 3

        assert np.array_equal(
            batch["column1"].values,
            np.array(
                [
                    "2020-01-01T02:20:00",
                    "2020-01-01T03:30:00",
                    "2020-01-01T01:10:00",
                    "2020-01-01T03:30:00",
                    "2020-01-01T02:20:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column2"].values,
            np.array(
                [
                    "2020-07-06T20:07:00",
                    "2020-12-14T19:41:00",
                    "2020-02-22T21:45:00",
                    "2020-12-14T03:42:00",
                    "2020-04-24T10:36:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column3"].values,
            np.array(
                [
                    "2020-01-01T00:00:00",
                    "2020-01-01T00:01:00",
                    "2020-01-01T00:02:00",
                    "2020-01-01T00:03:00",
                    "2020-01-01T00:04:00",
                ],
                dtype="datetime64[s]",
            ),
        )

    def test_basic_generators_date(self):
        data_date = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_DATE",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "visibility_type": "VISIBLE",
                    "precision": "DAY",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": "2020-01-01T01:10:33", "value": 0.3},
                            {"key": "2020-01-01T02:20:33", "value": 0.3},
                            {"key": "2020-01-01T03:30:33", "value": 0.4},
                        ],
                    },
                },
                {
                    "descriptor_type": "COL_DATE",
                    "id": "2",
                    "seed": 1,
                    "name": "column2",
                    "visibility_type": "VISIBLE",
                    "precision": "DAY",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": "2020-01-01T00:00:00",
                        "max": "2021-01-10T00:00:00",
                    },
                },
                {
                    "descriptor_type": "COL_DATE",
                    "id": "3",
                    "seed": 1,
                    "name": "column3",
                    "visibility_type": "VISIBLE",
                    "precision": "DAY",
                    "behaviour": {
                        "behaviour_type": "INCREMENT",
                        "start": "2020-01-01T00:00:00",
                        "step": 3600 * 24,
                    },
                },
            ],
        }

        table_generator = create_generator(data_date)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 5
        assert batch.shape[1] == 3

        assert np.array_equal(
            batch["column1"].values,
            np.array(
                [
                    "2020-01-01T00:00:00",
                    "2020-01-01T00:00:00",
                    "2020-01-01T00:00:00",
                    "2020-01-01T00:00:00",
                    "2020-01-01T00:00:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column2"].values,
            np.array(
                [
                    "2020-07-10T00:00:00",
                    "2020-12-22T00:00:00",
                    "2020-02-24T00:00:00",
                    "2020-12-21T00:00:00",
                    "2020-04-26T00:00:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column3"].values,
            np.array(
                [
                    "2020-01-01T00:00:00",
                    "2020-01-02T00:00:00",
                    "2020-01-03T00:00:00",
                    "2020-01-04T00:00:00",
                    "2020-01-05T00:00:00",
                ],
                dtype="datetime64[s]",
            ),
        )

    def test_basic_generators_time(self):
        data_time = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_TIME",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "WEIGHTS_TABLE",
                        "weights_table": [
                            {"key": "2020-01-01T01:10:33", "value": 1},
                            {"key": "2020-01-01T02:20:33", "value": 2},
                            {"key": "2020-01-01T03:30:33", "value": 3},
                        ],
                    },
                },
                {
                    "descriptor_type": "COL_TIME",
                    "id": "2",
                    "seed": 1,
                    "name": "column2",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": "1970-01-01T20:00:00",
                        "max": "1970-01-01T22:00:00",
                    },
                },
                {
                    "descriptor_type": "COL_TIME",
                    "id": "3",
                    "seed": 1,
                    "name": "column3",
                    "visibility_type": "VISIBLE",
                    "precision": "MINUTE",
                    "behaviour": {
                        "behaviour_type": "INCREMENT",
                        "start": "2020-01-01T00:00:00",
                        "step": 60,
                    },
                },
            ],
        }

        table_generator = create_generator(data_time)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert batch.shape[0] == 5
        assert batch.shape[1] == 3

        assert np.array_equal(
            batch["column1"].values,
            np.array(
                [
                    "1970-01-01T03:30:00",
                    "1970-01-01T03:30:00",
                    "1970-01-01T01:10:00",
                    "1970-01-01T03:30:00",
                    "1970-01-01T02:20:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column2"].values,
            np.array(
                [
                    "1970-01-01T21:01:00",
                    "1970-01-01T21:54:00",
                    "1970-01-01T20:17:00",
                    "1970-01-01T21:53:00",
                    "1970-01-01T20:37:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["column3"].values,
            np.array(
                [
                    "1970-01-01T00:00:00",
                    "1970-01-01T00:01:00",
                    "1970-01-01T00:02:00",
                    "1970-01-01T00:03:00",
                    "1970-01-01T00:04:00",
                ],
                dtype="datetime64[s]",
            ),
        )

    def test_sequences(self):
        data_sequence = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "1",
                    "seed": 1,
                    "name": "column1",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {"behaviour_type": "INCREMENT", "start": 1, "step": 1},
                },
                {
                    "descriptor_type": "SEQUENCE",
                    "id": "456-456",
                    "seed": 1,
                    "name": "seq",
                    "behaviour": {"behaviour_type": "LOOP", "iterations": 2},
                    "descriptors": [
                        {
                            "descriptor_type": "COL_INTEGER",
                            "id": "2",
                            "seed": 2,
                            "name": "column2",
                            "visibility_type": "VISIBLE",
                            "behaviour": {
                                "behaviour_type": "UNIQUE",
                                "min": 1,
                                "max": 10,
                            },
                        },
                        {
                            "descriptor_type": "SEQUENCE",
                            "id": "456-456",
                            "seed": 1,
                            "name": "seq",
                            "behaviour": {"behaviour_type": "LOOP", "iterations": 2},
                            "descriptors": [
                                {
                                    "descriptor_type": "COL_INTEGER",
                                    "id": "3",
                                    "seed": 3,
                                    "name": "column3",
                                    "visibility_type": "VISIBLE",
                                    "behaviour": {
                                        "behaviour_type": "UNIQUE",
                                        "min": 100,
                                        "max": 200,
                                    },
                                }
                            ],
                        },
                    ],
                },
            ],
        }

        table_generator = create_generator(data_sequence)
        table_generator.generate_next_batch(8, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["column1"].values, np.array([1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0])
        )
        assert np.array_equal(
            batch["column2"].values, np.array([1, 1, 7, 7, 2, 2, 9, 9])
        )
        assert np.array_equal(
            batch["column3"].values, np.array([171, 194, 150, 194, 108, 196, 128, 160])
        )
