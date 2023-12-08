import json
import logging

import marshmallow_dataclass

from smart_generator.descriptor.table_descriptor import TableDescriptor
from smart_generator.generator.table_generator import TableGenerator
from smart_generator.generator_factory import create_table_generator
from smart_generator.templates import set_templates_provider


def create_generator(data: dict) -> TableGenerator:
    try:
        obj = marshmallow_dataclass.class_schema(TableDescriptor)().load(data)
        return create_table_generator(obj)
    except Exception as e1:
        logging.warning("Descriptor could not be parsed as a table: " + str(e1))
        try:
            table_data = {"name": "table", "descriptors": [data]}
            obj = marshmallow_dataclass.class_schema(TableDescriptor)().load(table_data)
            return create_table_generator(obj)
        except Exception as e2:
            logging.warning("Descriptor could not be parsed as a column: " + str(e2))
            raise ValueError(
                "Descriptor could not be parsed. See the logs for more details."
            )


def create_generator_from_string(data: str) -> TableGenerator:
    return create_generator(json.loads(data))
