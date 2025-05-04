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


def broadcast_series_with_group_or_foreign_keys(
    original_series: pd.Series, expected_length: int
) -> pd.Series:
    """Broadcast series with group or foreign keys.

    Example:
    -------
    >>> original_series = pd.Series([0, 1, 2])
    >>> expected_length = 6
    >>> broadcast_series_with_group_or_foreign_keys(original_series, expected_length)
    >>> 0    0
    >>> 1    1
    >>> 2    2
    >>> 3    3
    >>> 4    4
    >>> 5    5

    >>> original_series = pd.Series([-1, 0, 2])
    >>> expected_length = 6
    >>> broadcast_series_with_group_or_foreign_keys(original_series, expected_length)
    >>> 0    -1
    >>> 1    0
    >>> 2    2
    >>> 3    -1
    >>> 4    3
    >>> 5    5
    """
    number_of_personas = expected_length // len(original_series)

    repeated_series = pd.Series(np.tile(original_series.values, number_of_personas))

    # How much to add to each row of the repeated series (if it is not -1)
    to_add_if_not_minus_one = np.repeat(
        np.arange(number_of_personas) * len(original_series), len(original_series)
    )

    is_valid_id = repeated_series >= 0
    repeated_series[is_valid_id] += to_add_if_not_minus_one[is_valid_id]

    return repeated_series


def _fail_if_persona_p_id_invalid(p_id_series: pd.Series) -> None:
    """Fail if persona p_id does not start with 0 and increment in steps of 1."""
    valid = pd.Series(list(range(len(p_id_series))))
    if not p_id_series.equals(valid):
        msg = f"""
        Persona p_id does not start with 0 and increment in steps of 1.
        Found: {p_id_series.to_list()}
        """
        raise ValueError(msg)


def _fail_if_data_to_upsert_is_not_dict_with_series_leafs(
    data_to_upsert: NestedDataDict,
) -> None:
    """Fail if data_to_upsert is not a dictionary with pandas Series as leafs.

    Args:
        data_to_upsert: Data to be upserted

    Raises:
        TypeError:
            If data_to_upsert is not a dictionary with pandas Series as leafs
    """
    if not isinstance(data_to_upsert, dict):
        msg = f"""
        data_to_upsert must be a dictionary.
        You provided: {type(data_to_upsert)}
        """
        raise TypeError(msg)

    flat_data_to_upsert = dt.flatten_to_qual_names(data_to_upsert)
    if not all(isinstance(v, pd.Series) for v in flat_data_to_upsert.values()):
        msg = f"""
        All leafs in data_to_upsert must be pandas Series.
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
    flat_data_to_upsert = dt.flatten_to_qual_names(data_to_upsert)
    flat_data_from_persona = dt.flatten_to_qual_names(data_from_persona)

    length_to_upsert = len(next(iter(flat_data_to_upsert.values())))

    if any(length_to_upsert != len(v) for v in flat_data_to_upsert.values()):
        incompatible_lengths = {
            key: len(value)
            for key, value in flat_data_to_upsert.items()
            if length_to_upsert != len(value)
        }
        msg = f"""
        The length of data in data_to_upsert differs, which is not allowed.
        Expected length: {length_to_upsert}
        Found lengths:

        {incompatible_lengths}
        """
        raise ValueError(msg)

    length_from_persona = len(next(iter(flat_data_from_persona.values())))

    if length_to_upsert % length_from_persona != 0:
        msg = f"""
        The length of data in data_to_upsert is not a multiple of the length of data in
        data_from_persona.

        Lengths:
        - data_to_upsert: {length_to_upsert}
        - data_from_persona: {length_from_persona}
        """
        raise ValueError(msg)
