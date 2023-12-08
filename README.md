# SmartGenerator 

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

SmartGenerator is an advanced Python package for generating test data.
It allows users to generate tabular data based on a description of structure and generation rules in JSON format. 
In its basics it provides generation of data based on specified distributions or other characteristics. 
The key feature of this library is the ability to generate data based on user-defined templates, providing a framework for creating realistic datasets.

You will find it beneficial if you need:
* to separate data description from the code and dynamically generate data based on the description in JSON format
* to generate realistic data where the values are aligned with each other (e.g. gender, country and name values in a row are consistent)
* to define more complex data generation rules (e.g. JOINed tables resulting in a single flat table)
* to generate big datasets (e.g. millions of rows) in reasonable time

## Installation

```bash
pip install smart_generator
```

## Usage

Create generator based on a descriptor as an object or as a JSON string. 

```python
from smart_generator import create_generator
from smart_generator.descriptor.table_descriptor import TableDescriptor

# define table_descriptor object or load it from JSON
# table_descriptor = { ... }

table_generator = create_generator(table_descriptor)
table_generator.generate_next_batch(8, True, False)
batch = table_generator.get_batch_dataframe("NAME", True)
```

```python
from smart_generator import create_generator_from_string

table_generator = create_generator_from_string(table_descriptor_str)
```

## Descriptors

The library provides a set of descriptors for defining the structure of the generated data.
When you define a descriptor for data generation, it is a hierarchical tree composed of three types of descriptors: `TableDescriptor`, `ColumnDescriptor` with multiple subtypes and `SequenceDescriptor`. For each descriptor you define a behaviour of how the data are generated.

Example:

```json
{
    "name": "table",
    "descriptors": [
        {
            "descriptor_type": "COL_INTEGER",
            "id": "1",
            "seed": 1,
            "name": "column-int",
            "visibility_type": "VISIBLE",
            "na_prob": 0.5,
            "behaviour": {
                "behaviour_type": "INCREMENT",
                "start": 10,
                "step": 2
            }
        },
        {
            "descriptor_type": "COL_FLOAT",
            "id": "2",
            "seed": 1,
            "name": "column-float",
            "precision": 2,
            "visibility_type": "VISIBLE",
            "behaviour": {
                "behaviour_type": "NORMAL_DISTRIBUTION",
                "mean": 0,
                "std_dev": 1
            }
        },
        {
                "descriptor_type": "COL_STRING",
                "id": "3",
                "seed": 1,
                "name": "column-string",
                "visibility_type": "VISIBLE",
                "behaviour": {
                    "behaviour_type": "WEIGHTS_TABLE",
                    "weights_table": [
                        {"key": "a", "value": 0.05},
                        {"key": "b", "value": 0.05},
                        {"key": "c", "value": 0.9}
                    ]
                }
        },
        {
                "descriptor_type": "COL_DATETIME",
                "id": "4",
                "seed": 1,
                "name": "column-datetime",
                "visibility_type": "VISIBLE",
                "precision": "MINUTE",
                "behaviour": {
                    "behaviour_type": "UNIFORM_DISTRIBUTION",
                    "min": "2020-01-01T00:00:00",
                    "max": "2021-01-02T00:00:00"
                }
        }
    ]
}
```

Typically, you will define a single `TableDescriptor` with multiple `ColumnDescriptor` objects for basic scenarios. 
But there is a possibility to define more levels to create nested structures using a `SequenceDescriptor`.

The tree structure of descriptors looks as follows:

```
TableDescriptor
├── ColumnDescriptor
├── ... (multiple ColumnDescriptors)
└── SequenceDescriptor
    ├── ColumnDescriptor
    ├── ... (multiple ColumnDescriptors)
    └── SequenceDescriptor
        ├── ...
```

### TableDescriptor

The `TableDescriptor` is the root of the descriptor tree. It defines the structure of the generated data and contains a list of `ColumnDescriptor` objects. 


| Property | Description                                                |
| --- |------------------------------------------------------------|
| name | Name of the table                                          |
| id | Unique identifier of the table                             |
| seed | Seed for generating values. Default value is 0.            |
| descriptors | List of `ColumnDescriptor` and `SequenceDescritor` objects |

### ColumnDescriptors

The `ColumnDescriptor` defines the structure of a single column in the generated data.

There are 6 types of `ColumnDescriptor` objects:

* `ColumnDescriptorInteger`
* `ColumnDescriptorFloat`
* `ColumnDescriptorString`
* `ColumnDescriptorDatetime`
* `ColumnDescriptorDate`
* `ColumnDescriptorTime`

Common properties for all of them:

| Property | Description                                                            |
| --- |------------------------------------------------------------------------|
| name | Name of the column                                                     |
| id | Unique identifier of the column                                        |
| seed | Seed for generating values. Default value is 1.                        |
| visibility_type | Visibility type of the column with possible values `VISIBLE`, `HIDDEN` |
| na_prob | Probability of generating NA values. Default value is 0.               |
| behavior | Behavior of the column.                                                |

`ColumnDescriptorFloat` additionally defines:

| Property  | Description                                       |
|-----------|---------------------------------------------------|
| precision | Number of decimal places of the generated numbers |

`ColumnDescriptorDatetime`, `ColumnDescriptorDate` and `ColumnDescriptorTime` additionally define:

| Property | Description                                                                                                            |
| --- |------------------------------------------------------------------------------------------------------------------------|
| precision | Precision of the column with possible values `YEAR`, `MONTH`, `WEEK`, `DAY`, `HOUR`, `MINUTE`, `SECOND`, `MILLISECOND` |

### SequenceDescriptor

The `SequenceDescriptor` defines a sequence or subtable of the generated data. It contains a list of `ColumnDescriptor` objects and `SequenceDescriptor` objects.

| Property | Description                                                |
| --- |------------------------------------------------------------|
| name | Name of the sequence                                       |
| id | Unique identifier of the sequence                          |
| seed | Seed for generating values. Default value is 1.            |
| descriptors | List of `ColumnDescriptor` and `SequenceDescritor` objects |
| behavior | Behavior of the sequence.                                  |

## Behaviors

The `behavior` property of `ColumnDescriptor` and `SequenceDescriptor` defines the behavior of the generation process of the column or sequence.

### Increment

The `Increment` behavior generates values based on the specified start value and step.

Compatible with `ColumnDescriptorInteger`, `ColumnDescriptorFloat`, `ColumnDescriptorDatetime`, `ColumnDescriptorDate` and `ColumnDescriptorTime`.

| Property | Description                                                                                                                                                              |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| start | Start value of the generated values. It is a number in case of `Integer` or `Float` columns. It is a corresponding type in case of `Datetime`, `Date` or `Time` columns. |
| step | Step for generating next value. For `Datetime`, `Date` and `Time` columns it is a number representing milliseconds.                                                      |

### Unique

The `Unique` behavior generates unique values within a specified range.

Compatible with `ColumnDescriptorInteger`, `ColumnDescriptorFloat`.

| Property | Description                                              |
| --- |----------------------------------------------------------|
| min | Minimum value of the range to generate from.             |
| max | Maximum value of the range to generate from.             |

### Uniform distribution

The `UniformDistribution` behavior generates values based on the uniform distribution.

Compatible with `ColumnDescriptorInteger`, `ColumnDescriptorFloat`, `ColumnDescriptorDatetime`, `ColumnDescriptorDate` and `ColumnDescriptorTime`.

| Property | Description                                                                                                                                                                      |
| --- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| min | Minimum value of the range to generate from. It is a number in case of `Integer` or `Float` columns. It is a corresponding type in case of `Datetime`, `Date` or `Time` columns. |
| max | Maximum value of the range to generate from. It is a number in case of `Integer` or `Float` columns. It is a corresponding type in case of `Datetime`, `Date` or `Time` columns. |

### Normal distribution

The `NormalDistribution` behavior generates values based on the normal distribution.

Compatible with `ColumnDescriptorInteger`, `ColumnDescriptorFloat`.

| Property | Description                                                                                                                                                                      |
| --- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mean | Mean parameter of the distribution.                                                                                                                                                  |
| std_dev | Standard deviation of the distribution.                                                                                                                                          |

### Exponential distribution

The `ExponentialDistribution` behavior generates values based on the exponential distribution.

Compatible with `ColumnDescriptorInteger`, `ColumnDescriptorFloat`.

| Property | Description                                                                         |
| --- |-------------------------------------------------------------------------------------|
| scale | Scale parameter of the distribution. It is the same as reverse of lambda parameter. |

### Weights table

The `WeightsTable` behavior generates values based on the weights table.

Compatible with `ColumnDescriptorString`, `ColumnDescriptorInteger`, `ColumnDescriptorFloat`, `ColumnDescriptorDatetime`, `ColumnDescriptorDate` and `ColumnDescriptorTime`.

| Property | Description                                                                                                                                                                                                        |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| weights_table | List of `Entry` objects, such as `{"key": some_key, "value": number}`. The key is a value to generate and the value is a weight of generating the value. The sum of all weights does not need to be 1. Key is a corresponding type based on the column type. |

### Template label

The `TemplateLabel` behavior generates labels based on the template.

Compatible with `ColumnDescriptorString`.

| Property | Description                                                                                                                                                                                                        |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| template | Name of the template for generating labels. |
| template_filters | Dictionary representing filters for the template. |

### Template Geo Location

The `TemplateGeoLocation` behavior generates geo locations based on the template.

Compatible with `ColumnDescriptorInteger` and `ColumnDescriptorFloat`.

| Property | Description                                                                                                                                                                                                        |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| template | Name of the template for generating geo locations. |
| coordinate_type | Type of the coordinate to generate. Possible values are `LATITUDE_WGS84` and `LONGITUDE_WGS84`. |
| template_filters | Dictionary representing filters for the template. |

### Template Timestamp

The `TemplateTimestamp` behavior generates timestamps based on the template. This behavior is useful for generating random timestamps from a specified range and the template determines the probability of generating a timestamp.

Compatible with `ColumnDescriptorDatetime`, `ColumnDescriptorDate` and `ColumnDescriptorTime`.

| Property | Description                                     |
| --- |-------------------------------------------------|
| template | Name of the template for generating timestamps. |
| start | Start value of the range to generate from.      |
| end | End value of the range to generate from.        |
| template_filters | Dictionary representing filters for the template. |

### Template Timeseries

The `TemplateTimeseries` behavior generates timeseries based on the template. This behavior is useful for generating timeseries values. When a column with this behaviour is used, it also requires a column `ColumnDescriptorDatetime`, `ColumnDescriptorDate` or `ColumnDescriptorTime` in the same table/sequence. It automatically pairs with the first column of such a type in the table/sequence.

Compatible with `ColumnDescriptorInteger` and `ColumnDescriptorFloat`.

| Property | Description                                     |
| --- |-------------------------------------------------|
| template | Name of the template for generating timeseries. |
| template_filters | Dictionary representing filters for the template. |

## Template Providers

Template providers are an extension of the library that allows users to define their own templates for generating data.

### Built-in Faker provider

The library provides a built-in template provider based on the [Faker](https://faker.readthedocs.io/en/master/) library, so if you install Faker, you can use all the templates provided by Faker.

```commandline
pip install Faker
```

Set the template provider:

```python
from smart_generator import add_templates_provider
from smart_generator.templates.samples.sample_faker import provider as faker_provider

add_templates_provider(faker_provider)
```

Example of an input descriptor using Faker to generate names:

```json
{
    "name": "table",
    "descriptors": [
        {
            "descriptor_type": "COL_STRING",
            "id": "1",
            "seed": 1,
            "name": "column-string",
            "visibility_type": "VISIBLE",
            "behaviour": {
                "behaviour_type": "TEMPLATE_LABEL",
                "template": "FIRST_NAME"
            }
        }
    ]
}
```

### Adding custom templates

To add your custom templates, you can you either `TemplatesProviderFromDataframe` or `TemplatesProviderFromSql` depending on your source of data templates.

#### Label templates

As an example, consider these 4 tables:

* gender - with columns `gender_id`, `label` and `weight`
* country - with columns `country_id`, `label` and `population`
* city - with columns `city_id`, `country_id`, `label` and `population`
* name - with columns `gender_id`, `country_id`, `label` and `weight`

You can then setup the template provider in which you define the tables and their relationships:

```python
from smart_generator.templates.templates_provider_sql import TemplatesProviderFromSql
from smart_generator.templates.template_table import TemplateTable

connection_string = 'connection_string_to_your_database'

provider = TemplatesProviderFromSql(connection_string)

provider.add_table(TemplateTable("gender", "gender", id_column="gender_id"))
provider.add_table(TemplateTable("country", "country", id_column="country_id", weight_column="population"))
provider.add_table(
    TemplateTable("city", "city", id_column="city_id", weight_column="population", dependency_templates=["country"]))
provider.add_table(TemplateTable("name", "name", id_column=None, dependency_templates=["gender", "country"]))
```

#### Geo location templates

As an example, consider a table with geo locations:

* geo_location - with columns `longitude`, `latitude` and `population`

```python
from smart_generator.templates.template_table import TemplateGeoLocationTable

provider.add_table(TemplateGeoLocationTable("population", "geo_location", "longitude", "latitude", weight_column="population", dependency_templates=["country"]))
```

#### Timestamp templates

As an example, consider a table with timestamps:

* events_telco - with columns `timestamp`, `sms`, `call`

```python
from smart_generator.templates.template_table import TemplateTimestampTable, TimeseriesUnit

provider.add_table(TemplateTimestampTable("telco_call", "events_telco", TimeseriesUnit.YEAR, TimeseriesUnit.HOUR, weight_column="calls"))
provider.add_table(TemplateTimestampTable("telco_sms", "events_telco", TimeseriesUnit.YEAR, TimeseriesUnit.HOUR, weight_column="sms"))
```

The `timestamp` column is not in a standard format, but rather an encoded timestamp. We provide an encoding function used to encode timestamps to a generic number representing a certain point of time in the timeseries. It takes into consideration day of week, so this way we can encode, for example, weekend or Monday morning data regardless of the year. This help to generate timestamps and timeseries from templates in an arbitrary time frame.

```python
from smart_generator.helpers.timeseries_coding import encode_timestamp, TimeseriesUnit
from datetime import datetime

print(encode_timestamp(datetime(2024, 1, 1), TimeseriesUnit.YEAR,
                       TimeseriesUnit.HOUR))  # returns 0 - this day is Monday and it is also aligned with the start of the year
print(encode_timestamp(datetime(2020, 1, 1), TimeseriesUnit.YEAR,
                       TimeseriesUnit.HOUR))  # returns 48 - this day is Wednesday
```

#### Timeseries templates

This is similar to the timestamp templates, but it is used for generating timeseries values.

The same table as in the timestamp templates example can be reused.

## Products using SmartGenerator

* [Data4Test](https://data4test.com) - a free online tool for generating test data based on SmartGenerator.