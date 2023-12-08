import numpy


def unique_combinations_from_columns(columns):
    """
    Returns unique combinations from the given columns.

    Args:
        columns (list[list]): List of columns.

    Returns:
        list: List of unique combinations.
    """
    zipped = list(zip(*columns))
    unique_combinations = list(set(zipped))
    return unique_combinations


def rows_from_columns(columns):
    """
    Transforms the given columns into rows.

    Args:
        columns (list[list]): List of columns.

    Returns:
        list: List of rows.
    """
    zipped = list(zip(*columns))
    all_combinations = numpy.array(zipped)
    return all_combinations
