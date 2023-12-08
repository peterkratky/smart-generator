def filters_conjunction(filters1: dict[str, list[int]], filters2: dict[str, list[int]]):
    """
    Returns conjunction of two filters.

    Args:
        filters1 (dict[str, list[int]]): First filter.
        filters2 (dict[str, list[int]]): Second filter.

    Returns:
        dict[str, list[int]]: Conjunction of the given filters.
    """
    if filters1 is None:
        return filters2

    filters = filters1
    if filters2:
        for key, values2 in filters2.items():
            if key in filters:
                values = filters[key]
                values = list(set(values) & set(values2))
                filters[key] = values
            else:
                filters[key] = values2

    return filters


def filters_merge(filters1: dict[str, list[int]], filters2: dict[str, list[int]]):
    """
    Merges two filters. If there is a mismatch in the values of the same key,
    an exception is raised.

    Args:
        filters1 (dict[str, list[int]]): First filter.
        filters2 (dict[str, list[int]]): Second filter.

    Returns:
        dict[str, list[int]]: Merged filters.

    Raises:
        Exception: If there is a mismatch in the values of the same key.
    """
    if filters1 is None:
        return filters2

    filters = filters1
    if filters2:
        for key, values2 in filters2.items():
            if key in filters:
                values = filters[key]
                if values != values2:
                    raise Exception(
                        f"Mismatch in filters detected for key {key}: [{','.join(map(str, values))}] versus [{','.join(map(str, values2))}]"
                    )
                filters[key] = values
            else:
                filters[key] = values2

    return filters
