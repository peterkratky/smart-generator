import re
import unicodedata

import pandas

from smart_generator.templates.template_table import (TemplateGeoLocationTable,
                                                      TemplateTable,
                                                      TemplateTimestampTable,
                                                      TimeseriesUnit)
from smart_generator.templates.templates_provider_dataframe import \
    TemplatesProviderFromDataframe


def to_email_chars(input):
    input = (
        unicodedata.normalize("NFKD", input)
        .encode("ASCII", "ignore")
        .decode("utf-8")
        .lower()
    )
    return re.sub(r"[^0-9a-zA-Z_-]", "", input)


provider = TemplatesProviderFromDataframe()

t_gender = pandas.DataFrame()
t_gender["gender_id"] = [0, 1]
t_gender["weight"] = [0.55, 0.45]
t_gender["label"] = ["male", "female"]

t_firstname = pandas.DataFrame()
t_firstname["gender_id"] = [0, 1, 0, 1, 0, 1, 0, 1]
t_firstname["country_id"] = [10, 10, 11, 11, 20, 20, 21, 21]
t_firstname["weight"] = [10, 9, 5, 4, 7, 1, 10, 10]
t_firstname["label"] = [
    "Fredy",
    "Julie",
    "Eric",
    "Jane",
    "Markus",
    "Monica",
    "Peter",
    "Jana",
]

t_lastname = pandas.DataFrame()
t_lastname["gender_id"] = [0, 1, 0, 1, 0, 1, 0, 1]
t_lastname["country_id"] = [10, 10, 11, 11, 20, 20, 21, 21]
t_lastname["weight"] = [7, 2, 8, 4, 7, 4, 6, 10]
t_lastname["label"] = [
    "Smith",
    "Smith",
    "Wright",
    "Wright",
    "Schmidth",
    "Schmidth",
    "Kratky",
    "Kratka",
]

t_continent = pandas.DataFrame()
t_continent["continent_id"] = [1, 2]
t_continent["weight"] = [1, 10]
t_continent["label"] = ["America", "Europe"]

t_country = pandas.DataFrame()
t_country["country_id"] = [10, 11, 20, 21]
t_country["continent_id"] = [1, 1, 2, 2]
t_country["weight"] = [9, 3, 4, 10]
t_country["label"] = ["Canada", "US", "Austria", "Slovakia"]

t_city = pandas.DataFrame()
t_city["city_id"] = [100, 101, 102, 103, 200, 201, 202, 203]
t_city["country_id"] = [10, 10, 11, 11, 20, 20, 21, 21]
t_city["weight"] = [7, 2, 8, 4, 7, 4, 6, 10]
t_city["label"] = [
    "Montreal",
    "Toronto",
    "Chicago",
    "New York",
    "Vienna",
    "Linz",
    "Bratislava",
    "Presov",
]

t_road = pandas.DataFrame()
t_road["road_id"] = [
    1000,
    1001,
    1002,
    1003,
    1004,
    1005,
    1006,
    1007,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
]
t_road["city_id"] = [
    100,
    100,
    101,
    101,
    102,
    102,
    103,
    103,
    200,
    200,
    201,
    201,
    202,
    202,
    203,
    203,
]
t_road["country_id"] = [10, 10, 10, 10, 11, 11, 11, 11, 20, 20, 20, 20, 21, 21, 21, 21]
t_road["weight"] = [10, 9, 5, 4, 7, 1, 10, 10, 7, 2, 8, 4, 7, 4, 6, 10]
t_road["label"] = [
    "M1",
    "M2",
    "T1",
    "T2",
    "CH1",
    "CH2",
    "NY1",
    "NY2",
    "V1",
    "V2",
    "L1",
    "L2",
    "B1",
    "B2",
    "P1",
    "P2",
]

t_geolocation = pandas.DataFrame()
t_geolocation["road_id"] = [
    1000,
    1001,
    1002,
    1003,
    1004,
    1005,
    1006,
    1007,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
]
t_geolocation["city_id"] = [
    100,
    100,
    101,
    101,
    102,
    102,
    103,
    103,
    200,
    200,
    201,
    201,
    202,
    202,
    203,
    203,
]
t_geolocation["country_id"] = [
    10,
    10,
    10,
    10,
    11,
    11,
    11,
    11,
    20,
    20,
    20,
    20,
    21,
    21,
    21,
    21,
]
t_geolocation["continent_id"] = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]
t_geolocation["weight"] = [10, 9, 5, 4, 7, 1, 10, 10, 7, 2, 8, 4, 7, 4, 6, 10]
t_geolocation["longitude"] = [
    10.00,
    10.01,
    10.02,
    10.03,
    10.04,
    10.05,
    10.06,
    10.07,
    20.00,
    20.01,
    20.02,
    20.03,
    20.04,
    20.05,
    20.06,
    20.07,
]
t_geolocation["latitude"] = [
    -10.00,
    -10.01,
    -10.02,
    -10.03,
    -10.04,
    -10.05,
    -10.06,
    -10.07,
    -20.00,
    -20.01,
    -20.02,
    -20.03,
    -20.04,
    -20.05,
    -20.06,
    -20.07,
]

t_phone_mobile_int = pandas.DataFrame()
t_phone_mobile_int["country_id"] = [10, 11, 20, 21]
t_phone_mobile_int["weight"] = [1, 1, 1, 1]
t_phone_mobile_int["label"] = ["\+1\d{10}", "\+1\d{10}", "\+43\d{8}", "\+421\d{9}"]

t_email = pandas.DataFrame()
t_email["weight"] = [1, 1]
t_email["label"] = [
    "{{to_email_chars(firstname)}}\.{{to_email_chars(lastname)}}@gmail\.com",
    "{{to_email_chars(firstname)}}\d{1,3}@gmail\.com",
]

t_eshop_purchase = pandas.DataFrame()
t_eshop_purchase["timestamp"] = range(8904)
t_eshop_purchase["coef"] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] * 1484

t_route = pandas.DataFrame()
t_route["route_id"] = [
    100,
    100,
    100,
    101,
    101,
    200,
    200,
    201,
    201,
    201,
    300,
    300,
    300,
    301,
    301,
    400,
    400,
    401,
    401,
    401,
]
t_route["country_id"] = [
    10,
    10,
    10,
    10,
    10,
    11,
    11,
    11,
    11,
    11,
    20,
    20,
    20,
    20,
    20,
    21,
    21,
    21,
    21,
    21,
]
t_route["weight"] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
t_route["longitude"] = [
    1.001,
    1.002,
    1.003,
    1.011,
    1.012,
    2.001,
    2.002,
    2.011,
    2.012,
    2.013,
    3.001,
    3.002,
    3.003,
    3.011,
    3.012,
    4.001,
    4.002,
    4.011,
    4.012,
    4.013,
]
t_route["latitude"] = [
    -1.001,
    -1.002,
    -1.003,
    -1.011,
    -1.012,
    -2.001,
    -2.002,
    -2.011,
    -2.012,
    -2.013,
    -3.001,
    -3.002,
    -3.003,
    -3.011,
    -3.012,
    -4.001,
    -4.002,
    -4.011,
    -4.012,
    -4.013,
]

provider.add_table(TemplateTable("gender", "gender", id_column="gender_id"))
provider.add_dataframe("gender", t_gender)

provider.add_table(
    TemplateTable(
        "firstname",
        "firstname",
        id_column=None,
        dependency_templates=["gender", "country"],
    )
)
provider.add_dataframe("firstname", t_firstname)

provider.add_table(
    TemplateTable(
        "lastname",
        "lastname",
        id_column=None,
        dependency_templates=["gender", "country"],
    )
)
provider.add_dataframe("lastname", t_lastname)

provider.add_table(TemplateTable("continent", "continent", id_column="continent_id"))
provider.add_dataframe("continent", t_continent)

provider.add_table(
    TemplateTable(
        "country", "country", id_column="country_id", dependency_templates=["continent"]
    )
)
provider.add_dataframe("country", t_country)

provider.add_table(
    TemplateTable("city", "city", id_column="city_id", dependency_templates=["country"])
)
provider.add_dataframe("city", t_city)

provider.add_table(
    TemplateTable(
        "road",
        "road",
        id_column="road_id",
        dependency_templates=["country"],
        weak_dependency_templates=["city"],
    )
)
provider.add_dataframe("road", t_road)

provider.add_table(
    TemplateGeoLocationTable(
        "population",
        "geo_location",
        "longitude",
        "latitude",
        dependency_templates=[],
        weak_dependency_templates=["road", "city", "country", "continent"],
    )
)
provider.add_dataframe("population", t_geolocation)

provider.add_table(
    TemplateTable(
        "phone_mobile_int",
        "phone_mobile_int",
        dependency_templates=["country"],
        using_expressions=True,
    )
)
provider.add_dataframe("phone_mobile_int", t_phone_mobile_int)

provider.add_table(
    TemplateTable(
        "email",
        "email",
        id_column=None,
        dependency_templates=[],
        label_dependency_templates=["firstname", "lastname"],
        using_expressions=True,
    )
)
provider.add_dataframe("email", t_email)

provider.add_table(
    TemplateTimestampTable(
        "eshop_purchase",
        "events_purchase",
        TimeseriesUnit.YEAR,
        TimeseriesUnit.HOUR,
        weight_column="coef",
    )
)
provider.add_dataframe("eshop_purchase", t_eshop_purchase)

provider.add_table(
    TemplateGeoLocationTable(
        "route",
        "route",
        "longitude",
        "latitude",
        id_column="route_id",
        dependency_templates=["country"],
        weak_dependency_templates=[],
        randomize=False,
    )
)
provider.add_dataframe("route", t_route)

provider.add_function(to_email_chars)
