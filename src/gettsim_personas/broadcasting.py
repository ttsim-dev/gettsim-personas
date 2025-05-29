"""Functions to broadcast GETTSIM input data."""

from __future__ import annotations

from typing import TYPE_CHECKING

import dags.tree as dt
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from gettsim_personas.interface import NestedDataDict


def broadcast_p_id(original_series: pd.Series, expected_length: int) -> pd.Series:
    """Broadcast p_id to the expected length.

    Fails (for simplicity) if the persona p_id does not start with 0 or is not
    consecutive.
    """
    _fail_if_persona_p_id_invalid(original_series)
    return pd.Series(list(range(expected_length)))


def broadcast_group_ids(original_series: pd.Series, expected_length: int) -> pd.Series:
    """Broadcast series with group IDs.

    Group IDs are used to identify groups of rows that should be treated together.
    The exact values don't matter as long as they maintain the same grouping pattern.

    Example:
    -------
    >>> original_series = pd.Series([0, 1, 1])
    >>> expected_length = 6
    >>> broadcast_group_ids(original_series, expected_length)
    >>> 0    0
    >>> 1    1
    >>> 2    1
    >>> 3    2
    >>> 4    3
    >>> 5    3
    """
    number_of_personas = expected_length // len(original_series)

    repeated_series = pd.Series(
        np.tile(original_series.values, reps=number_of_personas)
    )

    max_original_id = original_series.max()
    to_add = np.repeat(
        np.arange(number_of_personas) * (max_original_id + 1),
        repeats=len(original_series),
    )

    repeated_series += to_add

    return repeated_series


def broadcast_foreign_keys(
    original_series: pd.Series, expected_length: int
) -> pd.Series:
    """Broadcast series with foreign keys.

    Foreign keys are used to reference specific rows in another table.

    Example:
    -------
    >>> original_series = pd.Series([1, 0, -1])
    >>> expected_length = 6
    >>> broadcast_foreign_keys(original_series, expected_length)
    >>> 0    1
    >>> 1    0
    >>> 2    -1
    >>> 3    4
    >>> 4    3
    >>> 5    -1
    """
    number_of_personas = expected_length // len(original_series)

    repeated_series = pd.Series(
        np.tile(original_series.values, reps=number_of_personas)
    )

    to_add_if_not_minus_one = np.repeat(
        np.arange(number_of_personas) * len(original_series),
        repeats=len(original_series),
    )

    is_valid_id = repeated_series >= 0
    repeated_series[is_valid_id] += to_add_if_not_minus_one[is_valid_id]

    return repeated_series


def _fail_if_persona_p_id_invalid(p_id_series: pd.Series) -> None:
    """Fail if persona p_id does not start with 0 or increment in steps of 1."""
    valid = pd.Series(list(range(len(p_id_series))))
    if not p_id_series.equals(valid):
        msg = f"""
        Persona p_id does not start with 0 or increment in steps of 1.
        Found: {p_id_series.to_list()}
        """
        raise ValueError(msg)


def _fail_if_data_to_upsert_is_not_dict_with_array_or_series_leafs(
    data_to_upsert: NestedDataDict,
) -> None:
    """Fail if data_to_upsert is not a dictionary with Arrays as leafs.

    Args:
        data_to_upsert: Data to be upserted

    Raises:
        TypeError:
            If data_to_upsert is not a dictionary with Arrays as leafs
    """
    if not isinstance(data_to_upsert, dict):
        msg = f"""
        data_to_upsert must be a dictionary.
        You provided: {type(data_to_upsert)}
        """
        raise TypeError(msg)

    flat_data_to_upsert = dt.flatten_to_tree_paths(data_to_upsert)
    if not all(
        isinstance(v, (pd.Series, np.ndarray, list))
        for v in flat_data_to_upsert.values()
    ):
        msg = f"""
        All leafs in data_to_upsert must be pandas Series, numpy Arrays, or lists.
        You provided: {flat_data_to_upsert.values()}
        """
        raise TypeError(msg)


def _fail_if_data_lengths_are_incompatible(
    data_to_upsert: NestedDataDict,
    data_from_persona: NestedDataDict,
) -> None:
    """Fail if data lengths are incompatible.

    Lengths are incompatible if:
        - lengths in data_to_upsert are not all the same
        - lengths in data_to_upsert are not a multiple of the length in
          data_from_persona

    Args:
        data_to_upsert: Data to be upserted
        data_from_persona: Source data

    Raises:
        ValueError:
            If lengths in data_to_upsert differ
        ValueError:
            If lengths in data_to_upsert are not a multiple of the length in
            data_from_persona
    """
    flat_data_to_upsert = dt.flatten_to_tree_paths(data_to_upsert)
    flat_data_from_persona = dt.flatten_to_tree_paths(data_from_persona)

    # Get the length of any leaf of data_to_upsert
    length_of_data_to_upsert = len(next(iter(flat_data_to_upsert.values())))

    # Check if all leafs of data_to_upsert have the same length
    incompatible_lengths_in_data_to_upsert = {
        key: len(value)
        for key, value in flat_data_to_upsert.items()
        if length_of_data_to_upsert != len(value)
    }
    if incompatible_lengths_in_data_to_upsert:
        msg = f"""
        The length of data in data_to_upsert differs, which is not allowed.
        Expected length: {length_of_data_to_upsert}
        Found lengths:

        {incompatible_lengths_in_data_to_upsert}
        """
        raise ValueError(msg)

    # Get the length of any leaf of data_from_persona
    length_from_persona = len(next(iter(flat_data_from_persona.values())))

    # Check if the length of data_to_upsert is a multiple of the length of
    # data_from_persona
    if length_of_data_to_upsert % length_from_persona != 0:
        msg = f"""
        The length of data in data_to_upsert is not a multiple of the length of data in
        data_from_persona.

        Lengths:
        - data_to_upsert: {length_of_data_to_upsert}
        - data_from_persona: {length_from_persona}
        """
        raise ValueError(msg)
