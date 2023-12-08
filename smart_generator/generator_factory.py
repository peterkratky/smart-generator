import uuid
from typing import Union

from .descriptor.descriptor import Descriptor
from .descriptor.enums import ColumnVisibilityType
from .descriptor.sequence import Sequence
from .descriptor.table_descriptor import TableDescriptor
from .generator.column_generator_exponential_distribution import (
    ColumnGeneratorExponentialDistributionFloat,
    ColumnGeneratorExponentialDistributionInt)
from .generator.column_generator_increment import (
    ColumnGeneratorIncrementDate, ColumnGeneratorIncrementDatetime,
    ColumnGeneratorIncrementFloat, ColumnGeneratorIncrementInt,
    ColumnGeneratorIncrementTime)
from .generator.column_generator_normal_distribution import (
    ColumnGeneratorNormalDistributionFloat,
    ColumnGeneratorNormalDistributionInt)
from .generator.column_generator_template_geolocation import (
    ColumnGeneratorTemplateGeolocationFloat,
    ColumnGeneratorTemplateGeolocationInt)
from .generator.column_generator_template_label import (
    ColumnGeneratorTemplateId, ColumnGeneratorTemplateLabelString)
from .generator.column_generator_template_timeseries import (
    ColumnGeneratorTimeseriesTemplateFloat,
    ColumnGeneratorTimeseriesTemplateInt)
from .generator.column_generator_template_timestamp import (
    ColumnGeneratorTimestampTemplateDate,
    ColumnGeneratorTimestampTemplateDatetime,
    ColumnGeneratorTimestampTemplateTime)
from .generator.column_generator_uniform_distribution import (
    ColumnGeneratorUniformDistributionDate,
    ColumnGeneratorUniformDistributionDatetime,
    ColumnGeneratorUniformDistributionFloat,
    ColumnGeneratorUniformDistributionInt,
    ColumnGeneratorUniformDistributionTime)
from .generator.column_generator_unique import (ColumnGeneratorUniqueFloat,
                                                ColumnGeneratorUniqueInt)
from .generator.column_generator_weights_table import (
    ColumnGeneratorWeightsTableDate, ColumnGeneratorWeightsTableDatetime,
    ColumnGeneratorWeightsTableFloat, ColumnGeneratorWeightsTableInt,
    ColumnGeneratorWeightsTableString, ColumnGeneratorWeightsTableTime)
from .generator.sequence_generator_loop import SequenceGeneratorLoop
from .generator.sequence_generator_loop_random import \
    SequenceGeneratorLoopRandom
from .generator.sequence_generator_template import SequenceGeneratorTemplate
from .generator.table_generator import TableGenerator
from .helpers.args_convertion import prepare_args_from_descriptor
from .helpers.template_column_naming import template_from_column_type
from .templates import get_templates_provider

available_generators = [
    ColumnGeneratorIncrementInt,
    ColumnGeneratorIncrementFloat,
    ColumnGeneratorIncrementDatetime,
    ColumnGeneratorIncrementDate,
    ColumnGeneratorIncrementTime,
    ColumnGeneratorUniqueInt,
    ColumnGeneratorUniqueFloat,
    ColumnGeneratorUniformDistributionInt,
    ColumnGeneratorUniformDistributionFloat,
    ColumnGeneratorUniformDistributionDatetime,
    ColumnGeneratorUniformDistributionDate,
    ColumnGeneratorUniformDistributionTime,
    ColumnGeneratorNormalDistributionInt,
    ColumnGeneratorNormalDistributionFloat,
    ColumnGeneratorExponentialDistributionInt,
    ColumnGeneratorExponentialDistributionFloat,
    ColumnGeneratorWeightsTableInt,
    ColumnGeneratorWeightsTableFloat,
    ColumnGeneratorWeightsTableString,
    ColumnGeneratorWeightsTableDatetime,
    ColumnGeneratorWeightsTableDate,
    ColumnGeneratorWeightsTableTime,
    SequenceGeneratorLoop,
    SequenceGeneratorLoopRandom,
    SequenceGeneratorTemplate,
    ColumnGeneratorTemplateLabelString,
    ColumnGeneratorTimestampTemplateDatetime,
    ColumnGeneratorTimestampTemplateDate,
    ColumnGeneratorTimestampTemplateTime,
    ColumnGeneratorTimeseriesTemplateInt,
    ColumnGeneratorTimeseriesTemplateFloat,
    ColumnGeneratorTemplateGeolocationInt,
    ColumnGeneratorTemplateGeolocationFloat,
    ColumnGeneratorTemplateId,
    TableGenerator,
]


def create_table_generator(table_descriptor: TableDescriptor):
    table_generator = get_generator_hierarchy(table_descriptor)
    return table_generator


def get_generator_hierarchy(
    root_descriptor: Union[TableDescriptor, Sequence],
    seed=0,
    template_filters=None,
    common_dependencies: list[str] = None,
):
    propagate_templates = True
    # Empty template_filters ({}, but not None) is also considered to override parent
    # filters
    if (
        hasattr(root_descriptor, "template_filters")
        and root_descriptor.template_filters is not None
    ):
        template_filters = root_descriptor.template_filters
        # This can break synchronization as new filters are introduced. It can happen
        # that the parent sequence pushes to children values (e.g. country == 1), but
        # the new filter is different (e.g. country == 2). And when resolving filters
        # using conjuction (country == 1 AND coutnry == 2), this results in empty
        # filter. As a solution we do not propagate template values.
        propagate_templates = False

    if (
        hasattr(root_descriptor, "common_dependencies")
        and root_descriptor.common_dependencies
    ):
        common_dependencies = root_descriptor.common_dependencies

    # Resolve all parent filters and dependencies
    provider = get_templates_provider()
    if provider:
        # We need to find filters also on parents of specified template filters,
        # otherwise it can be without effect. For example, a filter with country_id
        # needs to find also relevant continent_id values. This is because in this case,
        # the continent dependecy is generated first and we need to generate only those
        # continents which contain specified countries.
        template_filters = provider.find_related_filters(template_filters)
        common_dependencies = provider.find_related_common_dependencies(
            common_dependencies
        )

    root_generator = create_generator(
        root_descriptor,
        seed,
        template_filters,
        common_dependencies,
        propagate_templates,
    )
    root_generator.child_column_generators = []
    root_generator.child_sequence_generator = None

    column_descriptors = []
    sequence_descriptors = []

    for descriptor in root_descriptor.descriptors:
        if "SEQ" in descriptor.get_descriptor_type():
            sequence_descriptors.append(descriptor)
        else:
            column_descriptors.append(descriptor)

    if len(sequence_descriptors) > 1:
        raise Exception("More than 1 sequence is present in the sequence group.")

    if len(sequence_descriptors) == 1:
        root_generator.child_sequence_generator = get_generator_hierarchy(
            sequence_descriptors[0], seed, template_filters, common_dependencies
        )

    # Create generators and internal generators
    generators, internal_generators = create_generators(
        column_descriptors, root_descriptor.seed, template_filters, common_dependencies
    )

    # Create internal generators for templated sequence dependencies
    if root_generator.child_sequence_generator:
        if root_generator.child_sequence_generator.strong_dependencies is not None:
            internal_generators.extend(
                create_internal_generators_hierarchy(
                    root_generator.child_sequence_generator.strong_dependencies,
                    root_descriptor.seed,
                    root_generator.child_sequence_generator.seed,
                    root_generator.child_sequence_generator.template_filters,
                    common_dependencies,
                )
            )

    # Add generators and internal generators to the root sequence.
    # This order is necessary for template label dependency: reverse order causes
    # the dependency column multiplied.
    for generator in generators:
        root_generator.add_child_column_generator(generator)
    for internal_generator in internal_generators:
        root_generator.add_internal_child_column_generator(internal_generator)

    # link internal generators based on dependencies
    for generator in root_generator.get_generator_columns():
        dependencies = []
        if generator.dependencies:
            dependencies.extend(generator.dependencies)
        if generator.label_dependencies:
            dependencies.extend(generator.label_dependencies)

        for dependency in dependencies:
            # Find dependency generator based on its seed
            dependency_generator = root_generator.get_generator_by_type(
                dependency, generator.seed
            )
            # If not found based on its seed, try to find by common seed - this is
            # common dependency
            if not dependency_generator:
                dependency_generator = root_generator.get_generator_by_type(
                    dependency, root_generator.seed
                )
            if dependency_generator:
                generator.linked_internal_generators[dependency] = dependency_generator

    root_generator.sort_child_generators()

    return root_generator


def create_generators(
    column_descriptors: list[Descriptor],
    seed_parent=1,
    template_filters=None,
    common_dependencies: list[str] = None,
):
    generators = []
    internal_generators = []

    for column_descriptor in column_descriptors:
        # Prepare filters for generator creation
        if (
            hasattr(column_descriptor, "behaviour")
            and hasattr(column_descriptor.behaviour, "template_filters")
            and column_descriptor.behaviour.template_filters
        ):
            filters = column_descriptor.behaviour.template_filters
        elif template_filters:
            filters = template_filters
        else:
            filters = None

        # Create column generator
        column_generator = create_generator(
            column_descriptor, seed_parent, filters, common_dependencies
        )
        generators.append(column_generator)

        # Analyze dependencies and create internal generators
        if column_generator.strong_dependencies is not None:
            internal_generators.extend(
                create_internal_generators_hierarchy(
                    column_generator.strong_dependencies
                    + column_generator.label_dependencies,
                    seed_parent,
                    column_descriptor.seed,
                    column_generator.template_filters,
                    common_dependencies,
                )
            )

    return generators, internal_generators


def create_generator(
    column_descriptor: Descriptor,
    seed: int = 1,
    template_filters=None,
    common_dependencies: list[str] = None,
    propagate_templates=True,
):
    descriptor_type = column_descriptor.get_descriptor_type()

    args = prepare_args_from_descriptor(column_descriptor)
    if "COL" in descriptor_type:
        args = args | {"seed_sequence": seed}
    if "SEQ" in descriptor_type:
        args = args | {"seed_parent": seed}
        args = args | {"propagate_templates": propagate_templates}
    if "TEMPLATE" in descriptor_type:
        args = args | {"templates_provider": get_templates_provider()}
        args = args | {"template_filters": template_filters}
        args = args | {"common_dependencies": common_dependencies}

    generator = instantiate_generator_by_type(descriptor_type, args)
    return generator


def create_internal_generators_hierarchy(
    dependencies: [str],
    seed_sequence: int = 1,
    seed_column: int = 1,
    template_filters=None,
    common_dependencies: list[str] = None,
):
    generators = create_internal_generators(
        dependencies, seed_sequence, seed_column, template_filters, common_dependencies
    )

    for generator in generators:
        if generator.dependencies is not None:
            generators = (
                create_internal_generators_hierarchy(
                    generator.strong_dependencies,
                    seed_sequence,
                    seed_column,
                    template_filters,
                    common_dependencies,
                )
                + generators
            )

    return generators


def create_internal_generators(
    dependencies: [str],
    seed_sequence: int = 1,
    seed_column: int = 1,
    template_filters=None,
    common_dependencies: list[str] = None,
):
    generators = []

    for generator_type in dependencies:
        if ColumnGeneratorTemplateId.generator_type in generator_type:
            template = template_from_column_type(generator_type).upper()
            key = f"{template}_ID"
            if common_dependencies and key.lower() in common_dependencies:
                seed_column = 0
            generator = ColumnGeneratorTemplateId(
                id=str(uuid.uuid4()),
                name=f"{key}_{seed_sequence + seed_column}",
                seed_sequence=seed_sequence,
                seed_column=seed_column,
                visible=False,
                na_prob=0,
                template_name=template,
                templates_provider=get_templates_provider(),
                template_filters=template_filters,
            )

            generators.insert(0, generator)

        elif ColumnGeneratorTemplateLabelString.generator_type in generator_type:
            template = template_from_column_type(generator_type).upper()
            key = f"{template}"
            if common_dependencies and key.lower() in common_dependencies:
                seed_column = 0
            generator = ColumnGeneratorTemplateLabelString(
                id=str(uuid.uuid4()),
                name=f"{key}_{seed_sequence + seed_column}",
                seed_sequence=seed_sequence,
                seed_column=seed_column,
                visible=False,
                na_prob=0,
                template_name=template,
                templates_provider=get_templates_provider(),
                template_filters=template_filters,
            )

            generators.insert(0, generator)

        else:
            raise ValueError(f"Unknown internal generator type {generator_type}")

    return generators


def instantiate_generator_by_type(generator_type: str, args: dict):
    for generator in available_generators:
        if generator.generator_type == generator_type:
            return generator(**args)

    raise ValueError(f"Unknown generator type {generator_type}")
