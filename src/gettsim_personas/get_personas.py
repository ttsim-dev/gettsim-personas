"""Get personas and upsert input data."""

from __future__ import annotations

import itertools
from datetime import date
from typing import TYPE_CHECKING

import dags.tree as dt
import numpy as np
import pandas as pd

from gettsim_personas.broadcasting import (
    _fail_if_data_lengths_are_incompatible,
    _fail_if_data_to_upsert_is_not_dict_with_array_or_series_leafs,
    broadcast_foreign_keys,
    broadcast_group_ids,
    broadcast_p_id,
)
from gettsim_personas.load_personas import load_personas
from gettsim_personas.persona_objects import PersonaCollection

if TYPE_CHECKING:
    from gettsim_personas.typing import NestedDataDict, Persona


def get_personas(date_str: str) -> PersonaCollection:
    """Collection of personas that are active at a given date.

    Args:
        date_str: Date in ISO format (YYYY-MM-DD)

    Returns:
        PersonaCollection containing only personas active at the given date
    """
    all_personas = load_personas()
    target_date = date.fromisoformat(date_str)
    _fail_if_multiple_personas_with_same_name_active_at_same_date(all_personas)
    active_personas = {
        p.name: p for p in all_personas if p.start_date <= target_date <= p.end_date
    }

    return PersonaCollection(personas=active_personas, date=target_date)


def upsert_input_data(
    data_from_persona: NestedDataDict,
    data_to_upsert: NestedDataDict,
) -> NestedDataDict:
    """Upsert GETTSIM input data.

    Updates and inserts new values into a NestedDataDict with input data for GETTSIM,
    e.g. created from a persona via `get_personas`. Data not in `data_to_upsert` is
    broadcasted to match the length of `data_to_upsert`.

    The length of data in `data_to_upsert` must be a multiple of the length of data in
    `data_from_persona`.

    Args:
        data_from_persona:
            NestedDataDict with input data for GETTSIM. Typically created from a persona
            object via `get_personas`.
        data_to_upsert:
            NestedDataDict with data to be upserted

    Returns:
        NestedDataDict with upserted data
    """
    _fail_if_data_to_upsert_is_not_dict_with_array_or_series_leafs(data_to_upsert)
    _fail_if_data_lengths_are_incompatible(data_to_upsert, data_from_persona)
    flat_data_to_upsert = dt.flatten_to_tree_paths(data_to_upsert)
    flat_data_from_persona = dt.flatten_to_tree_paths(data_from_persona)

    expected_length = len(next(iter(flat_data_to_upsert.values())))
    persona_length = len(next(iter(flat_data_from_persona.values())))
    number_of_new_personas = expected_length // persona_length

    upserted_data = flat_data_to_upsert.copy()
    for path, series in flat_data_from_persona.items():
        if path in upserted_data:
            continue
        if path == ("p_id",):
            broadcasted_series = broadcast_p_id(
                original_series=series,
                expected_length=expected_length,
            )
        elif "p_id_" in path[-1]:
            broadcasted_series = broadcast_foreign_keys(
                original_series=series,
                expected_length=expected_length,
            )
        elif path[-1].endswith("_id"):
            broadcasted_series = broadcast_group_ids(
                original_series=series, expected_length=expected_length
            )
        else:
            broadcasted_series = pd.Series(
                np.tile(series.values, number_of_new_personas)
            )

        broadcasted_series.name = path[-1]
        broadcasted_series.index = pd.RangeIndex(expected_length)
        upserted_data[path] = broadcasted_series

    return dt.unflatten_from_tree_paths(upserted_data)


def _fail_if_multiple_personas_with_same_name_active_at_same_date(
    all_personas: list[Persona],
) -> None:
    """Fail if multiple personas with the same name are active at the same date."""
    persona_names_to_active_periods: dict[str, list[tuple[date, date]]] = {}
    for persona in all_personas:
        if persona.name not in persona_names_to_active_periods:
            persona_names_to_active_periods[persona.name] = []
        persona_names_to_active_periods[persona.name].append(
            (persona.start_date, persona.end_date)
        )
    for persona_name, all_active_periods in persona_names_to_active_periods.items():
        if len(all_active_periods) > 1:
            for (start1, end1), (start2, end2) in itertools.combinations(
                all_active_periods, 2
            ):
                if start1 <= end2 and start2 <= end1:
                    msg = (
                        f"Multiple personas with the name '{persona_name}' are active "
                        f"at the same date. Overlapping periods: {start1} - {end1} and "
                        f"{start2} - {end2}."
                    )
                    raise ValueError(msg)
