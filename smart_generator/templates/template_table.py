from smart_generator.templates.enums import TimeseriesUnit


class TemplateTable:
    """
    A class used to represent a template table. Holds information about the source data
    and its dependencies.

    Attributes:
        name (str): Name of the table.
        source_name (str): Name of the source.
        label_column (str): Which column contains values.
        weight_column (str): Which column contains weights.
        id_column (str): Which column contains codetable keys.
        dependency_templates (list): References to other table keys on which this table
            is dependent.
        weak_dependency_templates (list): References to other table keys on which this
            table is weakly dependent. Weak dependency means that the table can be
            generated without the dependency, but if the dependency is present already
            in the generator structure or in the filters, it is used.
        label_dependency_templates (list): References to columns which are used
            to generate values. For example email is generated from firstname and
            lastname.
        randomize (bool): Whether to randomize the order of values for the generator.
            If false, the values are sorted as in the databse.
        using_expressions (bool): Whether the table is using expressions to generate values.
    """

    def __init__(
        self,
        name: str,
        source_name: str,
        label_column: str = "label",
        weight_column="weight",
        id_column: str = None,
        dependency_templates: list[str] = [],
        weak_dependency_templates: list[str] = [],
        label_dependency_templates: list[str] = [],
        randomize: bool = True,
        using_expressions: bool = False,
    ):
        """
        Constructor of the TemplateTable class.

        Args:
            name (str): Name of the table.
            source_name (str): Name of the source.
            label_column (str): Which column contains values.
            weight_column (str): Which column contains weights.
            id_column (str): Which column contains codetable keys.
            dependency_templates (list): References to other table keys on which this
                table is dependent.
            weak_dependency_templates (list): References to other table keys on which
                this table is weakly dependent. Weak dependency means that the table can
                be generated without the dependency, but if the dependency is present
                already in the generator structure or in the filters, it is used.
            label_dependency_templates (list): References to columns which are used
                to generate values. For example email is generated from firstname and
                lastname.
            randomize (bool): Whether to randomize the order of values for
                the generator. If false, the values are sorted as in the databse.
            using_expressions (bool): Whether the table is using expressions
                to generate values.
        """
        self.name = name
        self.source_name = source_name
        self.label_column = label_column
        self.weight_column = weight_column
        self.id_column = id_column
        self.dependency_templates = dependency_templates
        self.weak_dependency_templates = weak_dependency_templates
        self.label_dependency_templates = label_dependency_templates
        self.randomize = randomize
        self.using_expressions = using_expressions


class TemplateTimestampTable(TemplateTable):
    """
    A subclass of TemplateTable used to represent a template table with timestamps.

    Attributes:
        frame (TimeseriesUnit): A timeframe of the timeseries in the source data.
        unit (TimeseriesUnit): A time unit of the timeseries.
    """

    def __init__(
        self,
        name: str,
        source_name: str,
        frame: TimeseriesUnit,
        unit: TimeseriesUnit,
        label_column: str = "timestamp",
        weight_column="weight",
        dependency_templates: list[str] = [],
        weak_dependency_templates: list[str] = [],
        label_dependency_templates: list[str] = [],
        randomize: bool = True,
    ):
        """
        Constructor of the TemplateTimestampTable class.

        Args:
            frame (TimeseriesUnit): A timeframe of the timeseries in the source data.
            unit (TimeseriesUnit): A time unit of the timeseries.
        """
        super().__init__(
            name,
            source_name,
            label_column,
            weight_column,
            None,
            dependency_templates,
            weak_dependency_templates,
            label_dependency_templates,
            randomize,
            False,
        )
        self.frame = frame
        self.unit = unit


class TemplateGeoLocationTable:
    """
    A subclass of TemplateTable used to represent a template table with geolocation
    data.

    Attributes:
        longitude_column (str): Which column contains longitude values.
        latitude_column (str): Which column contains latitude values.
    """

    def __init__(
        self,
        name: str,
        source_name: str,
        longitude_column: str = "longitude",
        latitude_column: str = "latitude",
        weight_column="weight",
        id_column: str = None,
        dependency_templates: list[str] = [],
        weak_dependency_templates: list[str] = [],
        label_dependency_templates: list[str] = [],
        randomize: bool = True,
    ):
        """
        Constructor of the TemplateGeoLocationTable class.

        Args:
            longitude_column (str): Which column contains longitude values.
            latitude_column (str): Which column contains latitude values.
        """
        self.name = name
        self.source_name = source_name
        self.longitude_column = longitude_column
        self.latitude_column = latitude_column
        self.id_column = id_column
        self.weight_column = weight_column
        self.dependency_templates = dependency_templates
        self.weak_dependency_templates = weak_dependency_templates
        self.label_dependency_templates = label_dependency_templates
        self.randomize = randomize
