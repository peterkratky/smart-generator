import numpy as np
import pytest

from smart_generator import create_generator
from smart_generator import set_templates_provider
from smart_generator.templates.samples.sample_dataframe import provider


set_templates_provider(provider)


class TestGeneratorsTemplate:

    def test_label(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "gender",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "GENDER",
                    },
                }
            ],
        }
        table_generator = create_generator(data)
        table_generator.generate_next_batch(3, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["gender"].values, np.array(["male", "female", "male"])
        )

    def test_dependencies_simple(self):
        # country depends on continent

        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "continent",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CONTINENT",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "2",
                    "seed": 1,
                    "name": "country",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
            ],
        }
        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["continent"].values,
            np.array(["Europe", "Europe", "Europe", "Europe", "Europe"]),
        )
        assert np.array_equal(
            batch["country"].values,
            np.array(["Slovakia", "Slovakia", "Austria", "Slovakia", "Slovakia"]),
        )
        assert np.array_equal(batch["CONTINENT_ID_1"].values, np.array([2, 2, 2, 2, 2]))
        assert np.array_equal(
            batch["COUNTRY_ID_1"].values, np.array([21, 21, 20, 21, 21])
        )

    def test_dependencies_multiple(self):
        # firstname and lastname depend on both gender and country (which depends on continent)

        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "gender",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "GENDER",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "2",
                    "seed": 1,
                    "name": "firstname",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "FIRSTNAME",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "3",
                    "seed": 1,
                    "name": "lastname",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "LASTNAME",
                    },
                },
            ],
        }
        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["gender"].values,
            np.array(["male", "female", "male", "female", "male"]),
        )
        assert np.array_equal(
            batch["firstname"].values,
            np.array(["Peter", "Jana", "Markus", "Jana", "Peter"]),
        )
        assert np.array_equal(
            batch["lastname"].values,
            np.array(["Kratky", "Kratka", "Schmidth", "Kratka", "Kratky"]),
        )
        assert np.array_equal(
            batch["COUNTRY_ID_1"].values, np.array([21, 21, 20, 21, 21])
        )
        assert np.array_equal(batch["CONTINENT_ID_1"].values, np.array([2, 2, 2, 2, 2]))
        assert np.array_equal(batch["GENDER_ID_1"].values, np.array([0, 1, 0, 1, 0]))

    def test_dependencies_hierarchical(self):
        # road depends on city, which depends on country, which depends on continent

        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "continent",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CONTINENT",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "2",
                    "seed": 1,
                    "name": "country",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "3",
                    "seed": 1,
                    "name": "city",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "4",
                    "seed": 1,
                    "name": "road",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["continent"].values,
            np.array(["Europe", "Europe", "Europe", "Europe", "Europe"]),
        )
        assert np.array_equal(
            batch["country"].values,
            np.array(["Slovakia", "Slovakia", "Austria", "Slovakia", "Slovakia"]),
        )
        assert np.array_equal(
            batch["city"].values,
            np.array(["Presov", "Presov", "Vienna", "Presov", "Bratislava"]),
        )
        assert np.array_equal(
            batch["road"].values, np.array(["P2", "P2", "V1", "P2", "B1"])
        )
        assert np.array_equal(
            batch["COUNTRY_ID_1"].values, np.array([21, 21, 20, 21, 21])
        )
        assert np.array_equal(batch["CONTINENT_ID_1"].values, np.array([2, 2, 2, 2, 2]))
        assert np.array_equal(
            batch["CITY_ID_1"].values, np.array([203, 203, 200, 203, 202])
        )
        assert np.array_equal(
            batch["ROAD_ID_1"].values, np.array([2007, 2007, 2000, 2007, 2004])
        )

    def test_filter(self):
        data = {
            "name": "table1",
            "template_filters": {"country": [20]},
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "continent",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CONTINENT",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "2",
                    "seed": 1,
                    "name": "country",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "3",
                    "seed": 1,
                    "name": "city",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["continent"].values,
            np.array(["Europe", "Europe", "Europe", "Europe", "Europe"]),
        )
        assert np.array_equal(
            batch["country"].values,
            np.array(["Austria", "Austria", "Austria", "Austria", "Austria"]),
        )
        assert np.array_equal(
            batch["city"].values,
            np.array(["Vienna", "Linz", "Vienna", "Linz", "Vienna"]),
        )

    def test_filter_multiple(self):
        data = {
            "name": "table1",
            "template_filters": {"country": [10, 11], "city": [101, 102]},
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "1",
                    "seed": 1,
                    "name": "continent",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CONTINENT",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "2",
                    "seed": 1,
                    "name": "country",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "3",
                    "seed": 1,
                    "name": "city",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "4",
                    "seed": 1,
                    "name": "road",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["continent"].values,
            np.array(["America", "America", "America", "America", "America"]),
        )
        assert np.array_equal(
            batch["country"].values,
            np.array(["Canada", "US", "Canada", "US", "Canada"]),
        )
        assert np.array_equal(
            batch["city"].values,
            np.array(["Toronto", "Chicago", "Toronto", "Chicago", "Toronto"]),
        )

    def test_grouping_1(self):
        data = {
            "name": "table1",
            "template_filters": {
                # "country_id": [298, 214]
            },
            "common_dependencies": ["country"],
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "country1",
                    "seed": 1,
                    "name": "country1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "country2",
                    "seed": 2,
                    "name": "country2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "city1",
                    "seed": 1,
                    "name": "city1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "city2",
                    "seed": 2,
                    "name": "city2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "road1",
                    "seed": 1,
                    "name": "road1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "road2",
                    "seed": 2,
                    "name": "road2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(batch["country1"].values, batch["country2"].values)
        assert not np.array_equal(batch["city1"].values, batch["city2"].values)
        assert not np.array_equal(batch["road1"].values, batch["road2"].values)

    def test_grouping_2(self):
        data = {
            "name": "table1",
            "template_filters": {
                # "country_id": [298, 214]
            },
            "common_dependencies": ["city"],
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "country1",
                    "seed": 1,
                    "name": "country1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "country2",
                    "seed": 2,
                    "name": "country2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "city1",
                    "seed": 1,
                    "name": "city1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "city2",
                    "seed": 2,
                    "name": "city2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "road1",
                    "seed": 1,
                    "name": "road1",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "road2",
                    "seed": 2,
                    "name": "road2",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(batch["country1"].values, batch["country2"].values)
        assert np.array_equal(batch["city1"].values, batch["city2"].values)
        assert not np.array_equal(batch["road1"].values, batch["road2"].values)

    def test_geo(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "longitude",
                    "seed": 1,
                    "name": "longitude",
                    "precision": 5,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_GEOLOCATION",
                        "template": "POPULATION",
                        "coordinate_type": "LONGITUDE_WGS84",
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "latitude",
                    "seed": 1,
                    "name": "latitude",
                    "precision": 5,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_GEOLOCATION",
                        "template": "POPULATION",
                        "coordinate_type": "LATITUDE_WGS84",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "city",
                    "seed": 1,
                    "name": "city",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "CITY",
                    },
                },
                {
                    "descriptor_type": "COL_STRING",
                    "id": "road",
                    "seed": 1,
                    "name": "road",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "ROAD",
                    },
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["longitude"].values, np.array([20.07, 20.07, 20.00, 20.07, 20.04])
        )
        assert np.array_equal(
            batch["latitude"].values, np.array([-20.07, -20.07, -20.00, -20.07, -20.04])
        )
        assert np.array_equal(
            batch["city"].values,
            np.array(["Presov", "Presov", "Vienna", "Presov", "Bratislava"]),
        )
        assert np.array_equal(
            batch["road"].values, np.array(["P2", "P2", "V1", "P2", "B1"])
        )
        assert np.array_equal(
            batch["COUNTRY_ID_1"].values, np.array([21, 21, 20, 21, 21])
        )
        assert np.array_equal(batch["CONTINENT_ID_1"].values, np.array([2, 2, 2, 2, 2]))
        assert np.array_equal(
            batch["CITY_ID_1"].values, np.array([203, 203, 200, 203, 202])
        )
        assert np.array_equal(
            batch["ROAD_ID_1"].values, np.array([2007, 2007, 2000, 2007, 2004])
        )

    def test_label_expression(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "phone",
                    "seed": 1,
                    "name": "phone",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "PHONE_MOBILE_INT",
                    },
                }
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["phone"].values,
            np.array(
                [
                    "+421914177763",
                    "+421706690743",
                    "+4350008063",
                    "+421083778353",
                    "+421740681241",
                ]
            ),
        )
        assert np.array_equal(
            batch["COUNTRY_ID_1"].values, np.array([21, 21, 20, 21, 21])
        )

    def test_label_expression_based_on_other_columns(self):
        # email depends on firstname and lastname

        data = {
            "name": "table1",
            "descriptor_type": "TABLE",
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "5",
                    "seed": 1,
                    "name": "email",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "EMAIL",
                    },
                }
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["email"].values,
            np.array(
                [
                    "peter9@gmail.com",
                    "jana4@gmail.com",
                    "markus.schmidth@gmail.com",
                    "jana7@gmail.com",
                    "peter.kratky@gmail.com",
                ]
            ),
        )

    def test_timeseries(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_DATETIME",
                    "id": "1",
                    "seed": 1,
                    "name": "timestamp",
                    "visibility_type": "VISIBLE",
                    "precision": "HOUR",
                    "behaviour": {
                        "behaviour_type": "UNIFORM_DISTRIBUTION",
                        "min": "2022-01-01T20:00:00",
                        "max": "2023-01-01T22:00:00",
                    },
                },
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "2",
                    "seed": 1,
                    "name": "timeseries",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_TIMESERIES",
                        "template": "eshop_purchase",
                    },
                    "na_prob": 0.0,
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(5, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["timestamp"].values,
            np.array(
                [
                    "2022-07-07T16:00:00",
                    "2022-12-14T19:00:00",
                    "2022-02-23T11:00:00",
                    "2022-12-14T04:00:00",
                    "2022-04-25T16:00:00",
                ],
                dtype="datetime64[s]",
            ),
        )
        assert np.array_equal(
            batch["timeseries"].values, np.array([1.43, 0.57, 1.71, 1.43, 1.43])
        )

    def test_timeseries_no_datetime_column(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "COL_FLOAT",
                    "id": "2",
                    "seed": 1,
                    "name": "timeseries",
                    "precision": 2,
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_TIMESERIES",
                        "template": "eshop_purchase",
                    },
                    "na_prob": 0.0,
                }
            ],
        }

        table_generator = create_generator(data)

        with pytest.raises(Exception) as ex:
            table_generator.generate_next_batch(5, True, False)

    def test_sequences(self):
        data = {
            "name": "table1",
            "template_filters": {"country": [21, 20]},
            "descriptors": [
                {
                    "descriptor_type": "COL_STRING",
                    "id": "5",
                    "seed": 1,
                    "name": "country",
                    "visibility_type": "VISIBLE",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_LABEL",
                        "template": "COUNTRY",
                    },
                },
                {
                    "descriptor_type": "SEQUENCE",
                    "id": "456-456",
                    "seed": 1,
                    "name": "seq1",
                    "behaviour": {"behaviour_type": "LOOP", "iterations": 2},
                    "descriptors": [
                        {
                            "descriptor_type": "COL_STRING",
                            "id": "2",
                            "seed": 1,
                            "name": "firstname",
                            "visibility_type": "VISIBLE",
                            "behaviour": {
                                "behaviour_type": "TEMPLATE_LABEL",
                                "template": "FIRSTNAME",
                            },
                        },
                        {
                            "descriptor_type": "COL_STRING",
                            "id": "3",
                            "seed": 1,
                            "name": "lastname",
                            "visibility_type": "VISIBLE",
                            "behaviour": {
                                "behaviour_type": "TEMPLATE_LABEL",
                                "template": "LASTNAME",
                            },
                        },
                    ],
                },
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(6, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch["country"].values,
            np.array(
                ["Slovakia", "Slovakia", "Slovakia", "Slovakia", "Austria", "Austria"]
            ),
        )
        assert np.array_equal(
            batch["firstname"].values,
            np.array(["Peter", "Peter", "Jana", "Peter", "Monica", "Monica"]),
        )
        assert np.array_equal(
            batch["lastname"].values,
            np.array(["Kratky", "Kratky", "Kratka", "Kratky", "Schmidth", "Schmidth"]),
        )

    def test_sequence_templated(self):
        data = {
            "name": "table1",
            "descriptors": [
                {
                    "descriptor_type": "SEQUENCE",
                    "id": "456-456",
                    "seed": 1,
                    "name": "seq1",
                    "behaviour": {
                        "behaviour_type": "TEMPLATE_SEQUENCE",
                        "template": "ROUTE",
                    },
                    # "template_filters": {
                    #    "country_id": [30]
                    # },
                    "descriptors": [
                        {
                            "descriptor_type": "COL_FLOAT",
                            "id": "longitude1",
                            "seed": 1,
                            "name": "longitude1",
                            "visibility_type": "VISIBLE",
                            "precision": 5,
                            "behaviour": {
                                "behaviour_type": "TEMPLATE_GEOLOCATION",
                                "template": "ROUTE",
                                "coordinate_type": "LONGITUDE_WGS84",
                            },
                        },
                        {
                            "descriptor_type": "COL_FLOAT",
                            "id": "latitude1",
                            "seed": 1,
                            "name": "latitude1",
                            "visibility_type": "VISIBLE",
                            "precision": 5,
                            "behaviour": {
                                "behaviour_type": "TEMPLATE_GEOLOCATION",
                                "template": "ROUTE",
                                "coordinate_type": "LATITUDE_WGS84",
                            },
                        },
                    ],
                }
            ],
        }

        table_generator = create_generator(data)
        table_generator.generate_next_batch(8, True, False)
        batch = table_generator.get_batch_dataframe("NAME", True)

        assert np.array_equal(
            batch.iloc[:, 2].values, np.array([400, 400, 401, 401, 401, 300, 300, 300])
        )
        assert np.array_equal(
            batch["longitude1"].values,
            np.array([4.001, 4.002, 4.011, 4.012, 4.013, 3.001, 3.002, 3.003]),
        )
        assert np.array_equal(
            batch["latitude1"].values,
            np.array([-4.001, -4.002, -4.011, -4.012, -4.013, -3.001, -3.002, -3.003]),
        )
